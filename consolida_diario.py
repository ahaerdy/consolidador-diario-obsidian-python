#!/usr/bin/env python3
"""
Consolidador de Métricas do Diário Obsidian
Extrai dados do frontmatter de notas diárias e gera arquivo consolidado.
"""

import os
import sys
import re
from datetime import datetime, timedelta
from pathlib import Path
import argparse


def parse_date(date_str):
    """Converte string YYYYMMDD para objeto datetime.

    Args:
        date_str (str): A data em formato string YYYYMMDD (ex: '20260201').

    Returns:
        datetime: Um objeto datetime representando a data.

    Raises:
        ValueError: Se a string de data não estiver no formato esperado.
    """
    try:
        return datetime.strptime(date_str, "%Y%m%d")
    except ValueError:
        raise ValueError(f"Data inválida: {date_str}. Use o formato YYYYMMDD (ex: 20260201)")


def get_file_path(base_path, date_obj):
    """
    Retorna o caminho completo do arquivo de nota diária do Obsidian baseado na data.
    A estrutura esperada é: base_path/YYYY/MM/YYYYMMDD.md

    Args:
        base_path (str): O caminho base para o diretório das notas diárias.
        date_obj (datetime): Um objeto datetime representando a data da nota.

    Returns:
        str: O caminho completo para o arquivo da nota diária.
    """
    year = date_obj.strftime("%Y")
    month = date_obj.strftime("%m")
    filename = date_obj.strftime("%Y%m%d.md")

    return os.path.join(base_path, year, month, filename)


def extract_frontmatter(file_path):
    """
    Extrai o frontmatter (metadados YAML) de um arquivo markdown do Obsidian.
    O frontmatter é delimitado por '---' no início e no fim.

    Args:
        file_path (str): O caminho para o arquivo markdown.

    Returns:
        dict or None: Um dicionário com os campos do frontmatter e seus valores,
                      ou None se o arquivo não existir ou houver um erro de leitura.
                      Retorna um dicionário vazio se não houver frontmatter.
    """
    if not os.path.exists(file_path):
        return None

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Procura por frontmatter delimitado por ---
        # re.DOTALL permite que '.' case com newlines
        # re.MULTILINE permite que '^' e '$' casem com o início/fim de cada linha
        frontmatter_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL | re.MULTILINE)

        if not frontmatter_match:
            return {}

        frontmatter_text = frontmatter_match.group(1) # Pega o conteúdo entre os delimitadores
        frontmatter_data = {}

        # Parse dos campos do frontmatter linha por linha
        for line in frontmatter_text.split('\n'):
            line = line.strip()
            if ':' in line:
                key, value = line.split(':', 1) # Divide apenas no primeiro ':'
                key = key.strip()
                value = value.strip()
                frontmatter_data[key] = value

        return frontmatter_data

    except Exception as e:
        print(f"Erro ao ler arquivo {file_path}: {e}", file=sys.stderr)
        return None


def format_entry(date_obj, frontmatter):
    """
    Formata uma entrada consolidada para o arquivo de saída com base nos dados
    extraídos do frontmatter de uma nota diária.

    Args:
        date_obj (datetime): O objeto datetime da nota diária.
        frontmatter (dict): O dicionário contendo os dados do frontmatter.

    Returns:
        str: Uma string formatada representando a entrada consolidada para aquela data.
    """
    date_str = date_obj.strftime("%Y%m%d")

    # Define a ordem e os campos a serem extraídos.
    # Campos ausentes no frontmatter serão preenchidos com uma string vazia,
    # garantindo compatibilidade retroativa com notas mais antigas.
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

    output = [f"Data: {date_str}"] # Inicia a saída com a data
    output.append("---") # Separador para o frontmatter

    for field in fields:
        value = frontmatter.get(field, '') # Pega o valor do campo ou string vazia se não existir
        output.append(f"{field}: {value}")

    output.append("---") # Separador final

    return '\n'.join(output) # Junta todas as linhas em uma única string


def generate_date_range(start_date, end_date):
    """
    Gera uma lista de objetos datetime para cada dia entre a data inicial e final (inclusive).

    Args:
        start_date (datetime): O objeto datetime da data de início.
        end_date (datetime): O objeto datetime da data de término.

    Returns:
        list: Uma lista de objetos datetime.
    """
    dates = []
    current = start_date

    while current <= end_date:
        dates.append(current)
        current += timedelta(days=1) # Adiciona um dia

    return dates


def main():
    """
    Função principal do script.
    Configura os argumentos de linha de comando, processa as notas diárias
    e gera o arquivo consolidado.
    """
    parser = argparse.ArgumentParser(
        description='Consolida métricas de notas diárias do Obsidian',
        formatter_class=argparse.RawDescriptionHelpFormatter, # Mantém a formatação dos exemplos
        epilog="""
Exemplos:
  %(prog)s /caminho/notas ./saida.txt 20260201              # Do dia 20260201 até hoje
  %(prog)s /caminho/notas ./saida.txt 20260201 20260210     # Do dia 20260201 até 20260210
        """
    )

    # Argumentos posicionais obrigatórios conforme solicitado
    parser.add_argument('base_path',
                       help='Caminho base das notas (ex: /home/usuario/Obsidian/Diario)')
    parser.add_argument('output',
                       help='Caminho completo do arquivo de saída (ex: ~/Downloads/consolidado.txt)')
    parser.add_argument('data_inicial',
                       help='Data inicial no formato YYYYMMDD (ex: 20260201)')
    
    # Data final continua sendo opcional, mas posicionada ao final
    parser.add_argument('data_final',
                       nargs='?', # Argumento opcional
                       help='Data final no formato YYYYMMDD (opcional, padrão: hoje)')

    args = parser.parse_args() # Faz o parse dos argumentos

    # Parse e validação das datas
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
        end_date = datetime.now() # Se data_final não for fornecida, usa a data atual

    # Validação adicional: data inicial não pode ser posterior à final
    if start_date > end_date:
        print("Erro: Data inicial não pode ser posterior à data final", file=sys.stderr)
        sys.exit(1)

    # Verifica se o diretório base das notas existe
    if not os.path.isdir(args.base_path):
        print(f"Erro: Diretório base não encontrado: {args.base_path}", file=sys.stderr)
        sys.exit(1)

    # Gera a lista de todas as datas a serem processadas
    dates = generate_date_range(start_date, end_date)

    print(f"Processando {len(dates)} dias de {start_date.strftime('%Y-%m-%d')} a {end_date.strftime('%Y-%m-%d')}...")

    # Itera sobre cada data para extrair e formatar as entradas
    entries = []
    files_found = 0
    files_missing = 0

    for date in dates:
        file_path = get_file_path(args.base_path, date)
        frontmatter = extract_frontmatter(file_path)

        if frontmatter is not None: # Se o arquivo foi encontrado e processado (mesmo que sem frontmatter)
            files_found += 1
            entry = format_entry(date, frontmatter)
            entries.append(entry)
        else: # Se o arquivo não foi encontrado ou houve erro na leitura
            files_missing += 1
            print(f"  Aviso: Arquivo não encontrado ou vazio: {file_path}", file=sys.stderr)

    # Salva o arquivo consolidado final
    try:
        output_path = os.path.expanduser(args.output)
        os.makedirs(os.path.dirname(output_path), exist_ok=True) # Cria diretórios se não existirem

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(entries)) # Escreve todas as entradas separadas por duas quebras de linha

        print(f"\n✓ Consolidado gerado com sucesso!")
        print(f"  Arquivo: {output_path}")
        print(f"  Arquivos processados: {files_found}")
        print(f"  Arquivos não encontrados: {files_missing}")

    except Exception as e:
        print(f"Erro ao salvar arquivo: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main() # Garante que main() seja chamada apenas quando o script é executado diretamente
