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
            'PROGRAM': 1,
            'PROGRAMNAME': 2,
            'DECLARATIONS': 3,
            'ENDDECLARATIONS': 4,
            'FUNCTIONS': 5,
            'ENDFUNCTIONS': 6,
            'ENDPROGRAM': 7,
            'SEMICOLON': 8,
            'VARTYPE': 9,
            'COLON': 10,
            'REAL': 11,
            'INTEGER': 12,
            'STRING': 13,
            'BOOLEAN': 14,
            'CHARACTER': 15,
            'VOID': 16,
            'LBRACKET': 17,
            'RBRACKET': 17,  # Mesmo código que LBRACKET
            'FUNCTYPE': 18,
            'LPAREN': 19,
            'RPAREN': 20,
            'ENDFUNCTION': 21,
            'COMMA': 22,
            'QUESTION': 22,  # Mesmo código que COMMA
            'PARAMTYPE': 23,
            'LBRACE': 24,
            'RBRACE': 25,
            'IF': 26,
            'ENDIF': 27,
            'ELSE': 28,
            'WHILE': 29,
            'ENDWHILE': 30,
            'RETURN': 31,
            'BREAK': 32,
            'PRINT': 33,
            'ASSIGN': 34,
            'LEQ': 35,
            'LT': 36,
            'GT': 37,
            'GEQ': 38,
            'EQ': 39,
            'NEQ': 40,
            'HASH': 41,
            'MINUS': 42,
            'PLUS': 43,
            'MULTIPLY': 44,
            'DIVIDE': 45,
            'MODULO': 46,
            'TRUE': 47,
            'FALSE': 48,
            'VARIABLE': 49,  # Identificadores de variável
            'INTCONST': 50,
            'REALCONST': 51,
            'STRINGCONST': 52,
            'CHARCONST': 53,
            'FUNCTIONNAME': 18  # Reutiliza código do FUNCTYPE
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

        # Controle de contexto para identificadores
        self.context_stack = []
        self.last_token_type = None

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
        original_value = t.value
        t.value = t.value.upper()

        # Truncar se necessário
        t.value = self._truncate_lexeme(t.value)

        # Verificar se é palavra reservada
        token_type = self.reserved.get(t.value.lower(), None)

        if token_type:
            t.type = token_type
        else:
            # Determinar tipo de identificador baseado no contexto
            identifier_type = self._determine_identifier_type()
            t.type = identifier_type

        return t

    def _determine_identifier_type(self):
        """
        Determina o tipo de identificador baseado no contexto anterior
        """
        if not self.tokens_generated:
            return 'VARIABLE'

        # Verificar últimos tokens para determinar contexto
        if len(self.tokens_generated) > 0:
            last_token = self.tokens_generated[-1]

            # Após 'program' = PROGRAMNAME
            if last_token[0] == 'PROGRAM':
                return 'PROGRAMNAME'

            # Após 'functype tipo :' = FUNCTIONNAME
            if len(self.tokens_generated) >= 3:
                if (self.tokens_generated[-3][0] == 'FUNCTYPE' and
                        self.tokens_generated[-1][0] == 'COLON'):
                    return 'FUNCTIONNAME'

        # Padrão: identificador de variável
        return 'VARIABLE'

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
            tuple: (token_code, lexeme, line_number) ou None se EOF
        """
        token = self.lexer.token()

        if token is None:
            return None

        # Obter código do átomo
        token_code = self.token_codes.get(token.type, 0)

        # Armazenar token gerado para análise de contexto
        token_info = (token.type, token.value, token.lineno)
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