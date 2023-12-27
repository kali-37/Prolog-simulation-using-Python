import Queries
import re
import logging

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
        print(arg,"arg")
        result=re.match(r'(\w+)\((.*)\):-(.*)\.',arg) 
        if result:
            _quer=result.group(3)
            _quer = [x.strip() for x in re.split(r';|not|,(?=\(*\))', _quer)] # i did long way as did below 
            # _quer = [x.strip() for x in re.split(r';|not|,(?![^\(]*\))', _quer)]
            if _quer:
                return [result.group(1),[result.group(2)],_quer]
        

    @staticmethod
    def check_arguments(arg)->tuple[str,list[str]]|list[list[str]]|None|bool: 
        _tmp=Parser.validate_query(arg)
        if _tmp:
            print("TMP",_tmp)
            if _tmp=="if_query":
                _parsed_if=Parser.parse_if_query(arg)
                return _parsed_if
            else :
                return Parser.seprate_query_elems(arg)
            
        return False 
# ___________________  USER INPUT HANDLER ______________________ #
    @staticmethod
    def build(argv:str,Pred:dict):
        if Parser.validate_query(argv):
            key_tester,result=Parser.seprate_query_elems(argv) 
            if "ERROR" in result:
                return key_tester,result
            return Queries.Query().single_test(key_tester,result,Pred)


# _________________ USER INPUT HANDLER :CLOSED ________________ #