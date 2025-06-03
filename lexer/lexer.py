import ply.lex as lex

tokens = [
    'ID',
    'INTCONST',
    'REALCONST',
    'STRINGCONST',
    'CHARCONST',
    'PLUS',
    'MINUS',
    'MULT',
    'DIV',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'EQUALS',
    'SEMI',
    'COMMA',
]

reserved = {
    'program': 'PROGRAM',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'function': 'FUNCTION',
    'var': 'VAR',
    'return': 'RETURN',
    'int': 'INT',
    'real': 'REAL',
    'char': 'CHAR',
    'string': 'STRING',
}

tokens += list(reserved.values())

t_ignore = ' \t'

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_MULT    = r'\*'
t_DIV     = r'/'
t_EQUALS  = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACE  = r'\{'
t_RBRACE  = r'\}'
t_SEMI    = r';'
t_COMMA   = r','

def t_STRINGCONST(t):
    r'\"([^\\\n]|(\\.))*?\"'
    return t

def t_CHARCONST(t):
    r'\'[a-zA-Z0-9]\''
    return t

def t_REALCONST(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INTCONST(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value.lower(), 'ID')
    if t.type == 'ID' and hasattr(t.lexer, 'symbol_table') and t.lexer.symbol_table:
        t.index = t.lexer.symbol_table.add(t.value, t.lineno)
    else:
        t.index = None
    return t

def t_COMMENT_LINE(t):
    r'//.*'
    pass

def t_COMMENT_BLOCK(t):
    r'/\*[\s\S]*?\*/'
    pass

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"[Erro Léxico] Caractere ilegal: {t.value[0]} (linha {t.lexer.lineno})")
    t.lexer.skip(1)

def build_lexer(symbol_table=None):
    lexer = lex.lex()
    lexer.symbol_table = symbol_table
    return lexer
