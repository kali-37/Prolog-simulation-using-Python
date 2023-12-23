from re import IGNORECASE
import sys ,os,readline
from _parser import Parser
import logging
logging.basicConfig(level=logging.INFO,filename="log.log",filemode='w')
class key_listener:
    @staticmethod
    def _read():
            if sys.platform=="win32":
                import msvcrt # IGNORECASE
                while True:
                    if msvcrt.kbhit():
                        key = msvcrt.getch().decode('utf-8')
                        if key == 'n':
                            return 'n'
                        else:
                            return 'b'
            else:
                import tty,termios 

            while True:
                old_settings = termios.tcgetattr(sys.stdin)
                try:
                    tty.setcbreak(sys.stdin.fileno())
                    key = sys.stdin.read(1)
                finally:
                    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
                if key == 'n':
                    return 'n'
                else: 
                    return 'b'
class Predicate:
    predicates:dict[str|float|int,"Predicate"] = {}
    def __new__(cls,*args,)->"Predicate" :  
        if args[0] not in Predicate.predicates :
            Predicate.predicates[args[0]]=super().__new__(cls)
        return Predicate.predicates[args[0]]

    def __init__(self,name:str)->None:
        self.name:str=name 
        if not hasattr(self, 'argv') or self.argv is None:  # if the objecit has no attribute argv or argv is None
            self.argv: list[str|list]| None = None
       
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
        x= Parser().check_arguments(line)
        if  type(x)==bool:
            print("Syntax Error Operator Expected")
            logging.critical("GRAMMARS FILE HAVE TO BE CORRECTED") 
            exit()
        else:
            logging.info("GRAMMARS Accepted ") 
            tup:tuple[str,list[str]]|None=x 
            if tup is not None:  
                obj=Predicate(tup[0])
                obj.add_arg(list(tup[1]))
        
def detect_key(stdsrc):
    stdsrc.clear()
    while True:
        c=stdsrc.getch()
        if c==ord('n'):
            return 'n' 
        elif c==ord('b'):
            return 'b'
       
def main(argv):
    logging.info("LOGGED_Main")
    if not  argv[1]!="--help" or argv[1]!="-h":
        with open(argv[1]) as f:
            if not f.readable():
                raise FileNotFoundError(f"couldn't read file : Requested grammars file {argv[1]}")
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
                requested_value=Parser().build(str_input,Predicate.Predicate_transferer())
                if  type(requested_value)==bool:
                    print(requested_value)
                elif type(requested_value)==set:
                    print("Press 'n' to see next result and  'b' to break|quit")  
                    for i in requested_value:
                        if key_listener._read()=='n': 
                            print(i) 
                        else: 
                            break   
            else:
                raise SyntaxError("SyntaxError: Invalid syntax. Guess forgot '.' dot at the end of the query")
        except SyntaxError:
                ...
        except KeyboardInterrupt:
            print("CTRL+C Detected , Guess what, dumb ass dosen't know there is exit command")
            exit()
        except Exception as e:
            print(f"ERROR: {e}")
        
        

if __name__=='__main__':
    if len(sys.argv) ==2:

        main(sys.argv)
    else: 
        print("At least 2 arguent is expected ") 






#   AND |  ,
#   iF   |  :-
#    OR  | ; 
#    Not | not