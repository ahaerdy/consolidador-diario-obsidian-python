#!/usr/bin/env python3
"""
Consolidador de Métricas do Diário Obsidian
============================================
Extrai dados do frontmatter YAML de notas diárias do Obsidian e os consolida
em um único arquivo de texto estruturado, pronto para leitura humana ou análise por IA.

Estrutura esperada do cofre Obsidian:
    base_path/YYYY/MM/YYYYMMDD.md

Uso:
    python consolida_diario.py <base_path> <output> <data_inicial> [data_final]

Exemplos:
    python consolida_diario.py ~/Obsidian/Diario ~/Downloads/consolidado.txt 20260201
    python consolida_diario.py ~/Obsidian/Diario ~/Downloads/jan.txt 20260101 20260131
"""

import os
import sys
import re
from datetime import datetime, timedelta
from pathlib import Path
import argparse


# =============================================================================
# FUNÇÕES UTILITÁRIAS
# =============================================================================

def parse_date(date_str):
    """Converte string YYYYMMDD para objeto datetime.

    Centraliza o parsing de datas para que qualquer erro de formato seja
    capturado em um único lugar com uma mensagem clara.

    Args:
        date_str (str): A data em formato string YYYYMMDD (ex: '20260201').

    Returns:
        datetime: Um objeto datetime representando a data.

    Raises:
        ValueError: Se a string de data não estiver no formato esperado.
    """
    try:
        # strptime faz o parse estrito — '20260132' (dia 32) lançaria ValueError automaticamente
        return datetime.strptime(date_str, "%Y%m%d")
    except ValueError:
        raise ValueError(f"Data inválida: {date_str}. Use o formato YYYYMMDD (ex: 20260201)")


def get_file_path(base_path, date_obj):
    """
    Monta o caminho completo do arquivo de nota diária baseado na data.

    O plugin Daily Notes do Obsidian pode ser configurado para usar diferentes
    estruturas de pastas. Este script assume: base_path/YYYY/MM/YYYYMMDD.md
    Se sua estrutura for diferente, altere apenas esta função.

    Args:
        base_path (str): O caminho base para o diretório das notas diárias.
        date_obj (datetime): Um objeto datetime representando a data da nota.

    Returns:
        str: O caminho completo para o arquivo da nota diária.
    """
    year = date_obj.strftime("%Y")   # Ex: '2026'
    month = date_obj.strftime("%m")  # Ex: '02' (com zero à esquerda)
    filename = date_obj.strftime("%Y%m%d.md")  # Ex: '20260201.md'

    # os.path.join garante o separador correto de acordo com o SO (/ no Unix, \ no Windows)
    return os.path.join(base_path, year, month, filename)


# =============================================================================
# LEITURA E EXTRAÇÃO DO FRONTMATTER
# =============================================================================

def extract_frontmatter(file_path):
    """
    Extrai o frontmatter YAML de um arquivo Markdown do Obsidian.

    O frontmatter é o bloco de metadados no início do arquivo delimitado por '---'.
    Exemplo:
        ---
        energia: 8
        sono: 7
        humor: calmo
        ---
        Conteúdo da nota...

    O parser aqui é intencialmente simples (linha a linha), otimizado para
    frontmatters com pares 'chave: valor' planos. Para frontmatters com listas
    ou valores multilinha, considere usar a biblioteca PyYAML.

    Args:
        file_path (str): O caminho para o arquivo markdown.

    Returns:
        dict or None:
            - None: arquivo não encontrado ou erro de leitura (I/O)
            - {}: arquivo existe mas não tem frontmatter
            - dict: frontmatter extraído com sucesso
    """
    # Retorna None para sinalizar "arquivo ausente" — diferente de {} (arquivo sem frontmatter)
    if not os.path.exists(file_path):
        return None

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Regex para capturar o bloco entre os dois delimitadores '---'
        # re.DOTALL: faz '.' casar com '\n' (necessário para blocos multilinha)
        # re.MULTILINE: faz '^' e '$' casarem com início/fim de cada linha
        # O '?' em '(.*?)' torna a busca "não-gulosa" — para no primeiro '---' de fechamento
        frontmatter_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL | re.MULTILINE)

        if not frontmatter_match:
            return {}  # Arquivo existe, mas não tem frontmatter — retorna dict vazio

        # .group(1) retorna apenas o conteúdo capturado pelo primeiro par de parênteses
        frontmatter_text = frontmatter_match.group(1)
        frontmatter_data = {}

        # Parse linha a linha: cada linha no formato 'chave: valor'
        for line in frontmatter_text.split('\n'):
            line = line.strip()
            if ':' in line:
                # split(':', 1) divide apenas no PRIMEIRO ':' — preserva ':' em valores
                # Ex: 'resumo_dia: Reunião às 14:00' → chave='resumo_dia', valor='Reunião às 14:00'
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                frontmatter_data[key] = value

        return frontmatter_data

    except Exception as e:
        # Qualquer erro de I/O ou encoding vai para stderr sem interromper o processamento
        print(f"Erro ao ler arquivo {file_path}: {e}", file=sys.stderr)
        return None


# =============================================================================
# FORMATAÇÃO DA SAÍDA
# =============================================================================

def format_entry(date_obj, frontmatter):
    """
    Formata uma entrada consolidada para o arquivo de saída.

    Itera sobre uma lista canônica de campos na ordem definida.
    Campos ausentes no frontmatter são emitidos como vazios (ex: 'hipotese: ').
    Isso garante formato consistente em todas as entradas, mesmo para notas
    mais antigas que não tinham todos os campos — compatibilidade retroativa.

    Args:
        date_obj (datetime): O objeto datetime da nota diária.
        frontmatter (dict): O dicionário contendo os dados do frontmatter.

    Returns:
        str: Uma string com a entrada formatada para aquela data.
    """
    date_str = date_obj.strftime("%Y%m%d")

    # Lista canônica de campos — define tanto a ordem de saída quanto os campos suportados.
    # Organizada em três blocos temáticos:
    #   Bloco 1: métricas físicas e cognitivas (quantitativas)
    #   Bloco 2: métricas subjetivas e narrativas (qualitativas)
    #   Bloco 3: registros estruturados (eventos e padrões)
    fields = [
        # Bloco 1 — Métricas físicas e cognitivas
        'energia',
        'sono',
        'foco',
        'tensao',
        'corpo',
        # Bloco 2 — Métricas subjetivas e narrativas
        'humor',
        'sucessos',
        'desafios',
        'resumo_dia',
        'insights',
        'gratidao',
        'proximo_passo',
        'fase',
        'detalhamento',
        # Bloco 3 — Registros estruturados
        'hipotese',
        'decisao',
        'marco',
        'falha',
        'revisao',
        'inventario',
        'padrao_identificado',
        'questao_aberta',
        'diretriz',
        'aviso',
        'sincronicidade',
        'sonho',
        'estetica',
    ]

    output = [f"Data: {date_str}"]  # Cabeçalho da entrada
    output.append("---")            # Separador visual de abertura

    for field in fields:
        # .get(field, '') retorna '' se o campo não existir — nunca lança KeyError
        value = frontmatter.get(field, '')
        output.append(f"{field}: {value}")

    output.append("---")  # Separador visual de fechamento

    # '\n'.join() é mais eficiente que concatenação de strings em loop
    return '\n'.join(output)


# =============================================================================
# GERAÇÃO DE INTERVALO DE DATAS
# =============================================================================

def generate_date_range(start_date, end_date):
    """
    Gera uma lista com todos os dias entre start_date e end_date (ambos inclusive).

    Usa timedelta para incremento diário — correto em qualquer caso, incluindo
    mudanças de mês, fim de ano e anos bissextos.

    Args:
        start_date (datetime): O objeto datetime da data de início.
        end_date (datetime): O objeto datetime da data de término.

    Returns:
        list[datetime]: Lista de objetos datetime, um por dia.
    """
    dates = []
    current = start_date

    while current <= end_date:
        dates.append(current)
        current += timedelta(days=1)  # timedelta garante incremento correto em qualquer mês/ano

    return dates


# =============================================================================
# PONTO DE ENTRADA — ORQUESTRAÇÃO PRINCIPAL
# =============================================================================

def main():
    """
    Função principal: configura a CLI, orquestra o processamento e grava o arquivo de saída.

    Fluxo:
        1. Parse e validação dos argumentos de linha de comando
        2. Geração do intervalo de datas
        3. Para cada data: monta o caminho, extrai o frontmatter, formata a entrada
        4. Escreve todas as entradas em um único arquivo de saída
        5. Exibe resumo final no terminal
    """
    # argparse gerencia automaticamente --help, erros de argumentos e a exibição de uso
    parser = argparse.ArgumentParser(
        description='Consolida métricas de notas diárias do Obsidian',
        formatter_class=argparse.RawDescriptionHelpFormatter,  # Preserva formatação do epilog
        epilog="""
Exemplos:
  %(prog)s /caminho/notas ./saida.txt 20260201              # Do dia 20260201 até hoje
  %(prog)s /caminho/notas ./saida.txt 20260201 20260210     # Do dia 20260201 até 20260210
        """
    )

    # Argumentos posicionais: obrigatórios e sem flag (sem '--')
    parser.add_argument('base_path',
                       help='Caminho base das notas (ex: /home/usuario/Obsidian/Diario)')
    parser.add_argument('output',
                       help='Caminho completo do arquivo de saída (ex: ~/Downloads/consolidado.txt)')
    parser.add_argument('data_inicial',
                       help='Data inicial no formato YYYYMMDD (ex: 20260201)')

    # nargs='?' torna o argumento opcional; se omitido, args.data_final será None
    parser.add_argument('data_final',
                       nargs='?',
                       help='Data final no formato YYYYMMDD (opcional, padrão: hoje)')

    args = parser.parse_args()

    # --- Validação das datas ---
    try:
        start_date = parse_date(args.data_inicial)
    except ValueError as e:
        print(f"Erro: {e}", file=sys.stderr)
        sys.exit(1)

    if args.data_final:
        try:
            end_date = parse_date(args.data_final)
        except ValueError as e:
            print(f"Erro: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Se data_final não for informada, consolida até o dia atual
        end_date = datetime.now()

    # Validação de negócio: intervalo invertido não faz sentido
    if start_date > end_date:
        print("Erro: Data inicial não pode ser posterior à data final", file=sys.stderr)
        sys.exit(1)

    # Valida que o diretório base do cofre Obsidian existe antes de processar
    if not os.path.isdir(args.base_path):
        print(f"Erro: Diretório base não encontrado: {args.base_path}", file=sys.stderr)
        sys.exit(1)

    # --- Processamento ---
    dates = generate_date_range(start_date, end_date)

    print(f"Processando {len(dates)} dias de {start_date.strftime('%Y-%m-%d')} a {end_date.strftime('%Y-%m-%d')}...")

    entries = []     # Acumula as entradas formatadas de cada dia
    files_found = 0  # Contador de arquivos processados com sucesso
    files_missing = 0  # Contador de arquivos não encontrados

    for date in dates:
        file_path = get_file_path(args.base_path, date)
        frontmatter = extract_frontmatter(file_path)

        if frontmatter is not None:
            # Arquivo encontrado (mesmo que sem frontmatter — retorna {} nesse caso)
            files_found += 1
            entry = format_entry(date, frontmatter)
            entries.append(entry)
        else:
            # Arquivo ausente ou erro de leitura — registra aviso e continua
            files_missing += 1
            print(f"  Aviso: Arquivo não encontrado ou vazio: {file_path}", file=sys.stderr)

    # --- Gravação do arquivo de saída ---
    try:
        # os.path.expanduser converte '~' para o home do usuário em qualquer SO
        output_path = os.path.expanduser(args.output)

        # exist_ok=True evita erro se os diretórios pai já existirem
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            # Entradas separadas por linha em branco para facilitar leitura e parsing futuro
            f.write('\n\n'.join(entries))

        # Resumo final — confirmação visual do que foi feito
        print(f"\n✓ Consolidado gerado com sucesso!")
        print(f"  Arquivo: {output_path}")
        print(f"  Arquivos processados: {files_found}")
        print(f"  Arquivos não encontrados: {files_missing}")

    except Exception as e:
        print(f"Erro ao salvar arquivo: {e}", file=sys.stderr)
        sys.exit(1)


# Guard padrão do Python: main() só é chamada quando o script é executado diretamente.
# Se este módulo for importado por outro script, main() NÃO é chamada automaticamente.
if __name__ == '__main__':
    main()