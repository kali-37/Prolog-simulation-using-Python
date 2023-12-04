from re import IGNORECASE
import sys ,os
from parser import   Parser

# class key_DATA:

class Stack_history:
    
    def __init__(self):
        self.stack=[]  

    def adder(self,value):
        self.stack.append(value)

    def display(self):
        return self.stack


class Keylogger:

    @staticmethod
    def _key():
        if  sys.platform.startswith('win'):
            import msvcrt 
            if msvcrt.getch()== b'n':#  type:ignore
                return "NEXT"
            elif msvcrt.getch() == b'b': #type:ignore
                return "BREAK"
        else:
            import termios, tty
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            if ch == 'n':
                return "NEXT"
            elif ch == 'b':
                return "BREAK"
class stack:
    def __init__(self):
        self.stack=[]
    def push(self,user_input):
        self.stack.append(user_input)
    def above(self,times):
        return self.stack[times]
    def below(self,times):
        return self.stack[times] 


class Predicate:
    predicates:dict[str|int|float,"Predicate"] = {}
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

    def __str__(self):
        return f"{self.name},({self.argv})"

    @staticmethod
    def Predicate_transferer():
        return Predicate.predicates


def parse_file_data(file_pointer):
    for line in file_pointer:
        tup:tuple[str,list[str]]|None=Parser().build(line)
        if tup is not None:  
            obj=Predicate(tup[0])
            obj.add_arg(list(tup[1]))
        
    # for  obj in Predicate.predicates.values():
        # print(obj)

def main(argv):
    if not  argv[1]!="--help" or argv[1]!="-h":
        with open(argv[1]) as f:
            if not f.readable():
                raise FileNotFoundError("couldn't read file : Requested py main.py file_name")
            parse_file_data(f)

    user_input()

def user_input():
    os.system('clear')
    while True:
        try:
            str_input=input("| ?- ")
            if str_input.lower()=="exit":
                print("Exited .. Good bye") 
                exit()
            elif(str_input):
                requested_value=Parser().check_arguments(str_input,Predicate.Predicate_transferer())
                if  type(requested_value)==bool:
                    print(requested_value)
                elif type(requested_value)==set:
                    print("Press 'n' to see next result or 'b' to see previous result or 'q' to quit")  
                    while(True):
                        for i in requested_value:
                            print(i) 
                            if (Keylogger._key())=="NEXT":
                                continue
                            else:
                                break
                        break   

            else:
                raise SyntaxError("SyntaxError: Invalid syntax. Guess forgot '.' dot at the end of the query")
        except SyntaxError:
                ...
        except Exception as e:
            print(f"ERROR: {e}")
        
        

if __name__=='__main__':
    if len(sys.argv) ==2:
        main(sys.argv)
    else: 
        print("At least 2 arguent is expected ") 




# switch cases in python can be done as 
# def switch_demo(argument):

#     switcher = {
#         0: "This is Case Zero ",
#         1: "This is Case One ",
#         2: "This is Case Two ",
#     }

#     # get() method of dictionary data type returns
#     # value of passed argument if it is present
