from MathTeacher4 import *
from sympy import *
def do_examples(exm_list, only=None,getparam=False,row =0):
    for eq in exm_list:
        if only is not None and exm_list.index(eq) != only:
            continue
        print("Equation",exm_list.index(eq),": ",eq)
        if getparam :
            print(parsed_list[row])
            print("params: ",getparam_list(eq,parsed_list,row,begin,end))
        else:
            sympyform = convertall(eq,parsed_list,form_list,eval_list,begin,end)
            print( "SympyForm: ",sympyform)
            print( "Interpreted: ",interpret(sympyform))
if __name__ == '__main__':
    begin= '<'
    end = '>'
    symbs = [['x','y','z','k','n','m'],['A','B'],['f','g','h']]
    parsed_list,form_list, eval_list = init(begin,end,"function2.txt",symbs)
    
    #print(parsed_list)

    exm_list = [
    r"\\left( \\begin{array} { l } { x } \\\\ { y } \\\\ { z } \\end{array} \\right) = \\left( \\begin{array} { c } { 6 } \\\\ { - 4 } \\\\ { 27 } \\end{array} \\right)" 
    ,r"\int _ { 0 } ^ { 1 } x e ^ { 2 x - 1 } d x"    
        
    ,r"\int \frac { 4 x } { \sqrt { x ^ { 2 } + 1 } } d x"
    ,r"\int \frac { 4 x } { \sqrt { x ^ { 2 } + 1 } } d x  = 0"
    ,r"2 \operatorname {cos} x ( \operatorname {sin} x + \operatorname {cos} x )"
    ,r"\operatorname {cos} (x ** 2+ 1 + 2) ( \operatorname {sin} x + \operatorname {cos} x )"
    ,r"\operatorname { lim } _ { x \rightarrow 3 } ( \frac { x ^ { 2 } + 9 } { x - 3 } )"
    ,r"\operatorname { lim } _ { x \rightarrow 0 + } ( \frac { \operatorname {sin} x } { x } )"
    ,r"\operatorname { lim } _ { x \rightarrow \frac { 1 } { 2 } + } \frac { \operatorname {sin} x } { x } = 3"
    ,r"\frac { \operatorname {sin} x } { x }"
    ,"\\sum _ { k = 1 } ^ { 5 }  k x + 3 "
    ,"\\sum _ { k = 1 } ^ { 5 } k x + 3 = \\frac { 2 } { 7 }"
    ,"\\prod _ { k = 1 } ^ { 5 } k x + 3 = \\frac { 2 } { 7 }"
    ,r"[ \frac { n ( n + 1 ) } { 2 } ] ^ { 2 }"
    ,"\\operatorname { lim } _ { x \\rightarrow 0 } \\frac { \\operatorname { sin } ( x ) } { x }"]
    
    #{ lim } 
    #do_examples(exm_list)
    #latexeq = img2latex('prod.png')    
    # latexeq = r"\operatorname{ lim } _ { x \rightarrow \frac { 1 } { 2 } + } \frac { \operatorname{sin} x } { x } = 3"
    #latexeq = "\\operatorname { lim } _ { x \\rightarrow 0 } \\frac { \\operatorname { sin } ( x ) } { x }"
    #latexeq = r"x \exe e ^ {1} x y"
    latexeq = r"x \exe e e e1e e"
    latexeq = r"exp(1)exp(1) exp(1) e e e e e "
    latexeq = r"exp(1)"
    latexeq = r"x (x+1) (y) z"
    
    #latexeq = r"1 / 2"
    #latexeq= r"\\operatorname {lim} _ { x \to 5 } "
    #latexeq = r"\lim _ { x \to 5 }"
    #latexeq = r"\left(\begin{array}{lll}{ 1 } & { 1 } & { 1 } \\ { 0 } & { 2 } & { 5 } \\ { 2 } & { 5 } &{- 1}\end{array}\right)"
    row =6
    print("latexeq len:", len(latexeq))
    if isinstance(row,list): 
        row=row[0]
        print(parsed_list[row])
        print("len: ",getlen(latexeq,parsed_list,row,begin,end))
    elif row is not None and row != -1:
        print(parsed_list[row])
        print("params: ",getparam_list(latexeq,parsed_list,row,begin,end))
        
        print("converted: ",convert(latexeq,parsed_list,form_list,eval_list,begin,end,row))
        print("convertedall: ",convertall(latexeq,parsed_list,form_list,eval_list,begin,end))
    else:
        print("convertedall: ",convertall(latexeq,parsed_list,form_list,eval_list,begin,end))
        

    # try:
    #     sympyform =''
    #     sympyform =  convertall(latexeq,parsed_list,form_list,eval_list,begin,end)
    #     print(sympyform)
    # except MyException as e:
    #     print(e.msg)
    #     print("Convert Failed")
    #     pass
    # try:
    #     answer = interpret(sympyform)
    #     print(answer)
    # except MyException as e:
    #     print(e.msg)
    #     print("Solving Failed")
    #     pass
    try:
        #latex2img(answer,filename='answer.png')
        pass
    except:
        pass
    
