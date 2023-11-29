import Query
import re




class Parser(Query.query):

    checkin:dict[str,"Parser"]={}

        
    def arg_checker(self,argv:str,Pred:dict):
        print(argv,"argv...")
        b_S,b_C=(0,0) # bracket start "("  | bracket close ")" 
        p_dot=False # p_dot "." 
        for i in argv:
            if i==')' :
                b_C+=1 
            if i=='(':
                b_S+=1 
            if i=='.':
                p_dot=True

        if b_S==b_C==1 and p_dot:
            result=re.split(r'\(|\)|\.',argv) 
            result=list(filter(None,result))
            return Query.query().single_test(result,Pred)
        elif(b_S!=b_C):
            raise SyntaxError("Brackets are not Balanced .")






# def parse(x):
   
#     string=""
#     assumed_name=[[] for _ in range(30)]
#     assumed_elements=[[] for _ in range(30)]
#     e,ea=(0,0)
#     while p < len(x):

#         if x[p]=='(':
#             assumed_name[e].append(string.replace("\n",""))
#             string=""
#             p+=1
            
#         if  x[p]=="," or x[p]==")" :
#             assumed_elements[ea].append(string)
#             string=""
#             p+=1
        
#         if x[p]==".":
#             predicates[e].append(Predicate(assumed_name[e][0]))
#             predicates[e][0].add_arg(assumed_elements[ea])
#             string=""
#             ea+=1
#             e+=1

#         if len(x) ==p:
#             break
#         string+=x[p]
#         p+=1

#     inner_elements=[]

#     for i in predicates:
#         for j in i:
#             for x in j.argv:
#                 ...

