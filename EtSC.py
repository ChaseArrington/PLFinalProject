from yacc import yacc, lisp_str
import cmd


with open('testfile.txt', 'r') as content_file:
    content = content_file.read()
print content
s = ''
lines = []
for i in content:
    if i == '\n':
        lines.append(s)
        s = ''
    else:
        s += i
lines.append(s)
print lines
for i in lines:
    result = yacc.parse(i)
    if isinstance(result, str):
        if result[len(result) - 2] + result[len(result) - 1] == '**':
            #print result[0 : len(result) - 2]
            result = yacc.parse(result[0 : len(result) - 2])
    if result != None:
        print (result)

#result = yacc.parse(content)
#.print result