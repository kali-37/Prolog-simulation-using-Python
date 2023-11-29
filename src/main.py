import sys 
from parser import   Parser,Predicate_builder

class Predicate:
    predicates:dict[str,"Predicate"] = {}
    def __new__(cls,*args,)->"Predicate" :  
        if args[0] not in Predicate.predicates :
            Predicate.predicates[args[0]]=super().__new__(cls)
        return Predicate.predicates[args[0]]

    def __init__(self,name:str)->None:
        self.name:str=name 
        if not hasattr(self, 'argv') or self.argv is None:  # if the objecit has no attribute argv or argv is None
            self.argv: list[str | int | float |list]| None = None
       
    def add_arg(self,argv: list[str|int|float])-> None:
        if self.argv is None:
            self.argv=[argv]
        else:
            self.argv.append(argv)
            
    @staticmethod
    def Predicate_transferer():
        return Predicate.predicates

def parse_file_data(file_pointer):
    for line in file_pointer:
        Predicate_builder().build(line)



def main(argv):
    if not  argv[1]!="--help" or argv[1]!="-h":
        with open(argv[1]) as f:
            if not f.readable():
                raise FileNotFoundError("couldn't read file : Requested py main.py file_name")
            parse_file_data(f)






        
# def main():
    # obj=Predicate("LIKE")
    # obj.add_arg(["bobby","sanzog","mangoes"])
    # bb=Predicate("LIKE")
    # bb.add_arg(["new","ew"])
    # b=Predicate("pawan")
    # print(bb.argv)
    # requested_value=Parser().arg_checker("LIKE(mangoes,bobby,new).",Predicate.Predicate_transferer())
    # print(requested_value)



if __name__=='__main__':
    if len(sys.argv) ==2:
        main(sys.argv)
    else: 
        print("At least 2 arguent is expected ") 
