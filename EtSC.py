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
    print yacc.parse(i)

#result = yacc.parse(content)
#.print result