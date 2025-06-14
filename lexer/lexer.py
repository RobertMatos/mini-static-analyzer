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
        self.tokens_generated = []

        # Mapeamento de códigos dos átomos conforme Apêndice A
        self.token_codes = {
            # Palavras Reservadas (Códigos PRS01-PRS26)
            'INTEGER': 'PRS01',
            'PROGRAM': 'PRS14',
            'REAL': 'PRS02',
            'ENDPROGRAM': 'PRS15',
            'CHARACTER': 'PRS03',
            'FUNCTIONS': 'PRS16',
            'STRING': 'PRS04',
            'ENDFUNCTIONS': 'PRS17',
            'BOOLEAN': 'PRS05',
            'ENDFUNCTION': 'PRS18',
            'VOID': 'PRS06',
            'RETURN': 'PRS19',
            'TRUE': 'PRS07',
            'IF': 'PRS20',
            'FALSE': 'PRS08',
            'ELSE': 'PRS21',
            'VARTYPE': 'PRS09',
            'ENDIF': 'PRS22',
            'FUNCTYPE': 'PRS10',
            'WHILE': 'PRS23',
            'PARAMTYPE': 'PRS11',
            'ENDWHILE': 'PRS24',
            'DECLARATIONS': 'PRS12',
            'BREAK': 'PRS25',
            'ENDDECLARATIONS': 'PRS13',
            'PRINT': 'PRS26',

            # Símbolos Reservados (Códigos SRS01-SRS22)
            'SEMICOLON': 'SRS01',  # ;
            'HASH': 'SRS12',  # #
            'COMMA': 'SRS02',  # ,
            'MINUS': 'SRS13',  # -
            'COLON': 'SRS03',  # :
            'PLUS': 'SRS14',  # +
            'ASSIGN': 'SRS04',  # :=
            'MULTIPLY': 'SRS15',  # *
            'QUESTION': 'SRS05',  # ?
            'DIVIDE': 'SRS16',  # /
            'LPAREN': 'SRS06',  # (
            'MODULO': 'SRS17',  # %
            'RPAREN': 'SRS07',  # )
            'EQ': 'SRS18',  # ==
            'LBRACKET': 'SRS08',  # [
            'NEQ': 'SRS19',  # !=
            'RBRACKET': 'SRS09',  # ]
            'LT': 'SRS20',  # <
            'LBRACE': 'SRS10',  # {
            'LEQ': 'SRS21',  # <=
            'RBRACE': 'SRS11',  # }
            'GT': 'SRS22',  # >
            'GEQ': 'SRS23',  # >=

            # Identificadores (Códigos ID01-ID07)
            'PROGRAMNAME': 'IDN01',
            'VARIABLE': 'IDN02',
            'FUNCTIONNAME': 'IDN03',

            # Constantes (Códigos ID04-ID07)
            'INTCONST': 'IDN04',
            'REALCONST': 'IDN05',
            'STRINGCONST': 'IDN06',
            'CHARCONST': 'IDN07',

            # Submáquinas (Códigos SUB01-SUBNN)
            'SUBMACHINE1': 'SUB01',
            'SUBMACHINE2': 'SUB02',
            'SUBMACHINE3': 'SUB03',
            'SUBMACHINEN': 'SUBNN'
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

        # CORREÇÃO: Processar código com numeração de linha consistente
        processed_source = self._preprocess_source(source_code)
        self.lexer.input(processed_source)

        # Inicializar contador de linha do PLY
        self.lexer.lineno = 1

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
        # CORREÇÃO: Usar apenas o controle do PLY
        t.lexer.lineno += len(t.value)

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
        token_code = self.token_codes.get(token.type, 'UNKNOWN')

        # CORREÇÃO: Usar sempre t.lineno (controle do PLY)
        line_number = token.lineno

        # Armazenar token gerado para análise de contexto
        token_info = (token.type, token.value, line_number)
        self.tokens_generated.append(token_info)

        return (token_code, token.value, line_number)

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
    source_code = """program meuPrograma
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
