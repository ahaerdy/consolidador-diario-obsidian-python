# 📓 Consolidador de Métricas do Diário Obsidian

Script Python para extrair e consolidar automaticamente os metadados (frontmatter YAML) das notas diárias de um cofre Obsidian em um único arquivo de texto estruturado.

---

## Sumário

- [Contexto e Motivação](#contexto-e-motivação)
- [Como funciona o Daily Notes no Obsidian](#como-funciona-o-daily-notes-no-obsidian)
- [Estrutura esperada das notas](#estrutura-esperada-das-notas)
- [Campos suportados no frontmatter](#campos-suportados-no-frontmatter)
- [Instalação](#instalação)
- [Como usar](#como-usar)
- [Explicação detalhada do código](#explicação-detalhada-do-código)
- [Exemplo de saída](#exemplo-de-saída)
- [Limitações e próximos passos](#limitações-e-próximos-passos)

---

## Contexto e Motivação

O [Obsidian](https://obsidian.md/) é um editor de notas baseado em Markdown com suporte a um sistema de **diário diário (Daily Notes)**, onde cada dia recebe um arquivo `.md` próprio. É comum enriquecer essas notas com um bloco de metadados chamado **frontmatter YAML** — um cabeçalho estruturado no início de cada arquivo que registra métricas pessoais como nível de energia, sono, foco, humor, decisões, insights, entre outros.

O problema: esses dados ficam espalhados em centenas de arquivos. Analisá-los de forma agregada — seja por olhar humano, seja passando para uma IA — exige uma ferramenta de consolidação.

Este script resolve exatamente isso: percorre um intervalo de datas, lê o frontmatter de cada nota diária e gera um único arquivo de texto com todas as entradas formatadas e concatenadas.

---

## Como funciona o Daily Notes no Obsidian

O plugin **Daily Notes** (nativo do Obsidian) cria automaticamente um arquivo Markdown para cada dia. A estrutura de pastas padrão usada por este script é:

```
base_path/
└── 2026/
    ├── 01/
    │   ├── 20260101.md
    │   ├── 20260102.md
    │   └── ...
    └── 02/
        ├── 20260201.md
        └── ...
```

Ou seja: `base_path/YYYY/MM/YYYYMMDD.md`

> Se o seu cofre usar uma estrutura diferente, basta ajustar a função `get_file_path()`.

---

## Estrutura esperada das notas

Cada nota diária deve conter um bloco de frontmatter YAML no início, delimitado por `---`:

```markdown
---
energia: 8
sono: 7
foco: 9
humor: calmo e produtivo
tensao: baixa
corpo: leveza muscular, sem dores
resumo_dia: Dia de foco intenso no projeto principal. Entregas concluídas.
insights: Pausas curtas aumentam consistência mais do que sessões longas.
gratidao: família, saúde, clareza mental
proximo_passo: revisar backlog de tarefas abertas
fase: execução
---

Conteúdo livre da nota...
```

O script extrai apenas o frontmatter — o corpo da nota é ignorado.

---

## Campos suportados no frontmatter

O script reconhece e extrai os seguintes campos, organizados em três blocos temáticos:

### Bloco 1 — Métricas físicas e cognitivas
| Campo | Descrição |
|-------|-----------|
| `energia` | Nível de energia percebido no dia (ex: escala 1–10) |
| `sono` | Qualidade ou duração do sono |
| `foco` | Capacidade de concentração no dia |
| `tensao` | Nível de tensão ou estresse |
| `corpo` | Estado físico geral (dores, disposição, etc.) |

### Bloco 2 — Métricas subjetivas e narrativas
| Campo | Descrição |
|-------|-----------|
| `humor` | Estado emocional dominante |
| `sucessos` | Conquistas ou entregas do dia |
| `desafios` | Obstáculos enfrentados |
| `resumo_dia` | Síntese narrativa do dia |
| `insights` | Aprendizados ou percepções relevantes |
| `gratidao` | Registro de gratidão |
| `proximo_passo` | Próxima ação prioritária |
| `fase` | Fase atual de vida/projeto (ex: planejamento, execução) |
| `detalhamento` | Contexto adicional livre |

### Bloco 3 — Registros estruturados
| Campo | Descrição |
|-------|-----------|
| `hipotese` | Hipótese sendo testada |
| `decisao` | Decisão tomada no dia |
| `marco` | Marco ou conquista significativa |
| `falha` | Registro intencional de falhas para aprendizado |
| `revisao` | Revisão de algo anterior |
| `inventario` | Inventário de recursos, tarefas ou situações |
| `padrao_identificado` | Padrão comportamental ou de resultado observado |
| `questao_aberta` | Pergunta sem resposta ainda |
| `diretriz` | Princípio ou regra pessoal registrada |
| `aviso` | Alerta para si mesmo |
| `sincronicidade` | Coincidências ou eventos notáveis |
| `sonho` | Registro de sonhos |
| `estetica` | Referências visuais, musicais ou artísticas do dia |

> Campos ausentes em uma nota são incluídos na saída como vazios — garantindo formato consistente em todas as entradas.

---

## Instalação

Nenhuma dependência externa necessária. O script usa apenas a biblioteca padrão do Python 3.

**Requisitos:**
- Python 3.7 ou superior

**Clone o repositório:**
```bash
git clone https://github.com/seu-usuario/consolidador-diario-obsidian-python.git
cd consolidador-diario-obsidian-python
```

---

## Como usar

```
python consolida_diario.py <base_path> <output> <data_inicial> [data_final]
```

### Argumentos

| Argumento | Obrigatório | Descrição |
|-----------|-------------|-----------|
| `base_path` | ✅ | Caminho para o diretório raiz das notas diárias |
| `output` | ✅ | Caminho completo para o arquivo de saída (será criado) |
| `data_inicial` | ✅ | Data de início no formato `YYYYMMDD` |
| `data_final` | ❌ | Data de término no formato `YYYYMMDD` (padrão: hoje) |

### Exemplos

```bash
# Consolida do dia 01/02/2026 até hoje
python consolida_diario.py ~/Obsidian/Diario ~/Downloads/consolidado.txt 20260201

# Consolida um intervalo específico
python consolida_diario.py ~/Obsidian/Diario ~/Downloads/jan2026.txt 20260101 20260131

# Consolida apenas um dia
python consolida_diario.py ~/Obsidian/Diario ~/Downloads/hoje.txt 20260623 20260623
```

### Saída esperada no terminal

```
Processando 143 dias de 2026-02-01 a 2026-06-23...
  Aviso: Arquivo não encontrado ou vazio: /home/usuario/Obsidian/Diario/2026/03/20260315.md

✓ Consolidado gerado com sucesso!
  Arquivo: /home/usuario/Downloads/consolidado.txt
  Arquivos processados: 142
  Arquivos não encontrados: 1
```

---

## Explicação detalhada do código

O script está organizado em seis funções com responsabilidades bem separadas:

### `parse_date(date_str)`
Converte uma string no formato `YYYYMMDD` para um objeto `datetime`. Centraliza a validação do formato de data e lança uma exceção clara em caso de erro.

```python
def parse_date(date_str):
    return datetime.strptime(date_str, "%Y%m%d")
```

### `get_file_path(base_path, date_obj)`
Monta o caminho completo do arquivo `.md` para uma data específica, seguindo a estrutura `base_path/YYYY/MM/YYYYMMDD.md`.

```python
def get_file_path(base_path, date_obj):
    year = date_obj.strftime("%Y")
    month = date_obj.strftime("%m")
    filename = date_obj.strftime("%Y%m%d.md")
    return os.path.join(base_path, year, month, filename)
```

### `extract_frontmatter(file_path)`
O coração do script. Lê o arquivo Markdown e usa uma expressão regular com `re.DOTALL` para capturar o bloco entre os dois delimitadores `---`. Em seguida, faz o parse linha a linha, dividindo cada par `chave: valor` em um dicionário Python.

```python
frontmatter_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL | re.MULTILINE)
```

**Retornos possíveis:**
- `None` → arquivo não encontrado ou erro de leitura
- `{}` → arquivo existe mas não tem frontmatter
- `dict` → frontmatter extraído com sucesso

### `format_entry(date_obj, frontmatter)`
Formata a entrada de uma data no padrão de saída. Itera sobre a lista canônica de campos, usando `.get(field, '')` para garantir que campos ausentes apareçam como vazios — e não causem erros. Isso é essencial para compatibilidade retroativa com notas mais antigas que não tinham todos os campos.

### `generate_date_range(start_date, end_date)`
Gera a sequência completa de datas entre `start_date` e `end_date` usando `timedelta(days=1)`. Retorna uma lista de objetos `datetime`.

### `main()`
Função de entrada do script. Usa `argparse` para definir e validar os argumentos de linha de comando, coordena o fluxo de processamento e escreve o arquivo final. Inclui validações de negócio como verificação de datas invertidas e existência do diretório base.

---

## Exemplo de saída

```
Data: 20260201
---
energia: 8
sono: 7
foco: 9
tensao: baixa
corpo: leve, sem queixas
humor: focado e tranquilo
sucessos: entregou PR crítico, fechou 2 tarefas abertas há semanas
desafios: reunião longa consumiu o início da tarde
resumo_dia: Dia produtivo com foco no projeto principal.
insights: blocos de 90min funcionam melhor que sessões abertas
gratidao: saúde, clareza, suporte do time
proximo_passo: revisar backlog e priorizar sprint da semana
fase: execução
detalhamento: 
hipotese: 
decisao: adiar feature X para o próximo ciclo
marco: 
falha: 
revisao: 
inventario: 
padrao_identificado: manhãs com journaling têm mais entrega à tarde
questao_aberta: como reduzir interrupções sem isolar o time?
diretriz: 
aviso: 
sincronicidade: 
sonho: 
estetica: 
---

Data: 20260202
---
...
```

---

## Limitações e próximos passos

- **Parser YAML simples:** o script faz um parse ingênuo (linha a linha com `split(':', 1)`). Valores com `:` na string, listas YAML ou campos multilinha não são suportados. Para casos mais complexos, considere usar a biblioteca `PyYAML`.
- **Sem suporte a campos aninhados:** apenas pares `chave: valor` planos são extraídos.
- **Encoding fixo em UTF-8:** arquivos em outras codificações precisarão de ajuste na função `extract_frontmatter`.

**Melhorias planejadas:**
- [ ] Exportação para CSV (útil para análise em planilhas)
- [ ] Suporte a saída em JSON estruturado
- [ ] Modo de análise estatística básica (médias de energia, sono, foco)
- [ ] Parser YAML robusto com `PyYAML`

---

## Licença

MIT — use, modifique e distribua à vontade.