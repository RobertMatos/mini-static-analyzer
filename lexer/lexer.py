import ply.lex as lex
import re


class Lexer:
    """
    Analisador léxico para a linguagem CangaCode2025-1
    Implementa todos os padrões léxicos especificados no Apêndice C
    """
    
    def __init__(self, source_code):
        """
        Inicializa o lexer com o código fonte
        
        Args:
            source_code (str): Código fonte a ser analisado
        """
        self.source_code = source_code
        self.line_number = 1
        self.position = 0
        self.tokens_generated = []
        
        # Mapeamento de códigos dos átomos conforme Apêndice A
        self.token_codes = {
            'PROGRAM': '01',
            'PROGRAMNAME': '02', 
            'DECLARATIONS': '03',
            'ENDDECLARATIONS': '04',
            'FUNCTIONS': '05',
            'ENDFUNCTIONS': '06',
            'ENDPROGRAM': '07',
            'SEMICOLON': '08',
            'VARTYPE': '09',
            'COLON': '10',
            'LBRACKET': '11',
            'RBRACKET': '12',
            'COMMA': '13',
            'VARIABLE': '14',
            'INTCONST': '15',
            'REAL': '16',
            'INTEGER': '17',
            'STRING': '18',
            'BOOLEAN': '19',
            'CHARACTER': '20',
            'VOID': '21',
            'FUNCTYPE': '22',
            'FUNCTIONNAME': '23',
            'LPAREN': '24',
            'RPAREN': '25',
            'ENDFUNCTION': '26',
            'QUESTION': '27',
            'PARAMTYPE': '28',
            'LBRACE': '29',
            'RBRACE': '30',
            'IF': '31',
            'ENDIF': '32',
            'ELSE': '33',
            'WHILE': '34',
            'ENDWHILE': '35',
            'RETURN': '36',
            'BREAK': '37',
            'PRINT': '38',
            'ASSIGN': '39',
            'LEQ': '40',
            'LT': '41',
            'GT': '42',
            'GEQ': '43',
            'EQ': '44',
            'NEQ': '45',
            'HASH': '46',
            'MINUS': '47',
            'PLUS': '48',
            'MULTIPLY': '49',
            'DIVIDE': '50',
            'MODULO': '51',
            'TRUE': '52',
            'FALSE': '53',
            'REALCONST': '54',
            'STRINGCONST': '55',
            'CHARCONST': '56'
        }
        
        # Palavras reservadas
        self.reserved = {
            'program': 'PROGRAM',
            'declarations': 'DECLARATIONS',
            'enddeclarations': 'ENDDECLARATIONS', 
            'functions': 'FUNCTIONS',
            'endfunctions': 'ENDFUNCTIONS',
            'endprogram': 'ENDPROGRAM',
            'vartype': 'VARTYPE',
            'real': 'REAL',
            'integer': 'INTEGER',
            'string': 'STRING',
            'boolean': 'BOOLEAN',
            'character': 'CHARACTER',
            'void': 'VOID',
            'functype': 'FUNCTYPE',
            'endfunction': 'ENDFUNCTION',
            'paramtype': 'PARAMTYPE',
            'if': 'IF',
            'endif': 'ENDIF',
            'else': 'ELSE',
            'while': 'WHILE',
            'endwhile': 'ENDWHILE',
            'return': 'RETURN',
            'break': 'BREAK',
            'print': 'PRINT',
            'true': 'TRUE',
            'false': 'FALSE'
        }
        
        # Lista de tokens
        self.tokens = [
            'PROGRAMNAME', 'VARIABLE', 'FUNCTIONNAME',
            'INTCONST', 'REALCONST', 'STRINGCONST', 'CHARCONST',
            'ASSIGN', 'LEQ', 'GEQ', 'EQ', 'NEQ', 'LT', 'GT',
            'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'MODULO',
            'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET',
            'SEMICOLON', 'COLON', 'COMMA', 'QUESTION', 'HASH'
        ] + list(self.reserved.values())
        
        # Construir o lexer
        self.lexer = lex.lex(module=self)
        self.lexer.input(self._preprocess_source(source_code))
    
    def _preprocess_source(self, source):
        """
        Pré-processa o código fonte removendo comentários e caracteres inválidos
        """
        # Remover comentários de bloco /* */
        source = re.sub(r'/\*.*?\*/', '', source, flags=re.DOTALL)
        
        # Remover comentários de linha //
        source = re.sub(r'//.*', '', source)
        
        # Filtrar caracteres inválidos (manter apenas válidos)
        valid_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
                         '+-*/(){}[]<>=!:;,?#$_."\' \t\n\r')
        filtered_source = ''.join(c for c in source if c in valid_chars)
        
        return filtered_source
    
    def _truncate_lexeme(self, lexeme):
        """
        Trunca o lexema em 32 caracteres válidos
        """
        if len(lexeme) > 32:
            return lexeme[:32]
        return lexeme
    
    # Regras de tokens
    
    # Operadores compostos (devem vir antes dos simples)
    t_ASSIGN = r':='
    t_LEQ = r'<='
    t_GEQ = r'>='
    t_EQ = r'=='
    t_NEQ = r'!='
    
    # Operadores simples
    t_LT = r'<'
    t_GT = r'>'
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_MULTIPLY = r'\*'
    t_DIVIDE = r'/'
    t_MODULO = r'%'
    t_HASH = r'\#'
    
    # Delimitadores
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_SEMICOLON = r';'
    t_COLON = r':'
    t_COMMA = r','
    t_QUESTION = r'\?'
    
    # Ignorar espaços e tabs
    t_ignore = ' \t'
    
    def t_REALCONST(self, t):
        r'(\d+\.\d+([eE][+-]?\d+)?)'
        t.value = self._truncate_lexeme(t.value.upper())
        return t
    
    def t_INTCONST(self, t):
        r'\d+'
        t.value = self._truncate_lexeme(t.value)
        return t
    
    def t_STRINGCONST(self, t):
        r'"[a-zA-Z0-9 $_\.]*"'
        t.value = self._truncate_lexeme(t.value.upper())
        return t
    
    def t_CHARCONST(self, t):
        r"'[a-zA-Z]'"
        t.value = self._truncate_lexeme(t.value.upper())
        return t
    
    def t_IDENTIFIER(self, t):
        r'[a-zA-Z][a-zA-Z0-9]*|_[a-zA-Z0-9_]*'
        # Converter para maiúsculo para case-insensitive
        t.value = t.value.upper()
        
        # Truncar se necessário
        t.value = self._truncate_lexeme(t.value)
        
        # Verificar se é palavra reservada
        token_type = self.reserved.get(t.value.lower(), None)
        
        if token_type:
            t.type = token_type
        else:
            # Determinar tipo de identificador baseado no contexto
            # Por simplicidade, vamos classificar como VARIABLE por padrão
            # Em uma implementação completa, isso seria determinado pelo parser
            if self._is_program_name_context():
                t.type = 'PROGRAMNAME'
            elif self._is_function_name_context():
                t.type = 'FUNCTIONNAME'
            else:
                t.type = 'VARIABLE'
        
        return t
    
    def _is_program_name_context(self):
        """
        Verifica se estamos no contexto de um nome de programa
        (após a palavra 'program')
        """
        if len(self.tokens_generated) > 0:
            last_token = self.tokens_generated[-1]
            return last_token[0] == 'PROGRAM'
        return False
    
    def _is_function_name_context(self):
        """
        Verifica se estamos no contexto de um nome de função
        (após 'functype' e especificação de tipo)
        """
        if len(self.tokens_generated) >= 3:
            # Procura por padrão: functype tipo :
            for i in range(len(self.tokens_generated) - 2):
                if (self.tokens_generated[i][0] == 'FUNCTYPE' and
                    self.tokens_generated[i + 2][0] == 'COLON'):
                    return True
        return False
    
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        self.line_number += len(t.value)
    
    def t_error(self, t):
        """
        Tratamento de erro - caracteres inválidos são ignorados
        (filtro de primeiro nível)
        """
        t.lexer.skip(1)
    
    def next_token(self):
        """
        Retorna o próximo token
        
        Returns:
            tuple: (token_type, lexeme, line_number) ou None se EOF
        """
        token = self.lexer.token()
        
        if token is None:
            return None
        
        # Obter código do átomo
        token_code = self.token_codes.get(token.type, '00')
        
        # Armazenar token gerado para análise de contexto
        token_info = (token.type, token.value, self.line_number)
        self.tokens_generated.append(token_info)
        
        return (token_code, token.value, token.lineno)
    
    def tokenize_all(self):
        """
        Tokeniza todo o código fonte e retorna lista de tokens
        
        Returns:
            list: Lista de tuplas (token_code, lexeme, line_number)
        """
        tokens = []
        while True:
            token = self.next_token()
            if token is None:
                break
            tokens.append(token)
        return tokens
    
    def generate_lex_report(self, filename):
        """
        Gera relatório de análise léxica
        
        Args:
            filename (str): Nome do arquivo fonte
            
        Returns:
            str: Conteúdo do relatório LEX
        """
        tokens = self.tokenize_all()
        
        report = "=== RELATÓRIO DA ANÁLISE LÉXICA ===\n"
        report += f"Arquivo: {filename}\n"
        report += "Equipe: [código da equipe]\n"
        report += "Componentes: [nomes dos componentes]\n"
        report += "\n"
        
        for token_code, lexeme, line_num in tokens:
            # Determinar índice na tabela de símbolos
            if token_code in ['02', '14', '23']:  # PROGRAMNAME, VARIABLE, FUNCTIONNAME
                index_tab = "1"  # Simplificado - em implementação real seria dinâmico
            else:
                index_tab = "-"
            
            report += f"Lexeme: {lexeme}, Código: {token_code}, ÍndiceTabSimb: {index_tab}, Linha: {line_num}\n"
        
        return report


# Exemplo de uso
if __name__ == "__main__":
    # Código fonte de exemplo
    source_code = """
    program meuPrograma
    declarations
        vartype integer: contador, limite
        vartype real: media, soma
    endDeclarations
    
    functions
        functype integer: calcular(paramtype integer: x, y)
            if (x > y)
                return x + y
            else
                return x - y
            endif
        endFunction
    endFunctions
    
    endProgram
    """
    
    # Criar lexer
    lexer = Lexer(source_code)
    
    # Gerar tokens
    tokens = lexer.tokenize_all()
    
    # Exibir tokens
    for token in tokens:
        print(f"Código: {token[0]}, Lexeme: {token[1]}, Linha: {token[2]}")
    
    # Gerar relatório
    report = lexer.generate_lex_report("exemplo.251")
    print("\n" + report)