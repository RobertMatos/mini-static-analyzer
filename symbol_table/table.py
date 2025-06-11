"""
Tabela de Símbolos para o Static Checker CangaCode2025-1
Responsável por gerenciar apenas identificadores (não palavras reservadas)
"""


class SymbolTable:
    def __init__(self):
        """
        Inicializa a tabela de símbolos vazia.

        Estrutura interna:
        - symbols: lista de dicionários com os atributos de cada símbolo
        - lookup_table: dicionário para busca rápida por lexema (case-insensitive)
        """
        self.initialize()

    def initialize(self):
        """
        Inicializa ou reinicializa a tabela de símbolos.
        Método público que pode ser chamado para resetar a tabela.
        """
        self.symbols = []  # Lista de símbolos com todos os atributos
        self.lookup_table = {}  # Mapeamento lexema -> índice (case-insensitive)
        self.next_entry_number = 1  # Próximo número de entrada disponível

    def insert(self, lexeme, atom_code, line_number, original_length=None):
        """
        Insere um novo símbolo na tabela ou atualiza um existente.

        Args:
            lexeme (str): O lexema do símbolo
            atom_code (int): Código do átomo conforme Apêndice A
            line_number (int): Número da linha onde aparece
            original_length (int, optional): Tamanho original antes da truncagem

        Returns:
            int: Índice do símbolo na tabela (1-based)
        """
        # Debug: imprimir tentativa de inserção
        print(f"DEBUG: Tentando inserir - Lexema: '{lexeme}', Código: {atom_code}, Linha: {line_number}")

        # Normalizar lexema para case-insensitive
        lexeme_normalized = lexeme.upper()

        # Verificar se o símbolo já existe
        existing_index = self.lookup(lexeme)
        if existing_index is not None:
            # Símbolo já existe, apenas atualizar linha se necessário
            print(f"DEBUG: Símbolo '{lexeme}' já existe no índice {existing_index}")
            self._update_line(existing_index - 1, line_number)  # Convert to 0-based
            return existing_index

        # Calcular tamanhos
        if original_length is None:
            original_length = len(lexeme)

        # Truncar lexema em 32 caracteres
        truncated_lexeme = lexeme[:32]
        truncated_length = len(truncated_lexeme)

        # Criar novo símbolo
        symbol = {
            'entry_number': self.next_entry_number,
            'atom_code': atom_code,
            'lexeme': truncated_lexeme,
            'original_length': original_length,
            'truncated_length': truncated_length,
            'symbol_type': '--',  # Inicialmente indefinido
            'lines': [line_number]  # Primeira linha de ocorrência
        }

        # Adicionar à tabela
        index = len(self.symbols)  # Índice 0-based interno
        self.symbols.append(symbol)
        self.lookup_table[lexeme_normalized] = self.next_entry_number

        entry_number = self.next_entry_number
        self.next_entry_number += 1

        print(f"DEBUG: Novo símbolo inserido - Entrada: {entry_number}, Lexema: '{truncated_lexeme}'")
        print(f"DEBUG: Total de símbolos na tabela: {len(self.symbols)}")

        return entry_number

    def lookup(self, lexeme):
        """
        Busca um símbolo na tabela.

        Args:
            lexeme (str): O lexema a ser buscado

        Returns:
            int or None: Número da entrada (1-based) se encontrado, None caso contrário
        """
        lexeme_normalized = lexeme.upper()
        return self.lookup_table.get(lexeme_normalized)

    def _update_line(self, internal_index, line_number):
        """
        Atualiza as linhas de ocorrência de um símbolo (máximo 5).

        Args:
            internal_index (int): Índice interno (0-based) do símbolo
            line_number (int): Número da linha a ser adicionada
        """
        if internal_index < len(self.symbols):
            lines = self.symbols[internal_index]['lines']
            if line_number not in lines and len(lines) < 5:
                lines.append(line_number)

    def update_symbol_type(self, lexeme, symbol_type):
        """
        Atualiza o tipo de um símbolo.

        Args:
            lexeme (str): O lexema do símbolo
            symbol_type (str): Tipo do símbolo (FP, IN, ST, CH, BL, VD, AF, AI, AS, AC, AB)
        """
        entry_number = self.lookup(lexeme)
        if entry_number is not None:
            internal_index = entry_number - 1  # Convert to 0-based
            self.symbols[internal_index]['symbol_type'] = symbol_type

    def get_symbol_count(self):
        """
        Retorna o número total de símbolos na tabela.

        Returns:
            int: Número de símbolos
        """
        return len(self.symbols)

    def get_symbol_by_index(self, entry_number):
        """
        Obtém um símbolo pelo seu número de entrada.

        Args:
            entry_number (int): Número da entrada (1-based)

        Returns:
            dict or None: Dicionário com os dados do símbolo ou None se não encontrado
        """
        if 1 <= entry_number <= len(self.symbols):
            return self.symbols[entry_number - 1].copy()
        return None

    def generate_report_content(self, base_filename):
        """
        Gera o conteúdo do relatório da tabela de símbolos como string.

        Args:
            base_filename (str): Nome base do arquivo (sem extensão)

        Returns:
            str: Conteúdo do relatório formatado
        """
        content = []

        # Cabeçalho do relatório
        content.append("=== RELATÓRIO DA TABELA DE SÍMBOLOS ===")
        content.append(f"Arquivo: {base_filename}.251")
        content.append("Equipe: [CÓDIGO_DA_EQUIPE]")
        content.append("Componentes:")
        content.append("- [Nome1] - [email1] - [telefone1]")
        content.append("- [Nome2] - [email2] - [telefone2]")
        content.append("- [Nome3] - [email3] - [telefone3]")
        content.append("- [Nome4] - [email4] - [telefone4]")
        content.append("")

        # Verificar se há símbolos na tabela
        if not self.symbols:
            content.append("Nenhum símbolo identificador encontrado.")
            return "\n".join(content)

        # Dados dos símbolos
        for symbol in self.symbols:
            lines_str = str(symbol['lines']).replace(' ', '')  # Remove espaços da lista

            content.append(
                f"Entrada: {symbol['entry_number']}, "
                f"Codigo: {symbol['atom_code']:02d}, "
                f"Lexeme: {symbol['lexeme']}, "
                f"TamOriginal: {symbol['original_length']}, "
                f"TamTruncado: {symbol['truncated_length']}, "
                f"Tipo: {symbol['symbol_type']}, "
                f"Linhas: {lines_str}"
            )

        content.append(f"\nTotal de símbolos: {len(self.symbols)}")
        return "\n".join(content)

    def generate_report(self, base_filename):
        """
        Gera o relatório da tabela de símbolos no arquivo .TAB.

        Args:
            base_filename (str): Nome base do arquivo (sem extensão)
        """
        tab_filename = f"{base_filename}.TAB"

        try:
            with open(tab_filename, 'w', encoding='utf-8') as file:
                # Cabeçalho do relatório
                file.write("=== RELATÓRIO DA TABELA DE SÍMBOLOS ===\n")
                file.write(f"Arquivo: {base_filename}.251\n")
                file.write("Equipe: [CÓDIGO_DA_EQUIPE]\n")
                file.write("Componentes:\n")
                file.write("- [Nome1] - [email1] - [telefone1]\n")
                file.write("- [Nome2] - [email2] - [telefone2]\n")
                file.write("- [Nome3] - [email3] - [telefone3]\n")
                file.write("- [Nome4] - [email4] - [telefone4]\n")
                file.write("\n")

                # Verificar se há símbolos na tabela
                if not self.symbols:
                    file.write("Nenhum símbolo identificador encontrado.\n")
                    return

                # Dados dos símbolos
                for symbol in self.symbols:
                    lines_str = str(symbol['lines']).replace(' ', '')  # Remove espaços da lista

                    file.write(
                        f"Entrada: {symbol['entry_number']}, "
                        f"Codigo: {symbol['atom_code']:02d}, "
                        f"Lexeme: {symbol['lexeme']}, "
                        f"TamOriginal: {symbol['original_length']}, "
                        f"TamTruncado: {symbol['truncated_length']}, "
                        f"Tipo: {symbol['symbol_type']}, "
                        f"Linhas: {lines_str}\n"
                    )

                file.write(f"\nTotal de símbolos: {len(self.symbols)}\n")

        except IOError as e:
            print(f"Erro ao gerar relatório .TAB: {e}")
            raise

    def clear(self):
        """
        Limpa toda a tabela de símbolos.
        """
        self.symbols.clear()
        self.lookup_table.clear()
        self.next_entry_number = 1

    def __str__(self):
        """
        Representação string da tabela para debug.
        """
        if not self.symbols:
            return "Tabela de símbolos vazia"

        result = f"Tabela de símbolos ({len(self.symbols)} símbolos):\n"
        for symbol in self.symbols:
            result += f"  {symbol['entry_number']}: {symbol['lexeme']} (código {symbol['atom_code']})\n"
        return result