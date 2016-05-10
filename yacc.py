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

class function(object):
    def f(self):
        data = {
            'name': 'Rita',
            '$name': lambda x: data.update({'name': x}),
            'varVals': {},
            '$varVals': lambda x: data.update({'varVals': x}),
            'varL': [],
            '$varL': lambda x: data.update({'varL': x}),
            'equation': ['a', '+', 'b'],
            '$equation': lambda x: data.update({'equation': x}),
        }
        def cf(self, d):
            if d in data:
                return data[d]
            else:
                return None
        return cf
    run = f(1)

s1 = function()


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

#def p_exp_qlist(p):
#    'exp : quoted_list'
#    p[0] = p[1]

def p_exp_call(p):
    'exp : call'
    p[0] = p[1]

#def p_quoted_list(p):
#    'quoted_list : QUOTE list'
#    #p[0] = p[2]
#    p[0] = ["quote"] + [p[2]]



def p_items(p):
    '''items : item items
    '''
    #print p[1], p[2]
    p[0] = [p[1]] + p[2]
    #print p[0]

def p_items_empty(p):
    'items : empty'
    p[0] = []

def p_empty(p):
    'empty :'
    pass

def p_item_atom(p):
    'item : atom'
    p[0] = p[1]

#def p_item_list(p):
#    'item : list'
#    p[0] = p[1]

#def p_item_qlist(p):
#    'item : quoted_list'
#    p[0] = p[1]

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

def p_list(p):
    'call : LBrack items RBrack'
    print 'saw list'
    print p[2]
    p[0] = p[2]

def p_defFunc(p):
    '''call : FUNC item LPAREN items RPAREN LCURLY item MATH item RCURLY
            | FUNC item LPAREN items RPAREN LCURLY item MATH item MATH item RCURLY
            | FUNC item LPAREN items RPAREN LCURLY items RCURLY
    '''
    #print 'matched defFunc'
    functions[p[2]] = function()
    a = {}
    b = []
    c = []
    for i in p[4]:
        a[i] = 0
        b.append(i)
    functions[p[2]].run('$varVals')(a)
    functions[p[2]].run('$varL')(b)
    if len(p) == 11:
        #c = [p[7], p[8], p[9]]
        c = p[7 : 10]
    if len(p) == 13:
        c = p[7 : 12]
    functions[p[2]].run('$equation')(c)
    #print functions[p[2]].run('equation')
    #if len(p) == 13:
    #    functions[p[2]]['function'] = [p[7], p[8], p[9], p[10], p[11]]
    #print functions[p[2]]
    #functions[p[2]]['VarVars'] = (functions[p[2]]['vars'].keys())
    p[0] = p[2]

def p_callFunc(p):
    'call : item LPAREN items RPAREN'
    if p[1] in functions:
        #print 'calling', p[1], 'with', p[3]
        funString = ''
        a = functions[p[1]].run('varVals')
        #print a
        b = functions[p[1]].run('varL')
        #print b
        c = functions[p[1]].run('equation')
        #print c
        for i in range (0, len(p[3])):
            a[b[i]] = p[3][i]

        #print c
        for i in c:
            if i in a:
                i = a[i]
            funString += str(i)
        #print funString
        funString += '**'
        p[0] = funString
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



#def p_atom_simbol(p):
#    'atom : SIMB'
#    p[0] = p[1]

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


