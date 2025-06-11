# Static Checker — Projeto de Compiladores (UCSal 2025.1)

Este é o repositório do projeto da disciplina **Compiladores** da Universidade Católica do Salvador (UCSal), semestre 2025.1. O objetivo do projeto é desenvolver um **Static Checker** para a linguagem fictícia **CangaCode2025-1**, definida pelo professor Osvaldo Requião.

---

## 📌 Objetivo

Construir um programa em Python capaz de:
- Realizar **análise léxica** sobre arquivos `.251` escritos na linguagem CangaCode2025-1
- Armazenar **identificadores** em uma tabela de símbolos
- Gerar dois relatórios de saída: `.LEX` (tokens) e `.TAB` (símbolos)

---

## 🛠️ Tecnologias Utilizadas

- Linguagem: **Python 3.12**
- Biblioteca principal: [PLY (Python Lex-Yacc)](https://www.dabeaz.com/ply/)
- Editor recomendado: **PyCharm**
- Empacotamento: **PyInstaller**

---

## 📁 Estrutura do Projeto

```
mini-static-analyzer/
├── main.py                    # Arquivo principal
├── lexer/lexer.py             # Analisador léxico
├── parser/parser.py           # (Em breve) Analisador sintático
├── symbol_table/table.py      # Tabela de símbolos
├── output/                    # Relatórios .LEX e .TAB
├── tests/                     # Arquivos de teste (.251)
├── requirements.txt           # Dependências
└── dist/CangaCodeChecker.exe  # Executável gerado (opcional)
```

---

## ▶️ Como Executar

### 💻 Opção 1: Usando o Código Python

1. Instale as dependências:

```bash
pip install -r requirements.txt
```

2. Execute o analisador (sem extensão `.251`):

```bash
python main.py <nome_do_arquivo>
```

Exemplo:

```bash
python main.py MeuPrograma
```

---

### 🪟 Opção 2: Executável para Windows

1. Compile o executável (ou baixe, se já estiver disponível):

```bash
pip install pyinstaller
pyinstaller --onefile --name="CangaCodeChecker" main.py
```

2. Use da seguinte forma:

```cmd
CangaCodeChecker.exe MeuPrograma
```

O programa irá procurar automaticamente `MeuPrograma.251` no diretório atual e gerar:

- `MeuPrograma.LEX`
- `MeuPrograma.TAB`

---

## 📄 Arquivo de Entrada (.251)

Exemplo:

```
program MeuPrograma
declarations
    varType integer: x, y;
    varType real: resultado;
endDeclarations
functions
    funcType void: calcular()
        x := 10;
        y := 20;
        resultado := x + y;
    endFunction;
endFunctions
endProgram
```

---

## 🧾 Arquivos Gerados

### 🔸 `<nome>.LEX`
Relatório da análise léxica:

```
Lexeme: program, Código: 01, ÍndiceTabSimb: -, Linha: 1  
Lexeme: MeuPrograma, Código: 02, ÍndiceTabSimb: 1, Linha: 1  
...
```

### 🔸 `<nome>.TAB`
Tabela de símbolos:

```
Entrada: 1, Codigo: 02, Lexeme: MeuPrograma, Tipo: --, Linhas: [1]  
Entrada: 2, Codigo: 25, Lexeme: x, Tipo: IN, Linhas: [3, 6]  
...
```

---

## ⚠️ Tratamento de Erros

| Código | Descrição                        |
|--------|----------------------------------|
| 0      | Sucesso                          |
| 1      | Arquivo não encontrado           |
| 2      | Permissão negada                 |
| 3      | Erro interno                     |

Erros comuns:
- Arquivo `.251` não encontrado
- Caminho incorreto ou sem permissão
- Comentários ou caracteres inválidos são ignorados

---

## 📦 Requisitos

- Python 3.8+
- `requirements.txt`:

```txt
ply==3.11
```

Instale com:

```bash
pip install -r requirements.txt
```

---

## 👨‍💻 Suporte

- Verifique exemplos em `/tests`
- Documentação gerada automaticamente
- Em caso de dúvidas, entre em contato com a equipe de desenvolvimento