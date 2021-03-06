# -*- coding: utf-8 -*-
from yacc import yacc, lisp_str
import cmd

class Cobra(cmd.Cmd):     # See https://docs.python.org/2/library/cmd.html
    """
    MiniLisp evalúa expresiones sencillas con sabor a lisp, 
    más información en http://www.juanjoconti.com.ar
    """

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = ">>> "
        self.intro  = "CobraCmdLine"

    def do_exit(self, args):
        """Exits from the console"""
        return -1

    def do_EOF(self, args):
        """Exit on system end of file character"""
        print "End"
        return self.do_exit(args)

    def do_help(self, args):
        print self.__doc__

    def emptyline(self):    
        """Do nothing on empty input line"""
        pass

    def default(self, line):       
        """Called on an input line when the command prefix is not recognized.
           In that case we execute the line as Python code.
        """
        result = yacc.parse(line)
        if isinstance(result, str):
            if result[len(result) - 2] + result[len(result) - 1] == '**':
                #print result[0 : len(result) - 2]
                result = yacc.parse(result[0 : len(result) - 2])

        if result != None:
            print (result)
##### BugList
### using exec and java streams returns "None" rather, though it does function
### trying to condense item Math item returns a list 'invalid'


if __name__ == '__main__':
        ml = Cobra()
        ml.cmdloop()     # See https://docs.python.org/2/library/cmd.html
