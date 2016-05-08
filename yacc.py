import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from lex import tokens

DEBUG = False

# Namespace & built-in functions

name = {}
vars = {}
functions = {}

global ast
ast = []


def _print(l):
    print lisp_str(l[0])

name['print'] = _print

#  Evaluation functions

#def lisp_eval(simb, items):
#    if simb in name:
#        return call(name[simb], eval_lists(items))
#    else:
#        return [simb] + items

#def call(f, l):
#    try:
#        return f(eval_lists(l))
#    except TypeError:
#        return f

#def eval_lists(l):
#    r = []
#    for i in l:
#        if is_list(i):
#            if i:
#                r.append(lisp_eval(i[0], i[1:]))
#            else:
#                r.append(i)
#        else:
#            r.append(i)
#    return r

# Utilities functions
def eval_maths(l):
    if l[0] in vars:
        l[0] = vars[l[0]]
    if l[2] in vars:
        l[2] = vars[l[2]]
    if isinstance(l[0], int) & isinstance(l[2], int):
        if l[1] == '+':
            return l[0] + l[2]
        if l[1] == '-':
            return l[0] - l[2]
        if l[1] == '*':
            return l[0] * l[2]
        if l[1] == '/':
            return l[0] / l[2]
        return 'null'
    return 'invalid'

def is_list(l):
    return type(l) == type([])

def lisp_str(l):
    if type(l) == type([]):
        if not l:
            return "()"
        r = "("
        for i in l[:-1]:
            r += lisp_str(i) + " "
        r += lisp_str(l[-1]) + ")"
        return r
    elif l is True:
        return "#t"
    elif l is False:
        return "#f"
    elif l is None:
        return 'nil'
    else:
        return str(l)

# BNF

def p_exp_atom(p):
    'exp : atom'
    p[0] = p[1]

def p_exp_qlist(p):
    'exp : quoted_list'
    p[0] = p[1]

def p_exp_call(p):
    'exp : call'
    p[0] = p[1]

def p_quoted_list(p):
    'quoted_list : QUOTE list'
    #p[0] = p[2]
    p[0] = ["quote"] + [p[2]]

def p_list(p):
    'list : LPAREN items RPAREN'
    p[0] = p[2]

def p_items(p):
    'items : item items'
    print p[1], p[2]
    p[0] = [p[1]] + p[2]
    print p[0]

def p_items_empty(p):
    'items : empty'
    p[0] = []

def p_empty(p):
    'empty :'
    pass

def p_item_atom(p):
    'item : atom'
    p[0] = p[1]

def p_item_list(p):
    'item : list'
    p[0] = p[1]

def p_item_list(p):
    'item : quoted_list'
    p[0] = p[1]

def p_item_call(p):
    'item : call'
    p[0] = p[1]

def p_item_empty(p):
    'item : empty'
    p[0] = p[1]

def p_callMath(p):
    'call : item MATH item'
    p[0] = eval_maths([p[1], p[2], p[3]])

def p_callLet(p):
    'call : item Eq item'
    vars[p[1]] = p[3]
    p[0] = p[3]

def p_defFunc(p):
    '''call : FUNC item LPAREN items RPAREN LCURLY item MATH item RCURLY
            | FUNC item LPAREN items RPAREN LCURLY item MATH item MATH item RCURLY
    '''
    print 'matched defFunc'
    functions[p[2]] = {}
    functions[p[2]]['VarVars'] = []
    functions[p[2]]['vars'] = {}
    for i in p[4]:
        functions[p[2]]['vars'][i] = 0
        functions[p[2]]['VarVars'].append(i)
    if len(p) == 11:
        functions[p[2]]['function'] = [p[7], p[8], p[9]]
    if len(p) == 13:
        functions[p[2]]['function'] = [p[7], p[8], p[9], p[10], p[11]]
    print functions[p[2]]
    #functions[p[2]]['VarVars'] = (functions[p[2]]['vars'].keys())
    p[0] = p[2]

def p_callFunc(p):
    'call : item LPAREN items RPAREN'
    if p[1] in functions:
        print 'calling', p[1], 'with', p[3]
        mathList = []
        for i in range (0, len(p[3])):
            functions[p[1]]['vars'][functions[p[1]]['VarVars'][i]] = p[3][i]
        print functions[p[1]]['vars']
        for i in functions[p[1]]['function']:
            if i in functions[p[1]]['vars']:
                i = functions[p[1]]['vars'][i]
            mathList.append(i)
        p[0] = eval_maths(mathList)
    else:
        print 'nope nope nope'


def p_print(p):
    'call : PRINT items'
    s = ''
    for i in p[2]:
        if i in vars:
            i = vars[i]
        s += str(i)
    print s


def p_atom_simbol(p):
    'atom : SIMB'
    p[0] = p[1]

def p_atom_bool(p):
    'atom : bool'
    p[0] = p[1]

def p_atom_num(p):
    'atom : NUM'
    p[0] = p[1]

def p_atom_math(p):
    'atom : MATH'
    p[0] = p[1]

def p_atom_word(p):
    'atom : TEXT'
    p[0] = p[1]

def p_atom_str(p):
    'atom : STRING'
    p[0] = p[1]

def p_atom_empty(p):
    'atom :'
    pass

def p_true(p):
    'bool : TRUE'
    p[0] = True

def p_false(p):
    'bool : FALSE'
    p[0] = False

def p_nil(p):
    'atom : NIL'
    p[0] = None

# Error rule for syntax errors
def p_error(p):
    print "Syntax error!! ",p

# Build the parser
# Use this if you want to build the parser using SLR instead of LALR
# yacc.yacc(method="SLR")
yacc.yacc()


