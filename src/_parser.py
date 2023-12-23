import Queries
import re
import logging
# logging.basicConfig(level=logging.INFO)
class Parser(Queries.Query):
    @staticmethod 
    def validate_query(argv):
        logging.info("Parser")  
        b_S=argv.count('(')
        b_C=argv.count(')')
        p_dot= '.' in argv   
        try:  
            if b_S==b_C and p_dot:
                return True
            elif b_S != b_C:
                raise SyntaxError("SyntaxError: Unbalanced brackets detected. Ensure that the parentheses are properly matched.")
            else:
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
    def check_arguments(arg): 
        if Parser.validate_query(arg):
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