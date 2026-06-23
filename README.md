# consolidador-diario-obsidian-python

**Breve descrição:** Um script Python para consolidar métricas e informações de notas diárias do Obsidian, extraindo dados do frontmatter e gerando um arquivo de texto unificado.

## Visão Geral

Este repositório contém um script Python (`consolida_diario.py`) projetado para automatizar a consolidação de informações de suas notas diárias do Obsidian. Ele extrai dados estruturados (frontmatter YAML) de arquivos Markdown de diário, organizados por data, e os compila em um único arquivo de texto. Isso é particularmente útil para análise de tendências, revisão periódica ou simplesmente para ter um backup consolidado de suas métricas e reflexões diárias.

## Funcionalidades

*   **Extração de Frontmatter:** Lê e interpreta o bloco de frontmatter (metadados YAML) de cada nota diária.
*   **Organização por Data:** Processa notas dentro de um intervalo de datas especificado, seguindo a estrutura de pastas `YYYY/MM/YYYYMMDD.md` comum em diários do Obsidian.
*   **Saída Consolidada:** Gera um arquivo de texto único com todas as entradas formatadas, incluindo a data e os campos do frontmatter.
*   **Flexibilidade:** Permite especificar o caminho base das notas e o arquivo de saída, além de um intervalo de datas customizável.
*   **Tratamento de Erros:** Inclui validações para datas e caminhos de arquivo, além de avisos para notas não encontradas.

## Como Usar

### Pré-requisitos

*   Python 3.x instalado.
*   Suas notas diárias do Obsidian organizadas em uma estrutura de pastas `YYYY/MM/YYYYMMDD.md` dentro de um diretório base.

### Instalação

1.  Clone este repositório para sua máquina local:
    ```bash
    git clone https://github.com/seu-usuario/consolidador-diario-obsidian-python.git
    cd consolidador-diario-obsidian-python
    ```
2.  O script não possui dependências externas além das bibliotecas padrão do Python.

### Execução

O script é executado via linha de comando e aceita os seguintes argumentos:

```bash
python3 consolida_diario.py <data_inicial> [data_final] [--base-path <caminho>] [--output <arquivo_saida>]
```

**Argumentos:**

*   `<data_inicial>`: **Obrigatório.** A data de início do período a ser consolidado, no formato `YYYYMMDD` (ex: `20260201`).
*   `[data_final]`: **Opcional.** A data de término do período, também no formato `YYYYMMDD`. Se omitida, o script consolidará as notas da `data_inicial` até a data atual.
*   `--base-path <caminho>`: **Opcional.** O caminho absoluto para o diretório raiz onde suas notas diárias do Obsidian estão armazenadas. O padrão é `/home/arthur/storage_02/Backup_USB2/Backup_Obsidian/Cofre_02/05-Diario`.
*   `--output <arquivo_saida>`: **Opcional.** O caminho e nome do arquivo onde o resultado consolidado será salvo. O padrão é `~/Downloads/00-Arquivo-EMM/consolidado_diario.txt`.

**Exemplos:**

*   Consolidar notas de 1º de fevereiro de 2026 até hoje:
    ```bash
    python3 consolida_diario.py 20260201
    ```
*   Consolidar notas de 1º de fevereiro de 2026 até 10 de fevereiro de 2026:
    ```bash
    python3 consolida_diario.py 20260201 20260210
    ```
*   Consolidar notas de um caminho base diferente e salvar em um arquivo específico:
    ```bash
    python3 consolida_diario.py 20260101 20260131 --base-path "/caminho/para/meu/cofre/diario" --output "./consolidado_janeiro.txt"
    ```

## Estrutura do Código

O script é modular e consiste nas seguintes funções principais:

### `parse_date(date_str)`

*   **Propósito:** Converte uma string de data no formato `YYYYMMDD` para um objeto `datetime` do Python.
*   **Detalhes:** Essencial para validar e padronizar as datas de entrada fornecidas pelo usuário. Lança um `ValueError` se o formato da data for inválido.

### `get_file_path(base_path, date_obj)`

*   **Propósito:** Constrói o caminho completo para um arquivo de nota diária do Obsidian, dado o caminho base e um objeto `datetime`.
*   **Detalhes:** Segue a convenção de organização de pastas `YYYY/MM/YYYYMMDD.md` para localizar as notas.

### `extract_frontmatter(file_path)`

*   **Propósito:** Lê um arquivo Markdown e extrai seu bloco de frontmatter YAML.
*   **Detalhes:** Utiliza expressões regulares para encontrar o conteúdo entre os delimitadores `---` no início do arquivo. Analisa cada linha do frontmatter para criar um dicionário `chave: valor`. Retorna `None` se o arquivo não existir ou houver erro, e um dicionário vazio se não houver frontmatter.

### `format_entry(date_obj, frontmatter)`

*   **Propósito:** Formata os dados extraídos de uma nota diária (data e frontmatter) em uma string padronizada para o arquivo de saída.
*   **Detalhes:** Define uma lista fixa de campos esperados (`energia`, `sono`, `humor`, etc.) e os extrai do dicionário `frontmatter`. Campos ausentes são preenchidos com strings vazias para garantir consistência.

### `generate_date_range(start_date, end_date)`

*   **Propósito:** Gera uma lista de objetos `datetime` para cada dia dentro de um intervalo especificado (inclusive).
*   **Detalhes:** Facilita a iteração sobre todas as datas que precisam ser processadas pelo script.

### `main()`

*   **Propósito:** A função principal que orquestra a execução do script.
*   **Detalhes:**
    *   Configura o `ArgumentParser` para lidar com os argumentos de linha de comando (`data_inicial`, `data_final`, `--base-path`, `--output`).
    *   Chama `parse_date` para validar e converter as datas de entrada.
    *   Realiza validações adicionais (data inicial não pode ser posterior à final, caminho base deve existir).
    *   Utiliza `generate_date_range` para obter a lista de datas a processar.
    *   Itera sobre cada data, chamando `get_file_path`, `extract_frontmatter` e `format_entry`.
    *   Acumula as entradas formatadas e as escreve no arquivo de saída especificado.
    *   Fornece feedback ao usuário sobre o progresso e o resultado final, incluindo contagem de arquivos processados e não encontrados.

## Contribuição

Sinta-se à vontade para abrir issues para sugestões ou relatar bugs, ou enviar pull requests com melhorias.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

**Autor:** Arthur Haerdy Jr.