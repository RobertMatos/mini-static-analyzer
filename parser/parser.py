"""
Parser/Controller Principal do Static Checker CangaCode2025-1
Universidade Católica do Salvador - UCSal
Bacharelado em Engenharia de Software
Disciplina: Compiladores - Professor Osvaldo Requião Melo

Este módulo implementa o controlador principal do Static Checker seguindo
o padrão syntax-driven compiler. Coordena as chamadas ao analisador léxico
e gerencia a tabela de símbolos.
"""

import os
from pathlib import Path
from typing import List, Tuple, Optional, Dict
from lexer.lexer import Lexer
from symbol_table.table import SymbolTable


class Parser:
    """
    Controlador principal do Static Checker.

    Responsabilidades:
    - Atuar como programa principal do compilador (syntax-driven)
    - Gerenciar inicialização de todas as estruturas
    - Controlar escopo durante análise
    - Coordenar chamadas ao analisador léxico
    - Gerar relatórios de saída (.LEX e .TAB)
    """

    def __init__(self, filename: str):
        """
        Inicializa o parser com o arquivo fonte.

        Args:
            filename: Caminho para o arquivo .251 (com ou sem extensão)
        """
        self.filename = self._validate_filename(filename)
        self.base_name = Path(self.filename).stem
        self.directory = Path(self.filename).parent

        # Componentes principais
        self.lexer: Optional[Lexer] = None
        self.symbol_table = SymbolTable()

        # Controle de análise
        self.current_line = 1
        self.current_position = 0
        self.tokens_found: List[Tuple[str, int, Optional[int], int]] = []

        # Códigos de átomos que representam identificadores
        self.identifier_codes = {2, 18, 49}  # PROGRAMNAME, FUNCTYPE/FUNCTIONNAME, VARIABLE

        # Controle de escopo (preparado para expansão futura)
        self.scope_stack = ['global']
        self.current_scope = 'global'

        # Status da análise
        self.analysis_success = False

    def _validate_filename(self, filename: str) -> str:
        """
        Valida e ajusta o nome do arquivo de entrada.

        Args:
            filename: Nome do arquivo fornecido

        Returns:
            Caminho completo do arquivo .251

        Raises:
            FileNotFoundError: Se o arquivo não for encontrado
        """
        # Se não tem extensão, adiciona .251
        if not filename.endswith('.251'):
            filename += '.251'

        # Converte para Path para manipulação
        file_path = Path(filename)

        # Se é apenas nome do arquivo, procura no diretório corrente
        if not file_path.is_absolute() and len(file_path.parts) == 1:
            file_path = Path.cwd() / file_path

        # Verifica se o arquivo existe
        if not file_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

        return str(file_path)

    def analyze(self) -> bool:
        """
        Executa a análise completa do arquivo fonte.

        Returns:
            True se a análise foi bem-sucedida, False caso contrário
        """
        try:
            # 1. Abrir e ler o arquivo fonte
            with open(self.filename, 'r', encoding='ascii', errors='ignore') as file:
                source_code = file.read()

            # 2. Inicializar o analisador léxico
            self.lexer = Lexer(source_code)

            # 3. Inicializar estruturas de dados
            self.symbol_table.initialize()
            self.tokens_found = []
            self.current_line = 1

            print(f"Iniciando análise do arquivo: {self.filename}")

            # 4. Loop principal de análise
            self._main_analysis_loop()

            self.analysis_success = True
            print(f"Análise concluída com sucesso!")
            return True

        except FileNotFoundError as e:
            print(f"Erro: {e}")
            return False
        except Exception as e:
            print(f"Erro durante análise: {e}")
            return False

    def _main_analysis_loop(self):
        """
        Loop principal de análise: chama o lexer até EOF.
        """
        token_count = 0
        identifier_count = 0

        while True:
            try:
                # Obter próximo token do lexer
                token_result = self.lexer.next_token()

                if token_result is None:  # EOF
                    break

                token_code, lexeme, line_number = token_result
                token_count += 1

                # Atualizar linha atual
                if line_number > self.current_line:
                    self.current_line = line_number

                # Processar o token
                symbol_table_index = self._process_token(lexeme, token_code, line_number)

                if symbol_table_index is not None:
                    identifier_count += 1
                    print(f"DEBUG: Identificador inserido - Lexema: '{lexeme}', Código: {token_code}, Índice: {symbol_table_index}")

                # Armazenar informações para o relatório .LEX
                self.tokens_found.append((lexeme, token_code, symbol_table_index, line_number))

            except Exception as e:
                print(f"Erro ao processar token na linha {self.current_line}: {e}")
                continue

        print(f"Total de tokens processados: {token_count}")
        print(f"Total de identificadores inseridos na tabela: {identifier_count}")

    def _process_token(self, lexeme: str, token_code: int, line_number: int) -> Optional[int]:
        """
        Processa um token individual.

        Args:
            lexeme: O texto do token
            token_code: Código do átomo
            line_number: Linha onde foi encontrado

        Returns:
            Índice na tabela de símbolos (se aplicável) ou None
        """
        # Verificar se é um identificador (codes 2, 18, 49)
        if token_code in self.identifier_codes:
            print(f"DEBUG: Processando identificador - Lexema: '{lexeme}', Código: {token_code}, Linha: {line_number}")

            # Inserir na tabela de símbolos
            symbol_index = self.symbol_table.insert(lexeme, token_code, line_number)
            print(f"DEBUG: Identificador '{lexeme}' inserido com índice {symbol_index}")
            return symbol_index

        # Palavras reservadas, constantes e operadores não vão para tabela de símbolos
        return None

    def _update_scope_control(self, lexeme: str, token_code: int):
        """
        Atualiza o controle de escopo (preparado para expansão futura).

        Args:
            lexeme: Texto do token
            token_code: Código do átomo
        """
        # Controle básico de escopo - expandir no futuro
        if lexeme.upper() == 'FUNCTIONS':
            self._enter_scope('functions')
        elif lexeme.upper() == 'ENDFUNCTIONS':
            self._exit_scope()
        elif token_code == 18:  # functionName
            self._enter_scope(f'function_{lexeme}')
        elif lexeme.upper() == 'ENDFUNCTION':
            self._exit_scope()

    def _enter_scope(self, scope_name: str):
        """
        Entra em um novo escopo.

        Args:
            scope_name: Nome do escopo
        """
        self.scope_stack.append(scope_name)
        self.current_scope = scope_name

    def _exit_scope(self):
        """
        Sai do escopo atual.
        """
        if len(self.scope_stack) > 1:
            self.scope_stack.pop()
            self.current_scope = self.scope_stack[-1]

    def generate_reports(self):
        """
        Gera os relatórios .LEX e .TAB na mesma pasta do arquivo fonte.
        """
        try:
            self._generate_lex_report()
            self._generate_tab_report()
            print("Relatórios gerados com sucesso!")
        except Exception as e:
            print(f"Erro ao gerar relatórios: {e}")
            raise

    def _generate_lex_report(self):
        """
        Gera o relatório da análise léxica (.LEX).
        """
        lex_filename = self.directory / f"{self.base_name}.LEX"

        with open(lex_filename, 'w', encoding='utf-8') as file:
            # Cabeçalho
            file.write("=" * 60 + "\n")
            file.write("RELATÓRIO DA ANÁLISE LÉXICA\n")
            file.write("=" * 60 + "\n")
            file.write(f"Arquivo analisado: {self.base_name}.251\n")
            file.write("Equipe: [CÓDIGO_DA_EQUIPE]\n")
            file.write("Integrantes:\n")
            file.write("  - [NOME] - [EMAIL] - [TELEFONE]\n")
            file.write("  - [NOME] - [EMAIL] - [TELEFONE]\n")
            file.write("=" * 60 + "\n\n")

            # Dados dos tokens
            file.write("TOKENS ENCONTRADOS:\n")
            file.write("-" * 60 + "\n")
            file.write(f"{'Lexeme':<20} {'Código':<8} {'ÍndiceTabSimb':<12} {'Linha':<6}\n")
            file.write("-" * 60 + "\n")

            for lexeme, token_code, symbol_index, line_number in self.tokens_found:
                symbol_idx_str = str(symbol_index) if symbol_index is not None else "-"
                file.write(f"{lexeme:<20} {token_code:<8} {symbol_idx_str:<12} {line_number:<6}\n")

            file.write("-" * 60 + "\n")
            file.write(f"Total de tokens: {len(self.tokens_found)}\n")

            # Estatísticas adicionais
            identifiers_count = sum(1 for _, _, symbol_index, _ in self.tokens_found if symbol_index is not None)
            file.write(f"Total de identificadores: {identifiers_count}\n")

    def _generate_tab_report(self):
        """
        Gera o relatório da tabela de símbolos (.TAB).
        """
        tab_filename = self.directory / f"{self.base_name}.TAB"

        with open(tab_filename, 'w', encoding='utf-8') as file:
            # Cabeçalho
            file.write("=" * 80 + "\n")
            file.write("RELATÓRIO DA TABELA DE SÍMBOLOS\n")
            file.write("=" * 80 + "\n")
            file.write(f"Arquivo analisado: {self.base_name}.251\n")
            file.write("Equipe: [CÓDIGO_DA_EQUIPE]\n")
            file.write("Integrantes:\n")
            file.write("  - [NOME] - [EMAIL] - [TELEFONE]\n")
            file.write("  - [NOME] - [EMAIL] - [TELEFONE]\n")
            file.write("=" * 80 + "\n\n")

            # Usar método da tabela de símbolos para gerar conteúdo
            symbol_content = self.symbol_table.generate_report_content(self.base_name)

            # Dividir o conteúdo em linhas e escrever no arquivo
            lines = symbol_content.split('\n')
            # Pular as primeiras linhas (cabeçalho duplicado)
            content_started = False
            for line in lines:
                if line.startswith('Entrada:') or content_started or 'símbolo' in line.lower():
                    content_started = True
                    file.write(line + '\n')

    def get_analysis_status(self) -> bool:
        """
        Retorna o status da análise.

        Returns:
            True se a análise foi bem-sucedida
        """
        return self.analysis_success

    def get_statistics(self) -> Dict[str, int]:
        """
        Retorna estatísticas da análise.

        Returns:
            Dicionário com estatísticas
        """
        return {
            'total_tokens': len(self.tokens_found),
            'total_symbols': self.symbol_table.get_symbol_count(),
            'total_lines': self.current_line,
            'scopes_processed': len(self.scope_stack)
        }


# Exemplo de uso e teste
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Uso: python parser.py <nome_do_arquivo>")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        parser = Parser(filename)
        success = parser.analyze()

        if success:
            parser.generate_reports()
            stats = parser.get_statistics()
            print(f"\nEstatísticas da análise:")
            print(f"  Tokens processados: {stats['total_tokens']}")
            print(f"  Símbolos na tabela: {stats['total_symbols']}")
            print(f"  Total de linhas: {stats['total_lines']}")
            sys.exit(0)
        else:
            print("Análise falhou!")
            sys.exit(1)

    except Exception as e:
        print(f"Erro fatal: {e}")
        sys.exit(1)