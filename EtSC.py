from yacc import yacc, lisp_str
import cmd


with open('testfile.txt', 'r') as content_file:
    content = content_file.read()
s = ''
lines = []
for i in content:
    if i == '\n':
        lines.append(s)
        s = ''
    else:
        s += i
lines.append(s)
for i in lines:
    result = yacc.parse(i)
    if isinstance(result, str):
        if result[len(result) - 2] + result[len(result) - 1] == '**':
            result = yacc.parse(result[0 : len(result) - 2])
    if result != None:
        print (result)