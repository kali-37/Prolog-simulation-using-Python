import Queries,time
import re
import logging
from utilities import Relations

class Parser(Queries.Query):
    @staticmethod 
    def validate_query(argv):
        logging.info("Parser")  
        b_S=argv.count('(')
        b_C=argv.count(')')
        p_dot= '.' in argv   
        if_query=':-' in argv 
        try:  
            if if_query:
                print("IF_QU")
                return "if_query"
            elif b_S==b_C and p_dot:
                return True
            elif b_S != b_C:
                raise SyntaxError("SyntaxError: Unbalanced brackets detected. Ensure that the parentheses are properly matched.")
            elif not p_dot:
                raise SyntaxError("SyntaxError: Invalid syntax. Guess forgot '.' dot at the end of the query") 
        except SyntaxError as e: 
            print(e)
            return False

    @staticmethod 
    def seprate_query_elems(argv:str):
        result=list(filter(None,re.split(r'\(|\)|\.|\,|\n',argv)))
        key_tester=result.pop(0)
        return key_tester,result

    @staticmethod
    def parse_if_query(arg):
        parser_list=[]
        print("RELATION",arg)
        _spl=arg.split(':-')
        _rel=_spl[0]
        _relback=_spl[1]
        _quer0=re.match(r'([\w_]+)\(([A-Z,]+)\)*',_rel)
        _quer =re.findall(r'([\w_]+)\(([A-Z,]+)\)[\s]*(not|\,|\;)?[\s]*',_relback)
        if _quer0:
            relation,relation_inst=_quer0.group(1),_quer0.group(2)
            relation_inst=relation_inst.split(',')
            if _quer:
                for param, param_inst,operator in _quer: 
                        param_inst=param_inst.split(',')
                        if  set(param_inst).issubset(set(relation_inst)):
                            parser_list.append([param,param_inst,operator])
                        else:
                            print(f"ERROR: FAILED TO Create , RELATION[insts]:{relation_inst} must be subset of Query[insts]:{param_inst}")
                            exit()
                return [relation,relation_inst,parser_list]
            return False
        return False
    @staticmethod
    def check_arguments(arg)->tuple[str,list[str]]|list[list[str]]|None|bool: 
        _tmp=Parser.validate_query(arg)
        if _tmp:
            if _tmp=="if_query":
                _parsed_if=Parser.parse_if_query(arg)
                return _parsed_if
            else :
                return Parser.seprate_query_elems(arg)
            
        return False 
# ___________________  USER INPUT HANDLER ______________________ #

    
    @staticmethod 
    def build(argv: str, Pred: dict, _relation_obj: list["Relations"]):
        logging.info("BUILD user INPUT") 
        _tmp=Parser.validate_query(argv)
        if _tmp:   
            key_tester, result = Parser.seprate_query_elems(argv)
            # if "ERROR" in result:
                # return key_tester, result
            if key_tester not in Pred.keys():
                logging.info(f"IF_Query Build ,keytester:{key_tester}")
                for i in _relation_obj:
                    if i.relate == key_tester and len(i.queries_map)==len(result):
                        _inst =Relation(key_tester, result, _relation_obj, i)
                        print("MET___")
                return False
            
            else:
                return Queries.Query().single_test(key_tester, result, Pred)

# _________________ USER INPUT HANDLER :CLOSED ________________ #




class Relation:
    def __init__(self,key_tester:str,result:list[str],_relation_obj:list["Relations"],i:"Relations" ):
        logging.info(f"class: Relation invoked{key_tester,result}")
        self.key_tester=key_tester
        self.result=result 
        self._relation_obj=_relation_obj
        self.i=i
        self.bulked=list(i.bulk_)
        self._new_query=i.Query_dict
        self.calculate_queries_map()
        self.calculate_return() 

    def calculate_queries_map(self):
        for i in range(len(self.result)):
            self._new_query[i]=self.result[i]
        print(self._new_query.items()) 

    def calculate_return(self):
        print(self.bulked,"BULKED[]")
        time.sleep(32)
        new_result=[]
        for i in range(len(self.bulked)):
            for j in range(len(self.bulked)):
                _new_tester=self.bulked[i][j]
                # new_result.append(self.bulked[i][1]) 
                
        ... 

    def calculate_quantifier(self,_given):
        ... 
