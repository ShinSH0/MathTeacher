def getInfo(key, idx):
    obj = latexdict[key][idx]
    if idx == 0:
        print("DaePyo Image")
    elif isinstance(obj, list):
        return obj
    else:
        return [obj, obj, len_0]
len_3 = len(' }{  }{  }')
len_2 = len(' }{  }')
len_1 = len(' }')
len_0 = len('')
latexdict = {
    'Space':
    [
        r'\square \quad \square',
        [r'\square \! \square', r'\! ', len_0],
        [r'\square \, \square', r'\, ', len_0],
        [r'\square \: \square', r'\: ', len_0],
        [r'\square \; \square', r'\; ', len_0],
        [r'\square \quad \square', r'\quad ', len_0],
        [r'\square \qquad \square', r'\qquad ', len_0]
    ],
    'Root Fraction':
    [
        r'\frac { \sqrt { \square } }{ \sqrt { \square } } ',
        [r'\sqrt { \square }', r'\sqrt {  }', len_1],
        [r'\sqrt [ \square ]{ \square }', r'\sqrt [  ]{  }', len_2],
        [r'\frac { \square }{ \square }', r'\frac {  }{  }', len_2],
        [r'\frac { \sqrt { \square } }{ \sqrt { \square } }',  r'\frac { \sqrt {  } }{ \sqrt {  } }', len(r'} }{ \sqrt {  } }')]
    ],
    'Escaped':
    [
        r'\backslash',
        [r'\#', r'\# ', len_0],
        [r'\$', r'\$ ', len_0],
        [r'\%', r'\% ', len_0],
        [r'\&', r'\& ', len_0],
        [r'\string~', r'\string~ ', len_0],
        [r'\_', r'\_ ', len_0],
        [r'\string^', r'\string^ ', len_0],
        [r'\backslash', r'\backslash ', len_0],
        [r'\{', r'\{ ', len_0],
        [r'\}', r'\} ', len_0]
    ],
    'Subscript':
    [
        r'\square^{ \square} ',
        [r'\square^{ \square} ', r'^{  }', len_1],
        [r'\square_{ \square} ', r'_{  }', len_1],
        [r'\square_{ \square }^{ \square }', r'_{  }^{  }', len_2+1],
        [r'_{ \square }\square_{ \square }',
            r'_{  }  _{  }', len(r' }  _{  }')],
    ],
    'Integral':
    [
        r'\int _{ \square }^{ \square }',

        [r'\int ', r'\int ', len_0],
        [r'\int _{ \square }^{ \square }', r'\int _{  }^{  }', len_2+1],

        [r'\iint ', r'\iint ', len_0],
        [r'\iint _{ \square }^{ \square }', r'\iint _{  }^{  }', len_2+1],

        [r'\iiint ', r'\iiint ', len_0],
        [r'\iiint _{ \square }^{ \square }', r'\iiint _{  }^{  }', len_2+1],

        [r'\oint ', r'\oint ', len_0],
        [r'\oint _{ \square }^{ \square }', r'\oint _{  }^{  }', len_2+1],

        [r'\oiint ', r'\oiint ', len_0],
        [r'\oiint _{ \square }^{ \square }', r'\oiint _{  }^{  }', len_2+1],

        [r'\oiiint ', r'\oiiint ', len_0],
        [r'\oiiint _{ \square }^{ \square }', r'\oiiint _{  }^{  }', len_2+1],
    ],
    'Sum':
    [
        r'\sum \limits _{ \square }^{ \square }',
        [r'\sum ', r'\sum ', len_0],
        [r'\sum \limits _{ \square }^{ \square }', r'\sum \limits _{  }^{  }', len_2+1],
        [r'\prod ', r'\prod ', len_0],
        [r'\prod \limits _{ \square }^{ \square }', r'\prod \limits _{  }^{  }', len_2+1],
        [r'\bigcup ', r'\bigcup ', len_0],
        [r'\bigcup \limits _{ \square }^{ \square }', r'\bigcup \limits _{  }^{  }', len_2+1],
        [r'\bigcap ', r'\bigcap ', len_0],
        [r'\bigcap \limits _{ \square }^{ \square }', r'\bigcap \limits _{  }^{  }', len_2+1],
        [r'\bigvee ', r'\bigvee ', len_0],
        [r'\bigvee \limits _{ \square }^{ \square }', r'\bigvee \limits _{  }^{  }', len_2+1],
        [r'\bigwedge ', r'\bigwedge ', len_0],
        [r'\bigwedge \limits _{ \square }^{ \square }', r'\bigwedge \limits _{  }^{  }', len_2+1]
    ],
    "Triangle Function":
    [
        r'\sin ',
        [r'\cos ', r'\cos ', len_0],
        [r'\cot ', r'\cot ', len_0],
        [r'\csc ', r'\csc ', len_0],
        [r'\sec ', r'\sec ', len_0],
        [r'\sin ', r'\sin ', len_0],
        [r'\tan ', r'\tan ', len_0]
    ],
    "Log Limit":
    [
        r'\lim \limits _{ \square \to \square }',
        [r'\log _{ \square }', r'\log _{  }', len_1],
        [r'\lim \limits _{ \square }', r'\lim \limits _{  }', len_1],
        [r'\lim \limits _{ \square \to \square }', r'\lim \limits _{  \to  }', len(r' \to  }')],
        [r'\ln ', r'\ln ', len_0],
        [r'\min \limits _{ \square }', r'\min \limits _{  }', len_1],
        [r'\max \limits _{ \square }', r'\max \limits _{  }', len_1]
    ],
    
    "Greek":
    [
        r'\alpha ',
        '\\alpha ', 
        '\\beta ', 
        '\\gamma ', 
        '\\delta ', 
        '\\epsilon ', 
        '\\zeta ', 
        '\\eta ', 
        '\\theta ', 
        '\\kappa ', 
        '\\lambda ', 
        '\\mu ', 
        '\\xi ', 
        '\\pi ', 
        '\\rho ', 
        '\\tau ',
        '\\sigma ', 
        '\\phi ', 
        '\\varphi ',
        '\\chi ', 
        '\\psi ', 
        '\\omega ', 
        '\\Gamma ', 
        '\\Delta ', 
        '\\Theta ', 
        '\\Lambda ', 
        '\\Xi ', 
        '\\Phi ', 
        '\\Psi ', 
        '\\Omega '
    ],
    "Accent":
    [
        r'\hat \square ',
        [r'\hat \square ', r'\hat ',len_0],
        [r'\dot \square ', r'\dot ', len_0 ],
        [r'\vec \square ',r'\vec ',len_0],
        [r'\tilde \square ',r'\tilde ',len_0],
        [r'\overline \square ',r'\overline ',len_0]
    ],
    "Arrow":
    [
        r'\leftarrow ',
        r'\leftarrow ', 
        r'\rightarrow ',
        r'\Leftarrow ',  
        r'\Rightarrow ', 
        r'\leftrightarrow ',   
        r'\Leftrightarrow ',
        r'\mapsto '
    ],
    "Symbol":
    [
        r'\therefore ',
        r'\therefore ',
        r'\because ',
        r'\angle ', 

        r'\dots ', 
        r'\cdots ', 
        r'\prime ',
        r'\vdots ',

        r'\forall ',
        r'\infty ', 
        r'\hbar ', 
        r'\emptyset ',
        r'\nabla '
        r'\exists ',  
        r'\ell ', 
        r'\bot ', 
        r'\partial '
    ],
    "Brace":
    [
        r"\left ( \square \right )",
        [r"\left ( \square \right )",r"\left ( \right )",len(r" \right )")],
        [r"\left [ \square \right ]",r"\left [ \right ]",len(r" \right ]")],
        [r"\left \{ \square \right \}",r"\left \{ \right \}",len(r" \right \}")],
        [r"\left \lfloor \square \right \rfloor",r"\left \lfloor \right \rfloor",len(r" \right \rfloor")],
        [r"\left \lceil \square \right \rceil",r"\left \lceil \right \rceil",len(r" \right \rceil")],
        [r"\left \langle \square \right \rangle",r"\left \langle \right \rangle",len(r" \right \rangle")],
        [r"\left | \square \right |",r"\left | \right |",len(r" \right |")],
        [r"\left \| \square \right \|",r"\left \| \right \|",len(r" \right \|")]
    ],
    "Relational":
    [
        r'< ', 
        r'= ', 
        r'\neq ', 
        r'< ', 
        r'> ', 
        r'\leq  ', 
        r'\geq ', 
        r'\subset ', 
        r'\supset ', 
        r'\subseteq ', 
        r'\supseteq ', 
        r'\in ', 
        r'\ni ', 
        r'\notin ', 
        r'\equiv ', 
        r'\sim ', 
        r'\simeq ', 
        r'\approx ', 
        r'\cong ', 
        r'\propto ', 
        r'\perp ', 
        r'\parallel '
    ],
    "Operator":
    [
        r'+ ', 
        r'\pm ', 
        r'\mp ', 
        r'\times ', 
        r'\div ', 
        r'\ast ', 
        r'\star ', 
        r'\circ ', 
        r'\cdot ', 
        r'+ ', 
        r'\cap ', 
        r'\cup ', 
        r'\vee ', 
        r'\wedge ', 
        r'- ', 
        r'\oplus ', 
        r'\otimes ', 
        r'\dagger '
    ],
    "Array":
    [
        r'\begin{array} { l } \cdots \\ \cdots \end{array}',
        [r'\begin{array} { l } \cdots \\ \cdots \end{array}',r'\begin{array}  \end{array}', len(r' \end{array}')]    
    ]

}

def printList(string):
    li =  [i+' ' for i in string.split('\n')]
    for elem in li:
        print('r\''+elem+'\', ')
