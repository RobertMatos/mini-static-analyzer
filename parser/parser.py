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
        self.tokens_found: List[Tuple[str, str, Optional[int], int]] = []

        # CORREÇÃO: Códigos de átomos que representam identificadores (como strings)
        self.identifier_codes = {'ID01', 'ID02', 'ID03'}  # PROGRAMNAME, VARIABLE, FUNCTIONNAME

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

    def _process_token(self, lexeme: str, token_code: str, line_number: int) -> Optional[int]:
        """
        Processa um token individual.

        Args:
            lexeme: O texto do token
            token_code: Código do átomo (string como ID01, ID02, etc.)
            line_number: Linha onde foi encontrado

        Returns:
            Índice na tabela de símbolos (se aplicável) ou None
        """
        # Verificar se é um identificador (codes ID01, ID02, ID03)
        if token_code in self.identifier_codes:
            print(f"DEBUG: Processando identificador - Lexema: '{lexeme}', Código: {token_code}, Linha: {line_number}")

            # CORREÇÃO: Usar código string diretamente (sem conversão para número)
            symbol_index = self.symbol_table.insert(lexeme, token_code, line_number)
            print(f"DEBUG: Identificador '{lexeme}' inserido com índice {symbol_index}")
            return symbol_index

        # Palavras reservadas, constantes e operadores não vão para tabela de símbolos
        return None

    def _update_scope_control(self, lexeme: str, token_code: str):
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
        elif token_code == 'ID03':  # functionName
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
        Gera o relatório da análise léxica (.LEX) conforme exemplo visual fornecido.
        """
        lex_filename = self.directory / f"{self.base_name}.LEX"

        with open(lex_filename, 'w', encoding='utf-8') as file:
            # Cabeçalho fixo conforme imagem
            file.write("Código da Equipe: EQ03\n")
            file.write("Componentes:\n")
            file.write("    Gabriel de Abreu Farias Azevedo; gabriel.azevedo@ucsal.edu.br; (71)99210-5078\n")
            file.write("    Rebeca Bezerra Gonçalves dos Santos; rebecabezerra.santos@ucsal.edu.br; (71)99628-2261\n")
            file.write("    Sarah Evellyn Ferreira Nogueira; sarahevellyn.nogueira@ucsal.edu.br; (71)99675-0337\n")
            file.write("    Robert Valadares de Matos; robert.matos@ucsal.edu.br; (71)98189-1008\n")
            file.write("\n")
            file.write(f"RELATÓRIO DA ANÁLISE LÉXICA. Texto fonte analisado: {self.base_name}.251\n")
            file.write("\n")

            # Tokens encontrados
            for lexeme, token_code, symbol_index, line_number in self.tokens_found:
                lexeme_str = f"Lexeme: {lexeme},"
                code_str = f" Código: {token_code},"
                if symbol_index is not None:
                    index_str = f" ÍndiceTabSimb: {symbol_index},"
                else:
                    index_str = " ÍndiceTabSimb: -,"
                line_str = f" Linha: {line_number}.\n"

                file.write(lexeme_str + code_str + index_str + line_str)

    def _generate_tab_report(self):
        """
        Gera o relatório da tabela de símbolos (.TAB) conforme especificação do exemplo fornecido.
        """
        tab_filename = self.directory / f"{self.base_name}.TAB"

        with open(tab_filename, 'w', encoding='utf-8') as file:
            # Cabeçalho
            file.write("Codigo da Equipe: EQ03\n")
            file.write("Componentes:\n")
            file.write("    Gabriel de Abreu Farias Azevedo; gabriel.azevedo@ucsal.edu.br; (71)99210-5078\n")
            file.write("    Rebeca Bezerra Gonçalves dos Santos; rebecabezerra.santos@ucsal.edu.br; (71)99628-2261\n")
            file.write("    Sarah Evellyn Ferreira Nogueira; sarahevellyn.nogueira@ucsal.edu.br; (71)99675-0337\n")
            file.write("    Robert Valadares de Matos; robert.matos@ucsal.edu.br; (71)98189-1008\n")
            file.write("\n")
            file.write(f"RELATÓRIO DA TABELA DE SÍMBOLOS. Texto fonte analisado: {self.base_name}.251\n")
            file.write("\n")

            if self.symbol_table.is_empty():
                file.write("Nenhum símbolo encontrado na análise.\n")
                return

            symbols = self.symbol_table.get_all_symbols()

            for symbol in symbols:
                file.write(
                    f"Entrada: {symbol['entry_number']}, Codigo: {symbol['atom_code']}, Lexeme: {symbol['lexeme'].upper()},\n")
                file.write(
                    f"QtdCharAntesTrunc: {symbol['original_length']}, QtdCharDepoisTrunc: {symbol['truncated_length']},\n")
                file.write(f"TipoSimb: {symbol['symbol_type']}, Linhas: {{{', '.join(map(str, symbol['lines']))}}}.\n")
                file.write("------------------------------------------------------------\n")

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