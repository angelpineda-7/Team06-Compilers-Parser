from ply.lex import lex
from ply.yacc import yacc
from gui import GUI
import tkinter as tk
from tkinter import filedialog
# --- Tokenizer

reserved = {
   'if' : 'IF',
   'int' : 'INT',
   'for' : 'FOR',
}
error=False
# All tokens must be named in advance.
tokens = ['IDENTIFICATOR','CONSTANT','COMMENT','LPAREN', 'RPAREN','ASSIGMENTEQUAL','SEMICOLON','COMPARATOR','OPERATOR','ANDOR', 'KEYWORD' ]+list(reserved.values())


# Ignored characters
t_ignore = ' \t'

# Token matching rules are written as regexs
t_COMPARATOR=r'==|<=|>=|<|>'
t_ANDOR=r'&&|\|\|'
t_OPERATOR = r'-|\+|\*|/'
t_SEMICOLON = r';'
t_IDENTIFICATOR = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_ASSIGMENTEQUAL=r'\='

def t_KEYWORD(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    
    if t.value in list(reserved.keys()):
        t.type = reserved.get(t.value,'KEYWORD')    # Check for reserved words
        return t
    else:
        t.type="IDENTIFICATOR"
        return t

def t_COMMENT(t):
    r'//.*'
    pass
    # No return value. Token discarded
    
def t_CONSTANT(t):
    r'\d+'
    t.value = int(t.value)
    return t

# A function can be used if there is an associated action.
# Write the matching regex in the docstring.
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Ignored token with an action associated with it
def t_ignore_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

# Error handler for illegal characters
def t_error(t):
    if(t.type!=None):
        print(f'Illegal character {t.value[0]!r}')
        t.lexer.skip(1)

# Build the lexer object

# --- Parser
#
# Write functions for each grammar rule which is
# specified in the docstring.
def p_start(p):
    '''
    START : assigment
          | for
          | if
    '''
    # p is a sequence that represents rule contents.
    #
    # expression : term PLUS term
    #   p[0]     : p[1] p[2] p[3]
    # 
    p[0] = p[1]

def p_assignStart(p):
    '''
    assigment : INT afirst SEMICOLON
    '''
    p[0] = ('ASSIGMENT',p[1],p[2],p[3])

def p_assignFirst(p):
    '''
    afirst : IDENTIFICATOR ASSIGMENTEQUAL asecond
    '''
    p[0] = (p[1], p[2], p[3])

def p_assignSecond(p):
    '''
    asecond : CONSTANT
            | IDENTIFICATOR
            | operation
    '''
    p[0] = p[1]

def p_operation(p):
    '''
    operation : operationfirst
              | increment
    '''
    p[0] = p[1]

def p_operationfirst(p):
    '''
    operationfirst : asecond OPERATOR operationfirst
                    | asecond OPERATOR asecond
    '''
    p[0] = (p[1],p[2],p[3])

def p_increment(p):
    '''
    increment : IDENTIFICATOR OPERATOR OPERATOR
    '''
    p[0] = ('INCREMENT',p[1],p[2],p[3])

def p_for(p):
    '''
    for : FOR LPAREN ffirst SEMICOLON comparison SEMICOLON operation RPAREN
    '''
    p[0] = ('FOR',p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8])

def p_ffirst(p):
    '''
    ffirst : assigmentnosemi
           | asecond
    '''

    p[0]=p[1]
def p_assigmentnosemi(p):
    '''
    assigmentnosemi : INT afirst
    '''

    p[0]=(p[1],p[2])

def p_comparison(p):
    '''
    comparison : comparison ANDOR comparison
               | asecond COMPARATOR asecond
    '''  
    p[0]=(p[1],p[2],p[3])

def p_if(p):
    '''
    if : IF LPAREN comparison RPAREN
    '''
    p[0]=(p[1],p[2],p[3],p[4])

lineCounter=0
lineError=0
def p_error(p):
    global lineCounter
    global lineError
    global error
    lineError=lineCounter
    error=True

# Build the parser


# Parse an expression


def compParser(file_path):
    global lineCounter
    global error
    parser = yacc()
    lexer = lex()
    file=open(file_path,"r")
    lines=file.readlines()
    for line in lines:
        lineCounter=lineCounter+1
        result= parser.parse(line)
        if result!=None:
            print(result)
    if error==False:
        GUI.mensaje("Success!","The parsing process has been completed successfully ")
    else:
        GUI.mensaje("Error",f"Parsing failed. Error @ line {lineError}")

def main():
    gui=GUI()
    opcion=gui.elegir()
    if opcion==1:
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        if file_path.endswith(".c"):
            print(file_path)
            compParser(file_path)
        elif file_path=="":
            gui.mensaje("Error","Archivo no seleccionado")
            main()
        else:
            gui.mensaje("Error","Archivo no soportado")
            main()

main()