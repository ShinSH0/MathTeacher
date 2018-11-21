from __future__ import unicode_literals
from functools import reduce
import datetime
from operator import itemgetter
#latex 2img에 필요함
import io
from PIL import Image, ImageOps
import matplotlib.pyplot as plt
import operator
#img 2 latex에 필요함
import sys
import base64   
import requests
import json
import matplotlib.pyplot as plt
from sympy import *
from matplotlib import rcParams

#==== LaTex를 Image로 변환하는 데 필요한 폰트, 패키지등의 설정이다.
rcParams['font.family'] = 'NanumGothic'#'sans-serif'
rcParams['text.usetex'] = True
rcParams['text.latex.unicode'] = True
rcParams['text.latex.preamble'] = [r'\usepackage{mathtools}',r'\usepackage{kotex}',r'\usepackage{txfonts}']
#=============

begin_end_parsed=[]
primitive = (int, str, bool, float) #파이썬의 기본적인 타입들 리스트
argleft=['{','[','('] #여는 괄호들의 리스트
argright=['}',']',')'] #닫는 괄호들의 리스트
maximum_call = 2
img2latex_call = 0
lendict = {} #getlen을 메모이제이션으로 구현하기 위해 필요한 변수, lendict가 있어서 getlen의 시간복잡도가 O(len(string)*len(parsed_list))가 된다.
trianglefunction = ['sin','cos','tan','csc'] #삼각함수들
defaultfunction = ['integrate','limit','sqrt','exp','Sum','Matrix','Prod'] +trianglefunction #기본적으로 sympy에서 정의된 함수들 
triangleseperator = ['\\'+i for i in trianglefunction]
defaultmatrix = []
defaultcomplex = ['e']
alphabet = [chr(i) for i in range(ord('A'), ord('Z')+1)]+[chr(i) for i in range(ord('a'), ord('z')+1)]
seperator = ['+','-',',']
relationals = ['\\<','\\>','=',r'\leq',r'\geq'] # 관계식 종류 leq는 작거나 같음, geq는 크거나 같음이다.
escaped_relationals = []
escaped_seperator = []
matrixsize = []


# 커스텀 Exception의 메시지는 에러의 발생원인을 잘 담고 있어서 유지보수가 쉽다.
class MyException(Exception): 
    def __init__(self, msg):
        self.msg = msg

def getrange(range_list):
    first = range_list[0]
    last = range_list[-1]
    if isinstance(first,list):
        first = getrange(first)
    if isinstance(last,list):
        last = getrange(last)
    return range(first.start,last.stop)



def replace_parts(string, range_list, str_list):
    replaced_str = []
    i=0
    for _range, _str in zip(range_list, str_list):
        if isinstance(_str,list):
            if len(_str) == 0:
                continue
            start,stop = (lambda x: (x.start, x.stop)) (getrange(_range))
            replaced_str.append(string[i:start])
            #range에 전부 start를 빼기보다는 stop
            replaced_str.append(replace_parts(string[:stop],_range,_str)[start:])
            i = stop
        else:
            replaced_str.append(string[i:_range.start])
            replaced_str.append(_str)
            i = _range.stop
    return ''.join(replaced_str)

#string의 시작문자열이 str_list에 있다면 그 인덱스를 반환한다.
#ex) getidx("ab", ['a','b']) 는 0을 리턴한다
#ex) getidx("ab", ['c'])는 None을 리턴한다.  
def getidx(string, str_list,begin='',end=''):
    if isinstance(str_list, str):
        str_list = [str_list]

    for idx in range(len(str_list)):
        if isinstance(str_list[idx], list):
            if isinstance(str_list[idx][0],int):  
                if getbool(str_list[idx], string[:1],begin,end):
                    return (idx, 1)
            else:
                idx2 = getidx( string,str_list[idx],begin,end)[0]
                if idx2 is not None:
                    return (idx, len(str_list[idx][idx2]))
        elif string[:len(str_list[idx])] == str_list[idx]:
            return (idx, len(str_list[idx]))
    return (None,None)

def getlen(string, parsed_list,priority_list, row, begin,end,debugflag = False):
    if string in lendict:
        if row in lendict[string] :
            return lendict[string][row]
        else:
            flag_1 = True
            flag_2 = False
    else:
        flag_1 = False
        flag_2 = True
    parsed = [i[0] for i in parsed_list[row]]
    loopback = [i[1] for i in parsed_list[row]]
    noparam = [i[2] for i in parsed_list[row]]
    times = [i[3] for i in parsed_list[row]]
    loopback_len = len(loopback)
    insertidx = [None for i in range(loopback_len)]
    lastlength = None
    notNone = 1
    beforeback = None
    wasjumped = False
    jumprange = range(0)
    prev_flag  =False
    next_flag = False
    prev_idx = None
    prev_idx_len = None
    cnt = [0 for i in range(loopback_len)]
    if getidx(string,[parsed[0]],begin,end)[0] is None:
        raise MyException("'"+str(parsed[0])+"' Must Be First Of String")
    i= 0
    col = 0
    prev = -1
    str_len = len(string)
    waslooped = False
    start =0
    #== 루프시작 ==
    while i < str_len:
        str_list = [parsed_list[i][0][0]  for i in range(len(parsed_list))]
        str_list.insert(row,parsed[col])
        str_list = str_list[prev+1:]
        if next_flag:
            idx = prev_idx - (prev+1)
            idx_len = prev_idx_len
        elif prev_flag:
            idx,idx_len = (None,None)
        else:
            idx,idx_len = getidx(string[i:],str_list,begin,end)
        #디버깅 쵝오
        # if debugflag:
        #     print(string[i:],(str_list[idx], idx+(prev+1))  if idx is not None else None, row,col)
        
        if (idx is None or idx+(prev+1) != row)   and loopback[col] == col and (not isinstance(noparam[col],list) or not col in noparam[col][1]) and noparam[col] and getbool(times[col],cnt[col],begin,end):
            #반복할 문자열의 횟수가 달성됐고, 이제 그 반복할 문자열이 안 나왔다면 들어오는 If문
            waslooped = False
            if insertidx[col] is None:
                insertidx[col] =  notNone
            col+=1
            if col == len(parsed):
                if flag_1:
                    lendict[string][row] = i
                elif flag_2:
                    lendict[string] = {row: i}
                return i
            continue
        if idx is not None :
            if idx == row-(prev+1):
                if (not isinstance(noparam[col], list) or not col in noparam[col][1]) and loopback[col] == col : 
                    repeat_flag = True
                else:
                    repeat_flag = False
                if waslooped:
                    if repeat_flag:
                        #hasparam = False if noparam[col] else True
                        hasparam = False
                    else:
                        hasparam = False if noparam[col][1][beforeback] else True
                else:
                    if isinstance(noparam[col],list):
                        hasparam = False if noparam[col][0] else True
                    else:
                        hasparam = False if noparam[col] else True
                if insertidx[col] is None:
                    insertidx[col] = notNone
                        
                if hasparam or ( not isinstance(parsed[col],list)  and col != 0  and insertidx[col-1] is None and loopback[col-1] == col-1 and not isinstance(noparam[col-1],list) and noparam[col-1] == False):
                    #얘는 궁극의 예외처리를 안하는게 좋을듯
                    pass
                elif string[start:i] != '':
                    if loopback[col] is not None and getbool(times[col],cnt[col],begin,end) and col+1 == len(parsed):
                        if lastlength is not None:
                            if flag_1:
                                lendict[string][row] = lastlength
                            elif flag_2:
                                lendict[string] = {row: lastlength}
                            return lastlength
                        
                        if flag_1:
                            lendict[string][row] = start
                        elif flag_2:
                            lendict[string] = {row: start}
                        return start
                    if flag_1:
                        lendict[string][row] = lastlength
                    elif flag_2:
                        lendict[string] = {row: lastlength}
                    return lastlength
                if isinstance(str_list[idx],list):
                    start=i
                    i+= idx_len
                    if col + 1 < len(parsed) and parsed[col:col+2]  == [argleft, argright]:
                        arg_idx = argleft.index(string[start:start+1])
                        pair_idx = findpair_escaped(string[start:],argleft[arg_idx], argright[arg_idx])
                        if pair_idx is not None:
                            i = start + pair_idx-1
                            start += 1
                            col+=1
                            continue
                    if parsed[col] == escaped_seperator  and col+1 == len(parsed):
                        # 이건 분리기호인 경우 괄호 쌍을 맞추기 위함이다.
                        # 이를 사용하는 변환은 삼각함수, 로그함수 등이 있다.
                        i-= len(string[start:i]) 
                        idx_len -= len(string[start:i]) 
                else:
                    i+= idx_len
                start = i
                
                if loopback[col] is None:
                    col+=1
                    if col == len(parsed):
                        if flag_1:
                            lendict[string][row] = i
                        elif flag_2:
                            lendict[string] = {row: i}
                        return i
                    waslooped = False
                else:
                    cnt[col]+=1
                    if getbool(times[col],cnt[col],begin,end) and col+1 == len(parsed):
                        lastlength = start
                    beforeback = col
                    if times[col][1] == cnt[col]: # <1*1~2>에서 111을 11과 1로 끊어보기 위함
                        col+=1
                        if col == len(parsed):
                            if flag_1:
                                lendict[string][row] = i
                            elif flag_2:
                                lendict[string] = {row: i}
                            return i
                    else:
                        col = loopback[col]
                        waslooped = True
                # start=i
                if wasjumped:
                    for ii in jumprange:
                        insertidx[loopback[ii]]= None
                wasjumped = False
            else:
                idx = idx+(prev+1)
                ciridx = idx - 1 if idx > row else idx #circulated idx
                if next_flag:
#                    next_flag = False
                    pass
                elif priority_list[ciridx] == priority_list[row]: 
                    #우선순위가 같을 때는 자기 자신이 우선이므로, parsed[col:]을 먼저 처리해야한다.
                    prev_flag=True
                    prev_idx = idx
                    prev_idx_len = idx_len
                    continue

                length = getlen(string[i:],parsed_list,priority_list,ciridx,begin,end)
                if length is not None and priority_list[ciridx] <= priority_list[row]:
                    i+= length
                    if i == length : 
                        # 낮지 않은 우선순위 일경우에만 lastlength를 업데이트함.
                        lastlength = i
                    prev = -1
                else:
                    prev = idx
                    if prev+1 == len(parsed_list)+1:
                        if next_flag:
                            prev = -1
                            i+=1
                        else:
                            prev_flag=True
                            prev_idx = idx
                            prev_idx_len = idx_len
                            continue
                next_flag= False
        else:
            #idx,idx_len = getidx(string[i:],parsed[col:],begin,end)
            idx,idx_len = getidx(string[i:],parsed[col:],begin,end)
            if idx is not None:
                idx+=col
            if idx is not None and col != idx:
                if all(map(lambda x: getbool(x[0],x[1],begin,end),[[times[ii],cnt[ii]] for ii in range(col,idx+1)] )):
                    for ii in range(col,idx): #cnt[idx]는 초기화 안한다
                        cnt[ii] = 0
                    jumprange = range(col,idx) 
                    wasjumped = True
                    waslooped = False
                    prev = -1
                    col =idx
                elif all(map(lambda x: getbool(x[0],x[1],begin,end),[[times[ii],cnt[ii]] for ii in range(col,idx)] )):
                    for ii in range(col,idx):
                        cnt[ii] = 0
                    jumprange = range(col,idx) 
                    wasjumped = True
                    waslooped= False
                    prev = -1
                    col = idx
                elif prev_flag:
                    prev_flag= False
                    next_flag=True
                    continue
                else:
                    i+=1
                    prev = -1
                prev_flag= False
            elif prev_flag:
                prev_flag=False
                next_flag = True
                continue
            else:
                idx,idx_len = getidx(string[i:], [begin,end,'\\'+begin,'\\'+end,'\\\\','\\'],begin,end)
                prev = -1
                if idx is None:
                    i+=1
                elif idx == 0:
                    i+=len(begin)  
                elif idx==1:
                    i+=len(end)
                elif idx==5:
                    i+=1
                else: # [2,5) -> 2,3,4
                    i+= len([begin,end,'\\'+begin,'\\'+end,'\\\\','\\'][idx])
    if loopback[col] is not None and getbool(times[col],cnt[col],begin,end) and col+1 == len(parsed):
        if (not isinstance(noparam[col], list) or not col in noparam[col][1]) and loopback[col] == col : 
            repeat_flag = True
        else:
            repeat_flag = False
        if waslooped:
            if repeat_flag:
                hasparam = False
            else:
                hasparam = False if noparam[col][1][beforeback] else True
        else:
            if isinstance(noparam[col],list):
                hasparam = False if noparam[col][0] else True
            else:
                hasparam = False if noparam[col] else True
        if hasparam is False:
            if lastlength is not None:
                if flag_1:
                    lendict[string][row] = lastlength
                elif flag_2:
                    lendict[string] = {row: lastlength}
                return lastlength
            if flag_1:
                lendict[string][row] = start
            elif flag_2:
                lendict[string] = {row: start}
            return start
        if flag_1:
            lendict[string][row] = str_len
        elif flag_2:
            lendict[string] = {row: str_len}
        return str_len
    if flag_1:
        lendict[string][row] = lastlength
    elif flag_2:
        lendict[string] = {row: lastlength}
    return lastlength
def repairparam(param_list, loopback, startidx, firstback, lastinsertidx, col):
    ii = startidx[col]
    if ii is None:
        ii = lastinsertidx
    if firstback[col]:
        param_list.insert(ii,param_list[ii:])
        return param_list[:ii+1]
    else:
        param_list[ii] = param_list[ii]+param_list[ii+1:]
        return param_list[:ii+1]

def getparam_list(string, parsed_list, priority_list,row, begin,end,return_range_list=False):
    parsed = [i[0] for i in parsed_list[row]]
    loopback = [i[1] for i in parsed_list[row]]
    noparam = [i[2] for i in parsed_list[row]]
    times = [i[3] for i in parsed_list[row]]
    loopback_len = len(loopback)
    cnt = [0 for i in range(loopback_len)]
    range_list = []
    lastinsertidx = 0 # 마지막으로 넣은 인덱스
    insertidx_col_none = False
    insertidx = [None for i in range(loopback_len)]
    firstback = [True for i in range(loopback_len)]
    startidx = [None for i in range(loopback_len)]
    beforeback = None
    wasjumped = False
    lastlength = None
    prev_flag = False
    next_flag = False
    prev_idx = None
    prev_idx_len = None
    jumprange = range(0)
    param_list = []
    start=0
    i= 0
    col = 0
    prev = -1
    str_len = len(string)
    waslooped = False
    #== 루프시작 ==
    while i < str_len:
        str_list = [parsed_list[i][0][0]  for i in range(len(parsed_list))]
        str_list.insert(row,parsed[col])
        str_list = str_list[prev+1:]
        if next_flag:
            idx = prev_idx - (prev+1)
            idx_len = prev_idx_len
        elif prev_flag:
            idx, idx_len = (None,None)
        else:
            idx,idx_len = getidx(string[i:],str_list)
        #== 디버깅 쵝오 
        
        # print(string[i:],param_list,str_list[idx] if idx is not None else idx, None if idx is None else idx+prev+1, row,col)
        if (idx is None or idx+(prev+1) != row) and loopback[col] == col and (not isinstance(noparam[col],list) or not col in noparam[col][1]) and noparam[col] and getbool(times[col],cnt[col],begin,end):
            #반복할 문자열의 횟수가 달성됐고, 이제 그 반복할 문자열이 안 나왔다면 들어오는 If문
            waslooped = False
            if insertidx[col] is None:
                lastinsertidx = insertidx[col] =  len(param_list)
            col+=1
            if col == len(parsed):
                if return_range_list:
                    
                    
                    return (param_list,i, range_list)
                return (param_list,i) 

            continue
        if idx is not None : 
            if idx+(prev+1) == row : #우선순위가 높은 경우
                if (not isinstance(noparam[col], list) or not col in noparam[col][1]) and loopback[col] == col : 
                    repeat_flag = True
                else:
                    repeat_flag = False
                if waslooped:
                    if repeat_flag:
                        hasparam = False
                    else:
                        hasparam = False if noparam[col][1][beforeback] else True
                else:
                    if isinstance(noparam[col],list):
                        hasparam = False if noparam[col][0] else True
                    else:
                        hasparam = False if noparam[col] else True
                if insertidx[col] is None:
                    lastinsertidx = insertidx[col] =  len(param_list)
                    insertidx_col_none=True
                
                
                if hasparam or ( not isinstance(parsed[col],list)  and col != 0  and insertidx[col-1] is None and loopback[col-1] == col-1 and not isinstance(noparam[col-1],list) and noparam[col-1] == False):
                    #궁극의 예외처리...  [[' +', ' -'], 2, [False, {2: False}], [0, 1]], [' } (', None, True, None]에서
                    # +, -가 안나왔을 때는 } (가 인자를 넣는 것을 허용하는 것 
                    #주의할점은 loopback이 자기자신이여야한다.
                    param_list.append(string[start:i])
                    if return_range_list:
                        range_list.append(range(start,i))
                elif string[start:i] != '':
                    if loopback[col] is not None and getbool(times[col],cnt[col],begin,end) and col+1 == len(parsed):
                        if lastlength is not None:
                            return lastlength
                        if startidx[col] is None:
                            startidx[col] = insertidx[loopback[col]]
                        param_list = repairparam(param_list,loopback,startidx,firstback,lastinsertidx,col)
                        if return_range_list:
                            range_list = repairparam(range_list,loopback,startidx,firstback,lastinsertidx,col)
                        if return_range_list:
                            return (param_list,start, range_list)
                        return (param_list,start)
                    return lastlength
                        
                if isinstance(str_list[idx],list):
                    start=i
                    i+=idx_len
                    # print("aaaa:",seperator, parsed[col])
                    if col + 1 < len(parsed) and parsed[col:col+2]  == [argleft, argright]:
            
                        
                        arg_idx = argleft.index(string[start:start+1])
                        pair_idx = findpair_escaped(string[start:],argleft[arg_idx], argright[arg_idx])
                        if pair_idx is not None:
                            param_list.append(argleft[arg_idx])
                            if return_range_list:
                                range_list.append(range(start,start+1))
                            i = start + pair_idx-1
                            start += 1
                            col+=1
                            continue
                    if parsed[col] == escaped_seperator  and col+1 == len(parsed):
                        # 이건 seperator가 마지막 분리기호인 경우 괄호 쌍을 맞추기 위함이다.
                        # 이를 사용하는 변환은 삼각함수, 로그함수 등이 있다.
                        i-= len(string[start:i])
                        idx_len -= len(string[start:i]) 
                    if insertidx_col_none:
                        lastinsertidx = insertidx[col] =  len(param_list)
                        insertidx_col_none=False
                    param_list.append(string[start:i])

                    if return_range_list:
                        range_list.append(range(start,i))

                    idx_len = 0
                
                if wasjumped:
                    for ii in jumprange:
                        if startidx[ii] is None:
                            startidx[ii] = insertidx[loopback[ii]]
                        if not ((not isinstance(noparam[ii], list) or not ii in noparam[ii][1]) and loopback[ii] == ii) or isinstance(parsed[ii],list):
                            
                            param_list = repairparam(param_list,loopback,startidx,firstback,lastinsertidx,ii)
                            if return_range_list:
                                range_list = repairparam(range_list,loopback,startidx,firstback,lastinsertidx,ii)

                i += idx_len
                start = i

                if loopback[col] is None:
                    col+=1
                    if col == len(parsed):
                        if return_range_list:
                            return (param_list,i, range_list)
                        return (param_list,i) 
                    waslooped = False
                else: 
                    beforeback = col
                    if startidx[col] is None:
                        startidx[col] = insertidx[loopback[col]]
                    if not repeat_flag or isinstance(parsed[col],list)  :

                        param_list = repairparam(param_list,loopback,startidx,firstback,lastinsertidx,col)
                        if return_range_list:
                            range_list = repairparam(range_list,loopback,startidx,firstback,lastinsertidx,col)

                    cnt[col]+=1
                    if getbool(times[col],cnt[col],begin,end) and col + 1 == len(parsed):
                        if return_range_list:
                            lastlength = (param_list,start,range_list)
                        else:    
                            lastlength = (param_list,start)
                    firstback[col] = False
                    if times[col][1] == cnt[col]:  # <1*1~2>에서 111을 11과 1로 끊어보기 위함
                        col+=1
                        if col == len(parsed):
                            if return_range_list:
                                return (param_list,i, range_list)
                            return (param_list,i) 
                    else:
                        col = loopback[col]
                        waslooped = True

                # start=i

                if wasjumped:
                    for ii in jumprange:
                        insertidx[loopback[ii]] = None
                        startidx[ii] = None
                        firstback[ii] = True
                wasjumped = False
            else:
                idx = idx+(prev+1)
                ciridx = idx - 1 if idx > row else idx #circulated idx
                if next_flag:
                    pass
                elif priority_list[ciridx] == priority_list[row] :
                    #우선순위가 같을 때는 자기 자신이 우선이므로, parsed[col:]을 먼저 처리해야한다.
                    prev_flag=True
                    prev_idx = idx
                    prev_idx_len = idx_len
                    continue
                length = getlen(string[i:],parsed_list,priority_list,ciridx,begin,end)
                
                if length is not None and priority_list[ciridx] <= priority_list[row]:
                    i+= length
                    if i == length : 
                        # 낮지 않은 우선순위 일경우에만 lastlength를 업데이트함.
                        lastlength = (i,ciridx)
                    prev = -1
                else:
                    prev = idx
                    if prev+1 == len(parsed_list)+1:
                        if next_flag:
                            prev = -1
                            i+=1
                        else:
                            prev_flag=True
                            prev_idx = idx
                            prev_idx_len = idx_len
                            continue
                next_flag= False
        else:
            idx ,idx_len= getidx(string[i:],parsed[col:])
            if idx is not None:
                idx+=col
            if idx is not None and col != idx:
                if all(map(lambda x: getbool(x[0],x[1],begin,end),[[times[ii],cnt[ii]] for ii in range(col,idx+1)] )):
                    for ii in range(col,idx): #cnt[idx]는 초기화 안한다
                        cnt[ii] = 0
                    jumprange = range(col,idx) 
                    wasjumped = True
                    waslooped = False
                    col = idx
                    prev = -1
                elif all(map(lambda x: getbool(x[0],x[1],begin,end),[[times[ii],cnt[ii]] for ii in range(col,idx)] )):
                    for ii in range(col,idx): #cnt[idx]는 초기화 안한다
                        cnt[ii] = 0
                    jumprange = range(col,idx) 
                    wasjumped = True
                    waslooped = False
                    col = idx
                    prev = -1
                elif prev_flag:
                    prev_flag=False
                    next_flag = True
                    continue
                    
                else:
                    prev = -1
                    i+=1
                prev_flag = False
            elif prev_flag:
                prev_flag=False
                next_flag = True
                continue
            else:
                prev = -1
                idx,idx_len = getidx(string[i:], [begin,end,'\\'+begin,'\\'+end,'\\\\','\\'])
                if idx is None:
                    i+=1
                elif idx == 0:
                    i+= len(begin)
                elif idx==1:
                    i+= len(end)
                elif idx==5:
                    i+=1
                else: # [2,5) -> 2,3,4
                    i+= len([begin,end,'\\'+begin,'\\'+end,'\\\\','\\'][idx])
    if loopback[col] is not None and getbool(times[col],cnt[col],begin,end) and col+1 == len(parsed): #원래 cnt[col]+1이였음
        if (not isinstance(noparam[col], list) or not col in noparam[col][1]) and loopback[col] == col : 
            repeat_flag = True
        else:
            repeat_flag = False
        if waslooped:
            if repeat_flag:
                hasparam = False
            else:
                hasparam = False if noparam[col][1][beforeback] else True
        else:
            if isinstance(noparam[col],list):
                hasparam = False if noparam[col][0] else True
            else:
                hasparam = False if noparam[col] else True
        if hasparam is False:
            if lastlength is not None:
                return lastlength
            if not repeat_flag or isinstance(parsed[col],list):
                param_list = repairparam(param_list,loopback,startidx,firstback,lastinsertidx,col)
                if return_range_list:
                    range_list = repairparam(range_list,loopback,startidx,firstback,lastinsertidx,col)

            if return_range_list:
                return (param_list,start, range_list)
            return (param_list,start)
        if string[start:] != '':
            if insertidx[col] is None:
                lastinsertidx = insertidx[col] =  len(param_list)
                insertidx_col_none =True if repeat_flag else False
            else:
                insertidx_col_none = False
            param_list.append(string[start:str_len])
            if return_range_list:
                range_list.append(range(start,str_len))
            if insertidx_col_none:
                lastinsertidx = insertidx[col] =  len(param_list)

                insertidx_col_none= False

        if startidx[col] is None:
            startidx[col] = insertidx[loopback[col]]
        if not repeat_flag or isinstance(parsed[col],list):
            param_list = repairparam(param_list,loopback,startidx,firstback,lastinsertidx,col)
            if return_range_list:
                range_list = repairparam(range_list,loopback,startidx,firstback,lastinsertidx,col)

        if return_range_list:
            return (param_list,str_len, range_list)
        return (param_list,str_len)
    return lastlength


def escape(string,esc_list,stay=[]):
    i=0
    str_len = len(string)
    str_list = ['\\'+esc for esc in esc_list]+['\\\\','\\']
    str_list_len = len(str_list)
    while i < str_len:
        idx= getidx(string[i:],str_list)[0]
        if idx is None:
            i+=1
        elif str_list_len-idx==1:
            i+=1
        elif str_list_len-idx==2:
            i+= len('\\\\')
        else:
            if idx in stay:
                i+=len(str_list[idx])
            else:
                return string[:i] + esc_list[idx] + escape(string[i+len(str_list[idx]):],esc_list)
    return string


def find_escaped(string, target,begin='',end='',esc=''):
    i=0
    if esc=='':
        esc= target
    str_len = len(string)
    if begin=='' and end == '':
        while i < str_len:
            idx = getidx(string[i:],[target,'\\'+esc])[0]
            if idx==0:
                return i
            elif idx==1:
                i+= len('\\'+esc)
            else:
                i+=1
    else:
        while i < str_len:
            idx= getidx(string[i:],[target,begin,end,'\\'+esc,'\\'+begin,'\\'+end,'\\\\','\\'])[0]
            if idx is None:
                i+=1
            elif idx==0:
                return i
            elif idx==1:
                i+= getlen(string[i:],begin_end_parsed,[1.0],0,begin,end)
            elif idx==2:
                raise MyException("End '"+end+"' Cant Be Used Alone")
            elif idx==7:
                i+=1
            else:
                i+=len([target,begin,end,'\\'+esc,'\\'+begin,'\\'+end,'\\\\','\\'][idx])      
    return None

def getcode(string,begin,end,esc=''):
    """
    :return: 문자 코드를 리턴, 문자 코드를 얻을 수 없는 경우 return None
    """
    code = -1
    str_len = len(string)
    i=0
    if str_len ==0:
        return code
    elif str_len == 1:
        if string == begin or string == end or string == esc:
            return None
        return ord(string)
    elif string[:2] == '\\x':
        try:
            code = int(string[2:],16)
            return code
        except:
            return None
    else:
        esc_list = ['\\'+begin,'\\'+end]
        if esc != '':
            esc_list.insert(0,'\\'+esc)
        idx= getidx(string,esc_list)[0]
        if idx is None:
            return None
        else:
            code = ord(esc_list[idx][1:])
            return code        
        
def split_escaped(string, pivot):
    idx = find_escaped(string, pivot)
    if idx is None:
        return [string]
    return [string[:idx]] + split_escaped(string[idx+len(pivot):],pivot)

def getbool(times,x,begin,end):
    """
    :times: times는 정수만 가지는 리스트여야 한다. 
    """
    if isinstance(x,str):
        x= ord(x[0])
    if times is None:
        return False
    elif len(times) == 0:
        return True
    elif len(times) == 1:
        return x==times[0]
    elif len(times) == 2:
        return (True if times[0] == -1 else x>=times[0])  and  (True if times[1] == -1 else x<=times[1])
    else:
        raise MyException("Times Size Must Be Less Than 3")        

def findpair_escaped(string, left,right):
    
    i=0
    str_len = len(string)
    left_len = len(left)
    right_len = len(right)
    left_right =0
    if string[:left_len] != left:
        raise MyException("Left '"+left+"' Must Be First Of String '"+string+"'")
    while i< str_len:
        idx = getidx(string[i:],[left,right,'\\\\'])[0]
        if idx is None:
            i+=1
        elif idx == 0:
            left_right+=1
            i+= left_len
        elif idx == 1:
            left_right -=1
            i+= right_len
        elif idx==2:
            i+= len('\\\\')
        if left==right and left_right == 2:
            return i
        elif left_right == 0:
            return i
    return None

def getpattern(string, begin,end):
    """
    :return: 0: ''..., 1: -, 2: <*[~]>, 3: 그외
    """
    # 2는 \... 3은 \*, \...의 이스케이프가 필요함
    begin_len = len(begin)
    end_len = len(end)
    length = getlen(string,begin_end_parsed,[1.0],0,begin,end)
    if length is None:
        raise MyException("Begin '"+begin+"' And End '"+end+"' Not Matched")  
    else:
        try:
            find_escaped(string[begin_len:],'...',begin,end)
            return 0
        except:
            pass
        try:
            splited = split_escaped(string[begin_len:length-end_len],'-')
            if len(splited) == 2 and getcode(splited[0],begin,end,'-') is not None and getcode(splited[1],begin,end) is not None:
                return 1
        except:
            pass    
        try:
            find_escaped(string[begin_len:],'*',begin,end)
            return 2
        except:
            pass
    return 3

def pair_replace(string, left, right, new_left, new_right,begin,end):
    """
    :param string: left,right를 포함하고 있는 문자열
    :param left: '(' 같이 right와 짝을 이루는 문자열
    :param right: ')' 같이 left와 짝을 이루는 문자열
    :param new_left: '{' 같이 new_right와 짝을 이루고 left와 교체될 문자열 
    :param new_right: '}' 같이 new_left와 짝을 이루고 right와 교체될 문자열
    :param begin: '\\[' 같이 end와 짝을 이루는 문자열
    :param end: '\\] 같이 begin과 짝을 이루는 문자열
    :param begin_end: begin과 end사이는 건너 뛸 지 여부
    :return: 오류 발생 시 MyExcepion Raise, 그 이외에는 left를 new_left로 right를 new_right로 교체한 문자열을 반환한다.
    """
    #========================
    left_len = len(left)
    right_len = len(right)
    str_len = len(string)
    i=0
    #================
    while i< str_len:
        idx= getidx(string[i:],[left,'\\'+begin,'\\'+end,'\\\\','\\'])[0]
        if idx is None:
            i+=1
        elif idx==0:
            idx = findpair_escaped(string[i:], left,right)
            if idx is  None:
                raise MyException("Left '"+left+"' And Right '"+right+"' Not Matched")    
            return string[:i] + new_left +\
            pair_replace(string[i+left_len:i+idx-right_len],left,right,new_left,new_right,begin,end) +\
            new_right + pair_replace(string[i+idx:],left,right,new_left,new_right,begin,end) 
        elif idx<=3:
            i+= len([left,'\\'+begin,'\\'+end,'\\\\','\\'])
        elif idx==4:
            i+=1
    return string

        
def replace_escaped(string, esc_list,new_list):
    
    i=0
    str_len = len(string)
    while i< str_len:
        idx = getidx(string[i:],esc_list+['\\\\'])[0]
        if idx  is not None:
            if idx==len(esc_list):
                i+=2
            else:
                return string[:i] + new_list[idx] + replace_escaped(string[i+len(esc_list[idx]):],esc_list,new_list)
        else:
            i+=1
    return string
def escape_parsed(parsed,param,begin,end):
    str_list = [param,begin,end,'\\']
    escaped_parsed = []
    for pars in parsed:
        if isinstance(pars[0],str):
            pars[0] = escape(pars[0],str_list)
        elif isinstance(pars[0],list):
            if isinstance(pars[0][0],int):
                pass
            elif isinstance(pars[0][0],str):
                escaped_str_list = []
                for i in pars[0]:
                    escaped_str_list.append(escape(i,str_list))
                pars[0] = escaped_str_list
            else:
                print("Thinking...")
        else:
            print("Thinking 2... ")
        escaped_parsed.append(pars)
    return escaped_parsed

def parse(string,param,parsed,wasparam, begin, end):

    flag= True if wasparam is None else False
    str_list = [begin, '\'', '\'', '...', end]
    str_list2 = [begin, '*', '~', end]
    str_len = len(string)
    param_len = len(param)
    i = 0
    start = 0
    while i < str_len:
        idx = getidx(string[i:], [param, begin, end, '\\' +param, '\\'+begin, '\\'+end, '\\\\', '\\'])[0]
        if idx is None:
            i += 1
        else:
            if idx == 0:
                if string[start:i] == '':
                    if wasparam is not False:
                        raise MyException("Empty('') Cant Be In Splited")
                else:
                    escaped_str = string[start:i]
                    parsed.append([escaped_str,None,True if wasparam is not True else False,None ])    
                wasparam=True
                i += param_len
                start = i
            elif idx==1:
                pattern = getpattern(string[i:],begin,end)
                length = getlen(string[i:],begin_end_parsed,[1.0],0,begin,end)
                if pattern == 0:
                    loopback = len(parsed) 
                    start_str = ''
                    for j in range(len(str_list)):
                        idx = find_escaped(string[i:],str_list[j],begin,end, '.' if j==3 else '')
                        if idx is None:
                            raise MyException("'"+string+"' Cant Be Parsed")
                        else:   
                            i += idx
                            escaped_str = escape(string[start:i],['.' if j==3 else str_list[j]]) 
                            if escaped_str == '':
                                if j==2 or j==3:
                                    raise MyException("Empty('') Cant Be In Splited")
                            else:
                                if j<=1: # begin 이전과 시작문자
                                    parsed, wasparam = parse(escaped_str,param,parsed,False if wasparam is None else wasparam,begin,end)          
                                    loopback = len(parsed)
                                    
                                elif j==3: # 구분 문자 부분
                                    parsed, wasparam = parse(escaped_str,param,parsed, False if wasparam is None else wasparam,begin,end)
                                    parsed[-1][1] = loopback
                                    parsed[-1][3] = [0,-1]#times
                                    usual = loopback #평소

                                    #시작 - 구분 - 시작이 부적합한지 검사
                                    byloop = len(parsed) #loopback에 의해 돌아왔을 때   
                                    parsed, wasparam = parse(start_str,param,parsed, False if wasparam is None else wasparam,begin,end)
                                    sliceflag = False
                                    if len(parsed) <= byloop:
                                        byloop = usual
                                    else:
                                        sliceflag = True
                                        byloop -= 1
                                    if isinstance(parsed[usual][2],list):
                                        parsed[usual][2][1][byloop] = parsed[byloop][2]
                                    else:
                                        parsed[usual][2] = [parsed[usual][2], {byloop: parsed[byloop][2]}]
                                    if sliceflag:
                                        parsed=parsed[:byloop+1]
                                else:
                                    if j==2:
                                        start_str = escaped_str
                                    parsed, wasparam = parse(escaped_str,param,parsed,False if wasparam is None else wasparam,begin,end)
                            i += len(str_list[j])
                            start = i
                    if string[start:] =='':
                        return parsed, wasparam  
                elif pattern == 1:
                    escaped_str = string[start:i]  
                    if escaped_str != '':
                        parsed, wasparam = parse(escaped_str,param,parsed,False if wasparam is None else wasparam,begin,end)  
                    escaped_str = string[i+len(begin):i+length-len(end)]
                    splited = split_escaped(escaped_str,'-')
                    parsed.append([[getcode(splited[0],begin,end,'-'),getcode(splited[1],begin,end)],None,True if wasparam is not True else False,None])
                    i+= length
                    start=i
                    wasparam = False
                    if string[start:] =='':
                        return parsed, wasparam
#============================== 패턴 2===============================
                elif pattern == 2:
                    loopback = len(parsed) 
                    start_str = ''
                    times = []
                    for j in range(len(str_list2)):
                        try:
                            idx = find_escaped(string[i:],str_list2[j],begin,end)
                        except:
                            idx = None
                        
                        if idx is None:
                            if j==2:# ~만 없을 수 있다.
                                pass
                            else:
                                raise MyException("'"+string+"' Cant Be Parsed")
                        else:   
                            i += idx
                            #==이스케이프==
                            escaped_str = escape(string[start:i],['...',str_list2[j]])
                            if j==3: # 최대횟수
                                if escaped_str == '':
                                    times.append(-1)
                                else:
                                    try:
                                        times.append(int(escaped_str))
                                    except:
                                        raise MyException("Maximum Times Must Be Int")
                                if len(times) == 1 and times[0] <= 1:
                                    raise MyException("You Cant Use *0 Or *1")    
                                parsed[-1][1] = loopback
                                parsed[-1][3]  = times


                                #시작 - 구분 - 시작이 부적합한지 검사
                                usual = loopback #평소
                                #print(parsed,wasparam,usual,loopback)
                                byloop = len(parsed) #loopback에 의해 돌아왔을 때   
                                parsed, wasparam = parse(start_str,param,parsed, False if wasparam is None else wasparam,begin,end)
                                
                                #==디버깅 == 
                                #print(parsed,wasparam,usual,loopback)
                                # sliceflag = False
                                # if len(parsed) <= byloop:
                                #     byloop = usual
                                # else:
                                #     sliceflag = True
                                byloop -= 1
                                
                                if len(parsed) != byloop+2: #자기 자신 루프인 경우는 제외하겠다는 것!
                                    if isinstance(parsed[usual][2],list):
                                        parsed[usual][2][1][byloop] = parsed[byloop][2]
                                    else:
                                        parsed[usual][2] = [parsed[usual][2], {byloop: parsed[byloop][2]}]
                                parsed=parsed[:byloop+1]

                            elif escaped_str == '':
                                if j==1:
                                    raise MyException("Empty('') Cant Be In Splited")
                                elif j==2:                                    
                                    raise MyException("Minimum Times Cant Be Empty('')")
                            else:
                                if j==0: #begin 이전
                                    parsed, wasparam = parse(escaped_str,param,parsed,False if wasparam is None else wasparam,begin,end)          
                                    loopback = len(parsed)
                                elif j==1: #반복할문자열
                                    start_str= escaped_str
                                    parsed, wasparam = parse(escaped_str,param,parsed,False if wasparam is None else wasparam,begin,end)     
                                elif j==2:
                                    try:
                                        times.append(int(escaped_str))
                                    except:
                                        raise MyException("Minimum Times Must Be Int")
                            i += len(str_list2[j])
                            start = i
                    if string[start:] =='':
                        return parsed, wasparam 
                elif pattern == 3:
                    escaped_str = string[start:i]
                    if escaped_str != '':
                        parsed, wasparam = parse(escaped_str,param,parsed,False if wasparam is None else wasparam,begin,end)  
                    #==이스케이프==
                    escaped_str = escape(string[i+len(begin):i+length-len(end)],['...','*'])
                    splited = split_escaped(escaped_str,'|')
                    splited = list(map(lambda x : escape(x,'|'),splited))
                    parsed.append([splited, None, True if wasparam is not True else False,None ])    
                    i+=length
                    start =i
                    wasparam = False
                    if string[start:] =='':
                        return parsed, wasparam
                    
            elif idx==2:
                raise MyException("End '"+end+"' Cant Be Used Alone")
            elif idx==7:
                i+=1
            else: # [3,7) -> 3,4,5,6
                i+= len([param,begin,end,'\\'+param,'\\'+begin,'\\'+end,'\\\\','\\'][idx])
    
    if string[start:] == '':
        if flag:
            raise MyException("Empty('') Cant Be In Splited")
    else:
        parsed.append([string[start:],None,True if wasparam is not True else False,None])
        wasparam = False
    return parsed, wasparam
        

def img2latex(filename):
    #약 0.6초 정도 소모됨
    global maximum_call, img2latex_call
    if maximum_call == img2latex_call:
        print("Maximum Call")
        raise MyException("Dont Call img2latex More Than "+str(maximum_call))
    img2latex_call+=1
    file_path = filename
    image_uri = "data:image/jpg;base64," + str(base64.b64encode(open(file_path, "rb").read()))[2:-1]
    r = requests.post("https://api.mathpix.com/v3/latex",
        data=json.dumps({'src': image_uri, 'ocr' : ['math','text']}),
        headers={"app_id": "msjang4_dgsw_hs_kr", "app_key": "caacac60603c51823275", 
                "Content-type": "application/json"})
    _latex= json.loads(r.text)['latex']
    f= open("log.txt","a")
    f.write(str(datetime.datetime.now())+": "+_latex+'\n')
    f.close()
    return _latex
def center_align_img(img,size):
    if size is None:
        size = (50,50)
    img.thumbnail(size, Image.ANTIALIAS)
    layer = Image.new('RGB', size, (255,255,255))
    layer.paste(img, tuple(map(lambda x: (x[0]-x[1])//2, zip(size, img.size))))
    return layer
def latex2img(latex,x=0.001, y=0.001,size=50,imgsize=None,filename='output.png'):
    #이함수는 맨처음 실행됐을때만 겁나게 느리다. 이유는 모르겠다.
    fig = plt.figure()
    plt.text(x, y, r"$%s$" % latex, fontsize = size)
    fig.patch.set_facecolor('white')
    plt.axis('off')
    #plt.tight_layout()

    with io.BytesIO() as png_buf:
        plt.savefig(png_buf, bbox_inches='tight', pad_inches=0) #요거 1초 정도
        png_buf.seek(0)
        image = Image.open(png_buf)
        image.load()
        inverted_image = ImageOps.invert(image.convert("RGB"))
        cropped = image.crop(inverted_image.getbbox())
        if imgsize is not None:
            cropped = center_align_img(cropped,imgsize)
        cropped.save(filename)
    plt.close(fig)
    
def convertall(string,parsed_list,form_list,eval_list,priority_list,begin,end):
    global lendict
    parsed_list_len = len(parsed_list)
    for row in range(parsed_list_len):
        string = convert(string,parsed_list,form_list,eval_list,priority_list,begin,end,row,True)
        #==디버깅 쵝오
        # print(row,": ",repr(string))
        # print(row,": ", parsed_list[row])
    lendict = {} #lendict 초기화
    return string

def convert(string,parsed_list,form_list,eval_list,priority_list,begin,end,row,first=False):
    doeval = eval_list[row]
    str_len = len(string)
    if isinstance(string, list):
        str_list = []
        for i in range(str_len):
            str_list.append(convert(string[i],parsed_list,form_list,eval_list,priority_list,begin,end,row))
        return str_list
    i=0
    while i< str_len:
        param_list = getparam_list(string[i:],parsed_list,priority_list,row,begin,end)
        #디버깅 쵝오
        #print(string[i:],"param_list: ",param_list)
        if param_list is not None:
            if isinstance(param_list[0],int) and isinstance(param_list[1],int):
                ciridx = param_list[1]
                length = param_list[0]
                
                param_list =getparam_list(string[i:],parsed_list,priority_list,ciridx,begin,end,True)
                if length != param_list[1]:
                    raise MyException("Internal Critical Exception")
                
                try:
                    range_list = param_list[2]
                    param_list = param_list[0]
                except:
                    raise MyException("Internal Critical Exception")
                if len(param_list) > 1:
                    param_list = convert(param_list,parsed_list,form_list,eval_list,priority_list,begin,end,row)
                    return string[:i]+replace_parts(string[i:i+length],range_list,param_list)+ convert(string[i+length:],parsed_list,form_list,eval_list,priority_list,begin,end,row)
                else:
                    i+= length
            else:
                length = param_list[1]
                param_list = param_list[0]
                if len(param_list) ==1 and isinstance(param_list,list) and len(param_list[0]) ==1 and param_list[0][0] == string:
                    #=무한 재귀 방지
                    if first:
                        #재귀 호출이 아닌 경우에는 form형태로 변환해서 반환한다.
                        if doeval:
                            return eval(form_list[row].format(*param_list),globals(),locals())            
                        else:
                            return form_list[row].format(*param_list)
                    return string
                    
                param_list = convert(param_list,parsed_list,form_list,eval_list,priority_list,begin,end,row)
                #디버깅 쵝오
                # print("converted param_list: ",param_list)
                # print(form_list[row].format(*param_list))
                if doeval:
                    return string[:i] + eval(form_list[row].format(*param_list),globals(),locals()) + convert(string[i+length:],parsed_list,form_list,eval_list,priority_list,begin,end,row)

                else:
                    return string[:i] + form_list[row].format(*param_list) + convert(string[i+length:],parsed_list,form_list,eval_list,priority_list,begin,end,row)
        else:
            i+=1
    return string

def wannaconvert(wanna,symbs):
    symbs = symbs +[reduce(operator.add,symbs)]+ [relationals]+[argleft]+[argright]+[seperator]+[alphabet]
    str_list = ['Complex','Matrix','Function','Unknown','Relational','Argleft','Argright','Seperator','Alphabet']
    for i in range(len(str_list)):
        wanna =wanna.replace('{'+str_list[i]+'}','|'.join(symbs[i]))
    return wanna

def interpret(sympyform, func = 0):
    exec('eqr = '+sympyform,globals())
    if type(eqr) in primitive:
        print("is_Primitive")
        answer = latex(eqr)
    elif eqr.is_Relational:
        print("is_Relational ",end='')
        if func== 0: #선형방정식
            print("linear")
            answer = latex(solve(eqr,dict=True))
        elif func == 1: #미분방정식
            print("derivative")
            answer = latex(dsolve(eqr))
        elif func == 2: #집합연산
            print("set")
            answer = latex(solveset(eqr))
    else:
        if func == 3: #인수분해
            print("factor")
            answer = latex(factor(eqr))
        elif func == 4: #전개
            print("expand")
            answer = latex(expand(eqr))
        else:
            print("is_Nothing")
            answer = latex(eqr)

    return answer

def getsymbs(complex_str, matrix_str, function_str):
    try:
        complex = list(filter( lambda x: x != '' ,complex_str.split(" ")))
        matrix = list(filter( lambda x: x != '' ,matrix_str.split(" ")))
        size_list = []
        name_list = []
        str_list = ['(',',',')']
        i = 0
        temp = ''
        size = tuple()
        for m in matrix:
            while True:
                idx = m.find(str_list[i])
                if idx ==-1:
                    temp += m
                    break
                else:   
                    if i==0:
                        name_list.append(temp+m[:idx])
                        temp = ''
                    elif i==1:
                        size = int(temp+m[:idx])
                        temp = ''
                    elif i==2:
                        size = (size, int(temp+m[:idx]))
                        temp = ''
                        size_list.append(size)
                    i+=1
                    i%=3
                    m = m[idx+1:]
                    if m == '':
                        break
        if i!=0:
            raise Exception()
        function = list(filter(lambda x: x != '',function_str.split(" ")))
        return [complex, [name_list,size_list], function]
    except:
        raise MyException("ConFirm The Form")


def init(begin,end,filename,symbs):
    global begin_end_parsed,seperator,escaped_seperator, matrixsize
    for relational in relationals:
        escaped_relationals.append(escape(relational,[begin,end]))
    escaped_seperator = argleft + argright + seperator + triangleseperator+ escaped_relationals
    seperator = argleft+argright+ seperator+ triangleseperator + relationals
    begin_end_parsed = [[[begin,None,True,None],[end,None,False,None]]]
    f = open(filename,'r',encoding='utf-8') 
    exec(','.join(symbs[0]) + '='+ 'symbols(\''+' '.join(symbs[0])+'\')',globals())
    exec(','.join(symbs[2]) + '='+ 'symbols(\''+' '.join(symbs[2])+'\',cls=Function)',globals())
    #symbs[1]과 symbs[0]을 이용해 exec함... (symarray로)
    matrixsize = symbs[1]
    symbs[0] = symbs[0] + defaultcomplex
    symbs[1] = symbs[1][0] + defaultmatrix
    symbs[2] = symbs[2] + defaultfunction
    parsed_list = []
    form_list = []
    eval_list = []
    priority_list = []
    lines = f.readlines()
    if len(lines) % 8 != 0:
        # docs ,doeval , param , wanna, left, right, form 총 6부분으로 이루어져있다.
        raise MyException("Number Of Lines Not Multiples Of 8")
    for idx in range(0,len(lines),8):
        idx+=1
        doeval = True if lines[idx][:-1] == 'True' else False
        eval_list.append(doeval)
        param = lines[idx+1][:-1]
        wanna = lines[idx+2][:-1]
        wanna = wannaconvert(wanna,symbs)
        parsed = parse(wanna,param,[],None,begin,end)[0]
        parsed = escape_parsed(parsed,param,begin,end)
        left = lines[idx+3][:-1]
        right = lines[idx+4][:-1]
        form = pair_replace(replace_escaped(lines[idx+5][:-1],['\\{','\\}'],['{{','}}']),left,right,'{','}',begin,end)
        form = escape(form,['\\'])
        form_list.append(form)
        try:
            priority = float(lines[idx+6][:-1])
        except:
            raise MyException("Priority Must Be Int")
        priority_list.append(priority)
        parsed_list.append(parsed)
    return parsed_list, form_list,eval_list,priority_list

