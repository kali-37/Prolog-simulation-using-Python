
testr="relation(X,Y):-  likes(Y,X,Z) not likes(X,Y,Z) ; likes(X,X) , likes(P,Q)."

test=testr.split(':-')
print(test)
text0=test[0]
text=test[1]
import re 
rem=re.findall(r'([a-z][\w_]+)[\s]*\(([^)]+)\)[\s]*([a-z]+|\;|\,|\.)?[\s]*',text)
for pred,param,op in rem:
    print(pred,param.split(','),op)

_quer0=re.match(r'([\w_]+)\(([A-Z,]+)\)*',text0)
_quer =re.findall(r'([\w_]+)\(([A-Z,]+)\)[\s]*(not|\,|\;)?[\s]*',text)
if _quer0:
    relation,relation_inst=_quer0.group(1),_quer0.group(2)
    relation_inst=relation_inst.split(',')
    if _quer:
        for param, param_inst,operator in _quer:
                param_inst=param_inst.split(',')
                if  set(param_inst).issubset(set(relation_inst)):
                    print(relation,relation_inst,param,param_inst,operator )
                else:
                    print(f"ERROR: FAILED TO Create , RELATION[insts] must be subset of Query[insts]")
                    exit()
            #now returning the 
                
