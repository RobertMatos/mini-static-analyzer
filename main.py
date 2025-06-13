#!/usr/bin/env python3
"""
Programa Principal do Static Checker CangaCode2025-1
Universidade Católica do Salvador - UCSal

Este é o ponto de entrada principal do Static Checker.
Demonstra o uso correto das classes corrigidas.
"""

import sys
import os
from pathlib import Path

# Adicionar o diretório atual ao path para imports
sys.path.insert(0, str(Path(__file__).parent))

from parser.parser import Parser


def create_test_file():
    """
    Cria um arquivo de teste para demonstrar o funcionamento.
    """
    test_content = """program meuPrograma
declarations
    vartype integer: contador, limite, resultado
    vartype real: media, soma, valor
    vartype string: nome, mensagem
    vartype boolean: encontrado, finalizado
endDeclarations

functions
    functype integer: calcularSoma(paramtype integer: a, b)
        vartype integer: temp
        temp := a + b
        return temp
    endFunction

    functype real: calcularMedia(paramtype real: x, y, z)
        vartype real: resultado
        resultado := (x + y + z) / 3.0
        return resultado
    endFunction

    functype void: imprimirResultado(paramtype string: texto)
        print texto
    endFunction
endFunctions

endProgram
"""

    with open('teste.251', 'w', encoding='utf-8') as f:
        f.write(test_content)

    print("Arquivo de teste 'teste.251' criado com sucesso!")
    return 'teste.251'


def main():
    """
    Função principal do programa.
    """
    print("=" * 60)
    print("STATIC CHECKER CANGACODE2025-1")
    print("Universidade Católica do Salvador - UCSal")
    print("=" * 60)

    # Verificar argumentos
    if len(sys.argv) != 2:
        print("Uso: python main.py <arquivo.251>")
        print("Ou: python main.py teste (para criar arquivo de teste)")
        sys.exit(1)

    filename = sys.argv[1]

    # Se o argumento for 'teste', criar arquivo de teste
    if filename.lower() == 'teste':
        filename = create_test_file()

    try:
        # Inicializar o parser
        print(f"Inicializando análise do arquivo: {filename}")
        parser = Parser(filename)

        # Executar análise
        print("Executando análise léxica...")
        success = parser.analyze()

        if success:
            print("✓ Análise léxica concluída com sucesso!")

            # Gerar relatórios
            print("Gerando relatórios...")
            parser.generate_reports()

            # Exibir estatísticas
            stats = parser.get_statistics()
            print("\n" + "=" * 40)
            print("ESTATÍSTICAS DA ANÁLISE:")
            print("=" * 40)
            print(f"Tokens processados: {stats['total_tokens']}")
            print(f"Símbolos na tabela: {stats['total_symbols']}")
            print(f"Linhas processadas: {stats['total_lines']}")
            print(f"Escopos processados: {stats['scopes_processed']}")

            # Exibir informações dos arquivos gerados
            base_name = Path(filename).stem
            directory = Path(filename).parent

            lex_file = directory / f"{base_name}.LEX"
            tab_file = directory / f"{base_name}.TAB"

            print("\n" + "=" * 40)
            print("ARQUIVOS GERADOS:")
            print("=" * 40)
            print(f"Relatório léxico: {lex_file}")
            print(f"Tabela de símbolos: {tab_file}")

            # Mostrar preview dos arquivos se forem pequenos
            print("\n" + "=" * 40)
            print("PREVIEW DO ARQUIVO .TAB:")
            print("=" * 40)
            try:
                with open(tab_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')
                    # Mostrar apenas as primeiras 30 linhas
                    for i, line in enumerate(lines[:30]):
                        print(line)
                    if len(lines) > 30:
                        print(f"... (mais {len(lines) - 30} linhas)")
            except Exception as e:
                print(f"Erro ao ler arquivo .TAB: {e}")

            print("\n✓ Análise concluída com sucesso!")
            sys.exit(0)

        else:
            print("✗ Análise falhou!")
            sys.exit(1)

    except FileNotFoundError:
        print(f"✗ Erro: Arquivo '{filename}' não encontrado!")
        print("Certifique-se de que o arquivo existe e tem a extensão .251")
        sys.exit(1)

    except Exception as e:
        print(f"✗ Erro fatal durante a análise: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def test_components():
    """
    Testa os componentes individualmente.
    """
    print("=" * 60)
    print("TESTE DOS COMPONENTES INDIVIDUAIS")
    print("=" * 60)

    # Teste do Lexer
    print("\n1. TESTANDO LEXER:")
    print("-" * 30)

    from lexer.lexer import Lexer

    test_code = """program teste
    declarations
        vartype integer: x, y
    endDeclarations
    endProgram"""

    lexer = Lexer(test_code)
    tokens = lexer.tokenize_all()

    print(f"Tokens gerados: {len(tokens)}")
    for i, (code, lexeme, line) in enumerate(tokens[:10]):  # Mostrar primeiros 10
        print(f"  {i + 1}: Código {code}, Lexema '{lexeme}', Linha {line}")
    if len(tokens) > 10:
        print(f"  ... (mais {len(tokens) - 10} tokens)")

    # Teste da Tabela de Símbolos
    print("\n2. TESTANDO TABELA DE SÍMBOLOS:")
    print("-" * 30)

    from symbol_table.table import SymbolTable

    table = SymbolTable()

    # Inserir alguns símbolos
    test_symbols = [
        ("TESTE", 2, 1),
        ("VARIAVEL1", 49, 3),
        ("FUNCAO1", 18, 5)
    ]

    print("Inserindo símbolos de teste:")
    for lexeme, code, line in test_symbols:
        index = table.insert(lexeme, code, line)
        print(f"  '{lexeme}' inserido no índice {index}")

    print(f"\nTotal de símbolos: {table.get_symbol_count()}")

    # Teste de busca
    print("\nTeste de busca:")
    for lexeme in ["TESTE", "variavel1", "INEXISTENTE"]:
        result = table.lookup(lexeme)
        print(f"  Busca '{lexeme}': {result}")


if __name__ == "__main__":
    # Se chamado com argumento 'test', executar testes
    if len(sys.argv) == 2 and sys.argv[1].lower() == 'test':
        test_components()
    else:
        main()