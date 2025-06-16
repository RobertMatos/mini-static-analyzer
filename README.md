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

- Linguagem: **Python 3.12+**
- Biblioteca principal: [PLY (Python Lex-Yacc)](https://www.dabeaz.com/ply/)
- Editor recomendado: **PyCharm**
- Empacotamento: **PyInstaller**

---

## 📁 Estrutura do Projeto

```
mini-static-analyzer/
├── main.py                    # Arquivo principal
├── lexer/lexer.py             # Analisador léxico
├── parser/parser.py           # Analisador sintático
├── symbol_table/table.py      # Tabela de símbolos
├── tests/                     # Arquivos de teste (.251)
├── requirements.txt           # Dependências
└── dist/CangaCodeChecker.exe  # Executável gerado (opcional)
```

---

## ▶️ Como Executar

### 💻 Opção 1: Usando o Código Python (Via Terminal dentro da pasta do projeto)

1. Crie um ambiente virtual usando o proprio python

    ```bash
    python -m venv .venv
    ```
2. Acesse o ambiente virtual criado
    ```bash
    # Ambiente Windows
    source .\.venv_py\Scripts\activate
    
    # Ambiente Linux
    source .venv/bin/activate
    ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Execute o analisador (sem extensão `.251`):
   ```bash
   python main.py <nome_do_arquivo>
   ```

5. Exemplo:

   ```bash
   python main.py MeuPrograma
   ```

---

### 🪟 Opção 2: Executável para Windows(Execução via terminal...)

1. Compile o executável (ou baixe, se já estiver disponível):
   ```bash
   pyinstaller --onefile --name="CangaCodeChecker" main.py
   ```
   - Arquivo irá ser gerado na pasta dist.
   
2. Use da seguinte forma:

   ```cmd
   # Execução com arquivo .251 (Recomendado está na mesma pasta, caso não... informe o caminho ate o arquivo exemplo a seguir:  "C:\Users\fox\CangaCode\exemplo.251")
   CangaCodeChecker.exe MeuPrograma
      # Execução em ambiente WINDOWS se estiver na pasta principal do projeto
      .\dist\CangaCodeChecker.exe .\tests\exemplo1.251
      
   # Execução teste para verificar se estão ok
   CangaCodeChecker.exe teste
       # Execução em ambiente WINDOWS se estiver na pasta principal do projeto
       .\dist\CangaCodeChecker.exe teste
   ```

O programa irá gerar automaticamente `MeuPrograma.251` no diretório que ele foi especificado (Como tem em /tests o .LEX e .TAB gera lá):

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

## 👨‍💻 Suporte

- Verifique exemplos em `/tests`
- Documentação gerada automaticamente
- Em caso de dúvidas, entre em contato com a equipe de desenvolvimento
