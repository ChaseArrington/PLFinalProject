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

#s1 = function()


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
    if (isinstance(l[0], int) | isinstance(l[0], float)) & (isinstance(l[2], int) | isinstance(l[2], float)) :
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

def p_exp_call(p):
    'exp : call'
    p[0] = p[1]

def p_items(p):
    'items : item items'
    p[0] = [p[1]] + p[2]

def p_items_empty(p):
    'items : empty'
    p[0] = []


def p_empty(p):
    'empty :'
    pass

def p_item_atom(p):
    'item : atom'
    p[0] = p[1]

def p_item_call(p):
    'item : call'
    p[0] = p[1]

def p_item_math(p):
    'item : MATH'
    p[0] = p[1]

def p_item_empty(p):
    'item : empty'
    p[0] = p[1]

def p_callMath(p):
    'call : item MATH item'
    p[0] = eval_maths([p[1], p[2], p[3]])

def p_callLet(p):
    'call : TEXT Eq item'
    vars[p[1]] = p[3]
    p[0] = p[3]

def p_selectList(p):
    '''call : SELECT ALL item
            | SELECT NUM NUM NUM NUM item
            | SELECT NUM NUM NUM NUM item NUM LESS NUM AND NUM GREAT NUM'''
    if p[2] == 'all':
        print "\nselect * from " + str(p[3]) + ': ,' + str(p[3])
        p[0] = vars[p[3]]
    else:
        if len(p) == 7:
            a=[]
            for i in vars[p[6]][1:]:
                a.append([i[p[2]],i[p[3]],i[p[4]],i[p[5]]])
            print "\n select "+str(vars[p[6]][0][p[2]])+', '+str(vars[p[6]][0][p[3]])+', '\
                  +str(vars[p[6]][0][p[4]])+', '+str(vars[p[6]][0][p[5]])+' from '+str(p[6])+': '
            p[0] = a
        if len(p) == 14:
            b=[]
            if p[8] == '<' and p[12] == '>':
                for i in vars[p[6]][1:]:
                    if i[p[7]] < p[9] and i[p[11]] > p[13]:
                        b.append([i[p[2]],i[p[3]],i[p[4]],i[p[5]]])
                print "\n select "+str(vars[p[6]][0][p[2]])+', '+str(vars[p[6]][0][p[3]])+', '\
                      +str(vars[p[6]][0][p[4]])+', '+str(vars[p[6]][0][p[5]])+' from '+str(p[6])+' where '+\
                      str(vars[p[6]][0][p[7]]), p[8], p[9], p[10], str(vars[p[6]][0][p[7]]),p[12], p[13]
                p[0] = b

def p_list(p):
    'call : LBrack items RBrack'
    p[0] = p[2]

def p_defFunc(p):
    '''call : FUNC item LPAREN items RPAREN LCURLY item MATH item RCURLY
            | FUNC item LPAREN items RPAREN LCURLY item MATH item MATH item RCURLY
            | FUNC item LPAREN items RPAREN LCURLY EXEC items RCURLY
    '''
    functions[p[2]] = function()
    a = {}
    b = []
    c = []
    for i in p[4]:
        a[i] = 0
        b.append(i)
    functions[p[2]].run('$varVals')(a)
    functions[p[2]].run('$varL')(b)
    c = p[7 : len(p) - 1]
    functions[p[2]].run('$equation')(c)
    p[0] = p[2]

def p_callFunc(p):
    'call : item LPAREN items RPAREN'
    if p[1] in functions:
        funString = ''
        a = functions[p[1]].run('varVals')
        b = functions[p[1]].run('varL')
        c = functions[p[1]].run('equation')
        for i in range (0, len(p[3])):
            a[b[i]] = p[3][i]
        for i in c:
            if i in a:
                i = a[i]
            funString += str(i)
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

def p_printLine(p):
    'call : PRINTLINE STATEMENT'
    s = p[2]
    print '\n' + s[1:]

def p_exec(p):
    'item : EXEC items'
    from java.lang import Math
    s = ''
    for i in p[2]:
        i = str(i)
        i = i.replace('[', '(')
        i = i.replace(']', ')')
        s += str(i)
    p[0] = eval(compile(s, 'None', 'single'))


def p_date(p):
    'item : DATE'
    p[0] = p[1]

def p_atom_bool(p):
    'atom : bool'
    p[0] = p[1]

def p_atom_num(p):
    'atom : NUM'
    p[0] = p[1]

def p_atom_FLOAT(p):
    'atom : NUM DOT NUM'
    p[0] = float(str(p[1]) + str(p[2]) + str(p[3]))

def p_atom_math(p):
    'atom : MATH'
    p[0] = p[1]

def p_atom_word(p):
    'atom : TEXT'
    p[0] = p[1]

def p_atom_str(p):
    'atom : STRING'
    p[0] = p[1]

def p_atom_dot(p):
    'atom : DOT'
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


