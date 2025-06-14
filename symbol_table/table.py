"""
Tabela de Símbolos para o Static Checker CangaCode2025-1
Responsável por gerenciar apenas identificadores (não palavras reservadas)
Formatação conforme especificação do projeto (arquivo PDF)
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
        Metodo público que pode ser chamado para resetar a tabela.

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
        print(f"DEBUG SymbolTable: Tentando inserir - Lexema: '{lexeme}', Código: {atom_code}, Linha: {line_number}")

        # Normalizar lexema para case-insensitive
        lexeme_normalized = lexeme.upper()

        # Verificar se o símbolo já existe
        existing_index = self.lookup(lexeme)
        if existing_index is not None:
            # Símbolo já existe, apenas atualizar linha se necessário
            print(f"DEBUG SymbolTable: Símbolo '{lexeme}' já existe no índice {existing_index}")
            self._update_line(existing_index - 1, line_number)  # Convert to 0-based
            return existing_index

        # Calcular tamanhos
        if original_length is None:
            original_length = len(lexeme)

        # Truncar lexema em 32 caracteres
        truncated_lexeme = lexeme[:32]
        truncated_length = len(truncated_lexeme)

        # Determinar tipo do símbolo baseado no código do átomo
        symbol_type = self._determine_symbol_type(atom_code)

        # Criar novo símbolo
        symbol = {
            'entry_number': self.next_entry_number,
            'atom_code': atom_code,
            'lexeme': truncated_lexeme,
            'original_length': original_length,
            'truncated_length': truncated_length,
            'symbol_type': symbol_type,
            'lines': [line_number]  # Primeira linha de ocorrência
        }

        # Adicionar à tabela
        self.symbols.append(symbol)

        # Atualizar lookup table (case-insensitive)
        self.lookup_table[lexeme_normalized] = self.next_entry_number

        print(f"DEBUG SymbolTable: Símbolo '{lexeme}' inserido com sucesso no índice {self.next_entry_number}")

        # Incrementar contador e retornar índice
        current_index = self.next_entry_number
        self.next_entry_number += 1

        return current_index

    def _determine_symbol_type(self, atom_code):
        """
        Determina o tipo do símbolo baseado no código do átomo.
        Conforme especificação do PDF.

        Args:
            atom_code (int): Código do átomo

        Returns:
            str: Tipo do símbolo
        """
        type_mapping = {
            2: 'nome de programa',        # PROGRAMNAME
            18: 'nome de função',         # FUNCTIONNAME
            49: 'nome de variável'        # VARIABLE
        }
        return type_mapping.get(atom_code, 'tipo desconhecido')

    def _update_line(self, index, line_number):
        """
        Atualiza as linhas de ocorrência de um símbolo existente.

        Args:
            index (int): Índice do símbolo na lista (0-based)
            line_number (int): Nova linha de ocorrência
        """
        if 0 <= index < len(self.symbols):
            if line_number not in self.symbols[index]['lines']:
                self.symbols[index]['lines'].append(line_number)
                self.symbols[index]['lines'].sort()

    def lookup(self, lexeme):
        """
        Busca um símbolo na tabela pelo lexema.

        Args:
            lexeme (str): Lexema a ser buscado

        Returns:
            int or None: Índice do símbolo (1-based) ou None se não encontrado
        """
        lexeme_normalized = lexeme.upper()
        return self.lookup_table.get(lexeme_normalized)

    def get_symbol(self, index):
        """
        Obtém um símbolo pelo índice.

        Args:
            index (int): Índice do símbolo (1-based)

        Returns:
            dict or None: Dicionário com dados do símbolo ou None se não encontrado
        """
        if 1 <= index <= len(self.symbols):
            return self.symbols[index - 1].copy()  # Convert to 0-based and return copy
        return None

    def get_symbol_count(self):
        """
        Retorna o número total de símbolos na tabela.

        Returns:
            int: Quantidade de símbolos
        """
        return len(self.symbols)

    def get_all_symbols(self):
        """
        Retorna todos os símbolos da tabela.

        Returns:
            list: Lista com cópias de todos os símbolos
        """
        return [symbol.copy() for symbol in self.symbols]

    def is_empty(self):
        """
        Verifica se a tabela está vazia.

        Returns:
            bool: True se vazia, False caso contrário
        """
        return len(self.symbols) == 0

    def clear(self):
        """
        Limpa toda a tabela de símbolos.
        """
        self.initialize()

    def generate_report_content(self, base_filename):
        """
        Gera o conteúdo do relatório da tabela de símbolos conforme especificação do PDF.

        Args:
            base_filename (str): Nome base do arquivo (sem extensão)

        Returns:
            str: Conteúdo formatado do relatório
        """
        if self.is_empty():
            return "Nenhum símbolo encontrado na análise."

        lines = []

        # Formato conforme exemplo do PDF
        for symbol in self.symbols:
            lines.append(f"Entrada: {symbol['entry_number']}")
            lines.append(f"    Lexema: {symbol['lexeme']}")
            lines.append(f"    Código átomo: {symbol['atom_code']}")
            lines.append(f"    Tamanho original: {symbol['original_length']}")
            lines.append(f"    Tamanho após truncamento: {symbol['truncated_length']}")
            lines.append(f"    Tipo: {symbol['symbol_type']}")

            # Formatação das linhas de ocorrência
            lines_str = ', '.join(map(str, symbol['lines']))
            if len(symbol['lines']) == 1:
                lines.append(f"    Linha de definição: {lines_str}")
            else:
                lines.append(f"    Linhas de definição: {lines_str}")

            lines.append("")  # Linha em branco entre entradas

        return '\n'.join(lines)

    def print_debug_info(self):
        """
        Imprime informações de debug da tabela.
        """
        print(f"DEBUG SymbolTable - Estado atual:")
        print(f"  Total de símbolos: {len(self.symbols)}")
        print(f"  Próximo número de entrada: {self.next_entry_number}")
        print(f"  Lookup table keys: {list(self.lookup_table.keys())}")

        if self.symbols:
            print("  Símbolos:")
            for i, symbol in enumerate(self.symbols):
                print(f"    [{i}] {symbol}")

    def validate_integrity(self):
        """
        Valida a integridade da tabela de símbolos.

        Returns:
            tuple: (bool, list) - (é_válida, lista_de_erros)
        """
        errors = []

        # Verificar se lookup_table está sincronizado
        if len(self.lookup_table) != len(self.symbols):
            errors.append(f"Lookup table desincronizada: {len(self.lookup_table)} vs {len(self.symbols)}")

        # Verificar entrada_number sequencial
        expected_entry = 1
        for i, symbol in enumerate(self.symbols):
            if symbol['entry_number'] != expected_entry:
                errors.append(f"Entrada {i}: número esperado {expected_entry}, encontrado {symbol['entry_number']}")
            expected_entry += 1

        # Verificar se next_entry_number está correto
        if self.next_entry_number != len(self.symbols) + 1:
            errors.append(f"next_entry_number incorreto: {self.next_entry_number}, esperado {len(self.symbols) + 1}")

        # Verificar se todos os símbolos no lookup_table existem
        for lexeme, index in self.lookup_table.items():
            if not (1 <= index <= len(self.symbols)):
                errors.append(f"Lookup table: lexema '{lexeme}' aponta para índice inválido {index}")

        return len(errors) == 0, errors


# Exemplo de uso e teste
if __name__ == "__main__":
    # Teste básico da tabela de símbolos
    table = SymbolTable()

    print("=== TESTE DA TABELA DE SÍMBOLOS ===\n")

    # Inserir alguns símbolos de teste
    test_symbols = [
        ("MEUPROGRAMA", 2, 1),      # PROGRAMNAME
        ("CONTADOR", 49, 3),        # VARIABLE
        ("LIMITE", 49, 3),          # VARIABLE
        ("CALCULAR", 18, 7),        # FUNCTIONNAME
        ("X", 49, 7),              # VARIABLE
        ("Y", 49, 7),              # VARIABLE
        ("CONTADOR", 49, 10),       # VARIABLE (duplicata)
    ]

    print("Inserindo símbolos de teste:")
    for lexeme, code, line in test_symbols:
        index = table.insert(lexeme, code, line)
        print(f"  '{lexeme}' -> índice {index}")

    print(f"\nTotal de símbolos únicos: {table.get_symbol_count()}")

    # Testar busca
    print("\nTeste de busca:")
    for lexeme in ["MEUPROGRAMA", "contador", "INEXISTENTE"]:
        result = table.lookup(lexeme)
        print(f"  Busca por '{lexeme}': {result}")

    # Gerar relatório
    print("\n" + "="*50)
    print("RELATÓRIO DA TABELA:")
    print("="*50)
    print(table.generate_report_content("teste"))

    # Validar integridade
    is_valid, errors = table.validate_integrity()
    print(f"\nIntegridade da tabela: {'OK' if is_valid else 'ERRO'}")
    if errors:
        for error in errors:
            print(f"  - {error}")
