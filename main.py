from lexer.lexer import build_lexer

def main():
    lexer = build_lexer()

    try:
        with open("tests/exemplo1.251", "r") as f:
            data = f.read()
    except FileNotFoundError:
        print("Arquivo de teste não encontrado.")
        return

    lexer.input(data)

    print("Tokens reconhecidos:\n")
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(f"Linha {tok.lineno} | Tipo: {tok.type} | Valor: {tok.value}")

if __name__ == "__main__":
    main()
