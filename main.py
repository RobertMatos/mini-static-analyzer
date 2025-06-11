#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Static Checker CangaCode2025-1
Programa Principal - main.py

Universidade Católica do Salvador - UCSal
Bacharelado em Engenharia de Software
Disciplina: Compiladores
Professor: Osvaldo Requião Melo

Este módulo implementa o ponto de entrada principal do Static Checker
para a linguagem CangaCode2025-1, seguindo a arquitetura syntax-driven compiler.
"""

import sys
import os
from pathlib import Path

# Importação do parser que atua como controlador principal
try:
    from parser.parser import Parser
except ImportError as e:
    print(f"Erro: Não foi possível importar o módulo parser: {e}")
    print("Verifique se o arquivo parser/parser.py existe e está implementado.")
    sys.exit(1)


def print_usage():
    """
    Exibe instruções de uso do programa.
    """
    program_name = os.path.basename(sys.argv[0])
    print(f"Uso: {program_name} <nome_arquivo>")
    print()
    print("Parâmetros:")
    print("  nome_arquivo    Nome do arquivo fonte (sem extensão .251)")
    print("                  Pode ser apenas o nome (busca no diretório atual)")
    print("                  ou caminho completo para o arquivo")
    print()
    print("Exemplos:")
    print(f"  {program_name} exemplo")
    print(f"  {program_name} /caminho/para/exemplo")
    print(f"  {program_name} ./testes/exemplo")
    print()
    print("Nota: O programa procurará automaticamente pelo arquivo com extensão .251")


def validate_and_get_filepath(filename_arg):
    """
    Valida e obtém o caminho completo do arquivo .251 a ser analisado.

    Args:
        filename_arg (str): Argumento fornecido pelo usuário

    Returns:
        str: Caminho completo para o arquivo .251

    Raises:
        FileNotFoundError: Se o arquivo não for encontrado
        ValueError: Se o argumento for inválido
    """
    if not filename_arg or filename_arg.strip() == "":
        raise ValueError("Nome do arquivo não pode estar vazio")

    # Remove espaços em branco
    filename_arg = filename_arg.strip()

    # Se o usuário forneceu extensão .251, remove para padronizar
    if filename_arg.lower().endswith('.251'):
        filename_arg = filename_arg[:-4]

    # Adiciona a extensão .251
    filepath = filename_arg + '.251'

    # Converte para Path para manipulação mais robusta
    file_path = Path(filepath)

    # Se é um caminho absoluto ou relativo com diretórios
    if file_path.is_absolute() or '/' in filepath or '\\' in filepath:
        target_file = file_path
    else:
        # Se é apenas um nome, procura no diretório atual
        target_file = Path.cwd() / filepath

    # Verifica se o arquivo existe
    if not target_file.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {target_file}")

    # Verifica se é um arquivo (não diretório)
    if not target_file.is_file():
        raise ValueError(f"O caminho especificado não é um arquivo válido: {target_file}")

    return str(target_file.resolve())


def main():
    """
    Função principal do Static Checker CangaCode2025-1.

    Responsabilidades:
    - Processar argumentos da linha de comando
    - Validar arquivo de entrada (.251)
    - Instanciar e coordenar o parser
    - Gerenciar fluxo de execução geral
    - Tratar erros e garantir limpeza de recursos

    Returns:
        int: Código de retorno (0 para sucesso, 1 para erro)
    """

    print("=" * 60)
    print("Static Checker CangaCode2025-1")
    print("Universidade Católica do Salvador - UCSal")
    print("=" * 60)

    try:
        # 1. PROCESSAR ARGUMENTOS DA LINHA DE COMANDO
        if len(sys.argv) != 2:
            print("Erro: Número incorreto de argumentos.")
            print()
            print_usage()
            return 1

        filename_arg = sys.argv[1]

        # Verifica se o usuário pediu ajuda
        if filename_arg.lower() in ['-h', '--help', 'help', '/?']:
            print_usage()
            return 0

        print(f"Processando arquivo: {filename_arg}")

        # 2. VALIDAR ARQUIVO .251
        try:
            source_filepath = validate_and_get_filepath(filename_arg)
            print(f"Arquivo encontrado: {source_filepath}")
        except (FileNotFoundError, ValueError) as e:
            print(f"Erro na validação do arquivo: {e}")
            return 1

        # 3. INSTANCIAR O PARSER (CONTROLADOR PRINCIPAL)
        print("Inicializando analisador...")
        try:
            parser = Parser(source_filepath)
        except Exception as e:
            print(f"Erro ao inicializar o parser: {e}")
            return 1

        # 4. EXECUTAR ANÁLISE
        print("Iniciando análise léxica...")
        try:
            parser.analyze()
            print("Análise léxica concluída com sucesso!")

            # Gerar relatórios
            print("Gerando relatórios...")
            parser.generate_reports()
            print("Relatórios gerados com sucesso!")

            # Informar localização dos arquivos gerados
            base_name = Path(source_filepath).stem
            output_dir = Path(source_filepath).parent
            lex_file = output_dir / f"{base_name}.LEX"
            tab_file = output_dir / f"{base_name}.TAB"

            print()
            print("Arquivos gerados:")
            print(f"  - Relatório da análise léxica: {lex_file}")
            print(f"  - Relatório da tabela de símbolos: {tab_file}")

        except Exception as e:
            print(f"Erro durante a análise: {e}")
            return 1

        print()
        print("=" * 60)
        print("Processamento concluído com sucesso!")
        print("=" * 60)

        return 0

    except KeyboardInterrupt:
        print("\nOperação interrompida pelo usuário.")
        return 1

    except Exception as e:
        print(f"Erro inesperado: {e}")
        print("Por favor, verifique os arquivos de entrada e tente novamente.")
        return 1

    finally:
        # 5. GARANTIR LIMPEZA DE RECURSOS
        # Aqui poderia haver limpeza de recursos se necessário
        # Por enquanto, apenas uma mensagem de debug se necessário
        pass


if __name__ == "__main__":
    # Configura a codificação para UTF-8 se disponível
    try:
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')
        if hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

    # Executa o programa principal e retorna o código de saída
    exit_code = main()
    sys.exit(exit_code)