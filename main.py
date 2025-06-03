import sys
import os
from lexer.lexer import build_lexer
from symbol_table.table import SymbolTable

def gerar_tab_file(filepath: str, symbol_table: SymbolTable):
    base = os.path.splitext(os.path.basename(filepath))[0]
    tab_path = os.path.join("output", f"{base}.TAB")
    os.makedirs("output", exist_ok=True)

    with open(tab_path, "w") as f:
        f.write("RELATÓRIO DA TABELA DE SÍMBOLOS\n")
        f.write(f"Arquivo analisado: {filepath}\n\n")

        for symbol in symbol_table.get_all():
            f.write(f"Index: {symbol.index}\n")
            f.write(f"Atom Code: {symbol.atom_code}\n")
            f.write(f"Lexeme: {symbol.lexeme}\n")
            f.write(f"Tamanho original: {symbol.full_length}\n")
            f.write(f"Tamanho truncado: {symbol.truncated_length}\n")
            f.write(f"Tipo: {symbol.symbol_type or 'N/A'}\n")
            f.write(f"Linhas: {', '.join(map(str, symbol.lines))}\n")
            f.write("-" * 40 + "\n")

def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py NomeDoArquivo (sem .251)")
        return

    filename = sys.argv[1]
    filepath = filename if filename.endswith(".251") else f"{filename}.251"

    if not os.path.isfile(filepath):
        print(f"Arquivo '{filepath}' não encontrado.")
        return

    with open(filepath, "r") as f:
        data = f.read()

    symbol_table = SymbolTable()
    lexer = build_lexer(symbol_table=symbol_table)

    lexer.input(data)

    while True:
        tok = lexer.token()
        if not tok:
            break

    gerar_tab_file(filepath, symbol_table)

if __name__ == "__main__":
    main()
