import ply.lex as lex
import re


class Lexer:
    """
    Analisador léxico para a linguagem CangaCode2025-1
    Implementa todos os padrões léxicos especificados no Apêndice C
    COM CORREÇÃO CRÍTICA DO MAPEAMENTO DE LINHAS
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
            'INTEGER': 'PRS01', 'PROGRAM': 'PRS14', 'REAL': 'PRS02', 'ENDPROGRAM': 'PRS15',
            'CHARACTER': 'PRS03', 'FUNCTIONS': 'PRS16', 'STRING': 'PRS04', 'ENDFUNCTIONS': 'PRS17',
            'BOOLEAN': 'PRS05', 'ENDFUNCTION': 'PRS18', 'VOID': 'PRS06', 'RETURN': 'PRS19',
            'TRUE': 'PRS07', 'IF': 'PRS20', 'FALSE': 'PRS08', 'ELSE': 'PRS21',
            'VARTYPE': 'PRS09', 'ENDIF': 'PRS22', 'FUNCTYPE': 'PRS10', 'WHILE': 'PRS23',
            'PARAMTYPE': 'PRS11', 'ENDWHILE': 'PRS24', 'DECLARATIONS': 'PRS12', 'BREAK': 'PRS25',
            'ENDDECLARATIONS': 'PRS13', 'PRINT': 'PRS26',

            # Símbolos Reservados (Códigos SRS01-SRS22)
            'SEMICOLON': 'SRS01', 'HASH': 'SRS12', 'COMMA': 'SRS02', 'MINUS': 'SRS13',
            'COLON': 'SRS03', 'PLUS': 'SRS14', 'ASSIGN': 'SRS04', 'MULTIPLY': 'SRS15',
            'QUESTION': 'SRS05', 'DIVIDE': 'SRS16', 'LPAREN': 'SRS06', 'MODULO': 'SRS17',
            'RPAREN': 'SRS07', 'EQ': 'SRS18', 'LBRACKET': 'SRS08', 'NEQ': 'SRS19',
            'RBRACKET': 'SRS09', 'LT': 'SRS20', 'LBRACE': 'SRS10', 'LEQ': 'SRS21',
            'RBRACE': 'SRS11', 'GT': 'SRS22', 'GEQ': 'SRS23',

            # Identificadores (Códigos ID01-ID07)
            'PROGRAMNAME': 'IDN01', 'VARIABLE': 'IDN02', 'FUNCTIONNAME': 'IDN03',

            # Constantes (Códigos ID04-ID07)
            'INTCONST': 'IDN04', 'REALCONST': 'IDN05', 'STRINGCONST': 'IDN06', 'CHARCONST': 'IDN07',
        }

        # Palavras reservadas
        self.reserved = {
            'program': 'PROGRAM', 'declarations': 'DECLARATIONS', 'enddeclarations': 'ENDDECLARATIONS',
            'functions': 'FUNCTIONS', 'endfunctions': 'ENDFUNCTIONS', 'endprogram': 'ENDPROGRAM',
            'vartype': 'VARTYPE', 'real': 'REAL', 'integer': 'INTEGER', 'string': 'STRING',
            'boolean': 'BOOLEAN', 'character': 'CHARACTER', 'void': 'VOID', 'functype': 'FUNCTYPE',
            'endfunction': 'ENDFUNCTION', 'paramtype': 'PARAMTYPE', 'if': 'IF', 'endif': 'ENDIF',
            'else': 'ELSE', 'while': 'WHILE', 'endwhile': 'ENDWHILE', 'return': 'RETURN',
            'break': 'BREAK', 'print': 'PRINT', 'true': 'TRUE', 'false': 'FALSE'
        }

        # Lista de tokens
        self.tokens = [
            'PROGRAMNAME', 'VARIABLE', 'FUNCTIONNAME', 'INTCONST', 'REALCONST',
            'STRINGCONST', 'CHARCONST', 'ASSIGN', 'LEQ', 'GEQ', 'EQ', 'NEQ',
            'LT', 'GT', 'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'MODULO', 'LPAREN',
            'RPAREN', 'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET', 'SEMICOLON',
            'COLON', 'COMMA', 'QUESTION', 'HASH'
        ] + list(self.reserved.values())

        # Controle de contexto para identificadores
        self.last_token_type = None

        # CORREÇÃO CRÍTICA: Pré-processar código com mapeamento correto
        processed_source = self._preprocess_source(self.source_code)

        # Construir o lexer
        self.lexer = lex.lex(module=self)
        self.lexer.input(processed_source)
        self.lexer.lineno = 1

    def _preprocess_source(self, source: str) -> str:
        """
        CORREÇÃO: Pré-processa o código fonte para remover comentários
        preservando a contagem de linhas.

        Args:
            source: O código fonte original.

        Returns:
            O código fonte processado.
        """
        # Função para substituir comentários de bloco por newlines, preservando a contagem de linhas
        def block_comment_replacer(match):
            comment_text = match.group(0)
            return '\n' * comment_text.count('\n')

        # 1. Substitui comentários de bloco por newlines para manter a estrutura das linhas
        source = re.sub(r'/\*.*?\*/', block_comment_replacer, source, flags=re.DOTALL)

        # 2. Remove comentários de linha
        source = re.sub(r'//.*', '', source)

        return source

    def _truncate_lexeme(self, lexeme):
        """
        Trunca o lexema em 32 caracteres válidos
        """
        if len(lexeme) > 32:
            return lexeme[:32]
        return lexeme

    # Regras de tokens

    t_ASSIGN = r':='
    t_LEQ = r'<='
    t_GEQ = r'>='
    t_EQ = r'=='
    t_NEQ = r'!='
    t_LT = r'<'
    t_GT = r'>'
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_MULTIPLY = r'\*'
    t_DIVIDE = r'/'
    t_MODULO = r'%'
    t_HASH = r'\#'
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
        original_value = t.value
        t.value = t.value.upper()
        t.value = self._truncate_lexeme(t.value)
        
        token_type = self.reserved.get(t.value.lower(), None)

        if token_type:
            t.type = token_type
        else:
            identifier_type = self._determine_identifier_type()
            t.type = identifier_type
        
        # Armazena o tipo do token atual para a próxima iteração
        self.last_token_type = t.type
        return t

    def _determine_identifier_type(self):
        """
        Determina o tipo de identificador baseado no contexto anterior.
        NOTA: Esta é uma implementação simplista e pode não cobrir todos os casos.
        """
        # Após 'program' -> PROGRAMNAME
        if self.last_token_type == 'PROGRAM':
            return 'PROGRAMNAME'
        
        # Após 'functype tipo :' -> FUNCTIONNAME
        # Verificação simplificada: se o último token foi um tipo, assume-se que o próximo é uma função.
        # Uma abordagem mais robusta exigiria um parser.
        if self.last_token_type in ['INTEGER', 'REAL', 'STRING', 'CHARACTER', 'BOOLEAN', 'VOID']:
             # Se os 3 últimos tokens foram 'FUNCTYPE', 'TIPO', ':' -> é nome de função.
             # Esta lógica é complexa para o lexer, então usamos uma heurística mais simples.
             # O parser é o local ideal para essa distinção.
             pass # Lógica mais complexa pode ser adicionada aqui

        # Padrão: identificador de variável
        return 'VARIABLE'

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        """
        Tratamento de erro - caracteres inválidos são ignorados
        """
        # Para evitar problemas com caracteres inválidos, apenas os pulamos.
        # Em um compilador real, um erro seria reportado aqui.
        print(f"Caractere ilegal '{t.value[0]}' na linha {t.lexer.lineno}")
        t.lexer.skip(1)

    def next_token(self):
        """
        Retorna o próximo token do lexer.
        """
        token = self.lexer.token()
        if token is None:
            return None

        # Obter código do átomo
        token_code = self.token_codes.get(token.type, 'UNKNOWN')

        # Armazenar para análise de contexto
        token_info = (token.type, token.value, token.lineno)
        self.tokens_generated.append(token_info)

        # O número da linha (token.lineno) agora deve estar correto
        return (token_code, token.value, token.lineno)

    def tokenize_all(self):
        """
        Tokeniza todo o código fonte e retorna lista de tokens.
        """
        tokens = []
        while True:
            token = self.next_token()
            if token is None:
                break
            tokens.append(token)
        return tokens



# Função de teste para validar mapeamento de linhas
def test_line_mapping():
    """
    Testa especificamente o mapeamento de linhas
    """
    test_code = """program teste
// comentário linha 2
declarations
    /* comentário 
       de bloco */
    vartype integer: x
endDeclarations
endProgram"""

    print("=== TESTE DE MAPEAMENTO DE LINHAS ===")
    print("Código original:")
    for i, line in enumerate(test_code.split('\n'), 1):
        print(f"{i:2d}: {line}")

    lexer = Lexer(test_code)
    tokens = lexer.tokenize_all()

    print("\nTokens com linhas:")
    for code, lexeme, line in tokens:
        print(f"  '{lexeme}' -> linha {line}")


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

    # Executar teste de mapeamento
    print("\n" + "=" * 50)
    test_line_mapping()
