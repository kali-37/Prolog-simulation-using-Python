import sys 

import collections
class Predicate:
    def __init__(self,name):
        self.name=name 
        self.argv=list()   


    def add_arg(self,argv):
        self.argv.append(argv)

    def __str__(self):
        return f"Name : {self.name},    Argument = {self.argv} "                


def parse(x):
    p=0
    predicates:List[List[Predicate]] =[[] for _ in range(30)] 
    string=""
    assumed_name=[[] for _ in range(30)]
    assumed_elements=[[] for _ in range(30)]
    e,ea=(0,0)
    while p < len(x):

        if x[p]=='(':
            assumed_name[e].append(string.replace("\n",""))
            string=""
            p+=1
            
        if  x[p]=="," or x[p]==")" :
            assumed_elements[ea].append(string)
            string=""
            p+=1
        
        if x[p]==".":
            predicates[e].append(Predicate(assumed_name[e][0]))
            predicates[e][0].add_arg(assumed_elements[ea])
            string=""
            ea+=1
            e+=1

        if len(x) ==p:
            break
        string+=x[p]
        p+=1

    for i in predicates:
        for j in i:
            print(j)


def main():
    with open (sys.argv[1]) as f:
        if not f.readable():
            raise FileNotFoundError("Couldn't read the file") 
        data=f.read() 
        parse(data)


if __name__=='__main__':
    if len(sys.argv) ==2:
        main()
    else: 
        print("At least 2 arguent is expected ") 
