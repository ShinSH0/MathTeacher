from Core import *
from MTlist import latexdict
import os
def mkdir(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)
def getRepresentLatex(obj):
    if isinstance(obj, list):
        return obj[0]
    else:
        return obj
for key in latexdict.keys():
    dirname ='image/'+key
    mkdir(dirname)
    for i in range(len(latexdict[key])):
        imgname = dirname+ '/'+str(i)+'.png'
        latexx = getRepresentLatex(latexdict[key][i]) 
        #print(latexx, imgname)
        try:
            latex2img(latexx,filename=imgname,imgsize=(50,50))
        except:
            print("Error : ", latexx, " | ",imgname)