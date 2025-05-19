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
    print (
        "Código da Equipe: EQ03\n"
        "Componentes:\n"
            "   Gabriel de Abreu Farias Azevedo;  gabriel.azevedo@ucsal.edu.br;	\n"
            "   Rebeca Bezerra Gonçalves dos Santos;  rebecabezerra.santos@ucsal.edu.br; \n"
            "   Sarah Evellyn Ferreira Nogueira;  sarahevellyn.nogueira@ucsal.edu.br; \n"
            "   Robert Valadares de Matos;  robert.matos@ucsal.edu.br; \n"
    )
    print("Tokens reconhecidos:\n")
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(f"| Linha {tok.lineno} | Tipo: {tok.type} | Valor: {tok.value}")

if __name__ == "__main__":
    main()
