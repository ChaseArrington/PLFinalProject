#------------------------------------------------------------
# lex.py
#
# tokenizer
# ------------------------------------------------------------

import ply.lex as lex

# List of token names.   
tokens = ('NUM', 'LPAREN', 'RPAREN','NIL', 'TRUE', 'FALSE', 'TEXT', 'MATH', 'Eq', 'LCURLY', 'RCURLY',
          'FUNC', 'PRINT', 'STRING', 'LBrack', 'RBrack', 'DOT', 'DATE', 'EXEC','PRINTLINE','STATEMENT','ALL','SELECT',
          'GREAT', 'LESS','AND')

# Reserved words
reserved = {
    'nil' : 'NIL',
    'Class' : 'CLASS',
    'def' : 'FUNC',
    'print' : 'PRINT',
    'exec' : 'EXEC',
    'printLine' : 'PRINTLINE',
    'select' : 'SELECT',
    'all' : 'ALL',
    'and' : 'AND',
}

# Regular expression rules for simple tokens
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBrack = r'\['
t_RBrack = r'\]'
t_TRUE = r'\#t'
t_FALSE = r'\#f'
t_MATH = r'[\+\-\/\*]'
t_Eq = r'\='
t_LCURLY = r'{'
t_RCURLY = r'}'
t_STRING = r'\'[a-zA-Z ]+\''
t_DOT = r'\.'
t_GREAT = r'>'
t_LESS = r'<'

def t_STATEMENT(t):
    r'@.*'
    return t

def t_DATE(t):
    r'\d{1,2}[-][A-Za-z]{3}[-]\d{2,3}'
    return t

def t_NUM(t):
    r'\d+'
    try:
        t.value = int(t.value)    
    except ValueError:
        print "Line %d: Number %s is too large!" % (t.lineno,t.value)
        t.value = 0
    return t


def t_TEXT(t):
    r'[a-zA-Z_]+'
    #r'\'[a-zA-Z0-9 '+\*\- :,]*\''
    t.type = reserved.get(t.value,'TEXT')    # Check for reserved words
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs, commas, quotes)
t_ignore  = ' \t'
t_ignore_COMMMA = '\,'
t_ignore_QUOTE = '\''

# Error handling rule
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

# Build the lexer
lex.lex()

if __name__ == '__main__':
    lex.runmain()
