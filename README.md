# Static Checker — Projeto de Compiladores (UCSal 2025.1)

Este é o repositório do projeto da disciplina **Compiladores** da Universidade Católica do Salvador (UCSal), semestre 2025.1. O objetivo do projeto é desenvolver um **Static Checker** para a linguagem fictícia **CangaCode2025-1**, definida pelo professor Osvaldo Requião.

---

## 📌 Objetivo

Construir um programa em Python capaz de:
- Realizar análise léxica sobre arquivos `.251` escritos na linguagem CangaCode2025-1
- Armazenar identificadores em uma tabela de símbolos
- Gerar dois relatórios de saída: `.LEX` (análise léxica) e `.TAB` (tabela de símbolos)

---

## 🛠️ Tecnologias utilizadas

- Linguagem: Python 3.12
- Ferramentas: [PLY (Python Lex-Yacc)](https://www.dabeaz.com/ply/)
- Editor recomendado: PyCharm

---

## 📁 Estrutura do projeto

```
mini-static-analyzer/
├── main.py # Arquivo principal (executável)
├── lexer/lexer.py # Implementação do analisador léxico
├── parser/parser.py # (Em breve) Analisador sintático parcial
├── symbol_table/table.py # Implementação da tabela de símbolos
├── output/ # Relatórios gerados (.LEX e .TAB)
└── tests/ # Arquivos de teste .251
```

---

## ▶️ Como executar

1. Instale as dependências:

```bash
pip install ply
```

2. Execute o programa passando o nome do arquivo .251 (sem extensão):

```bash
python main.py
```

Exemplo de estrutura dentro da pasta tests/:

```
tests/
└── exemplo1.251
```
##  📄 Entradas e saídas
### ✅ Entrada:
- Um arquivo com extensão .251, escrito em CangaCode2025-1

### 🧾 Saídas:
- nome_do_arquivo.LEX: Relatório da análise léxica

- nome_do_arquivo.TAB: Tabela de símbolos
