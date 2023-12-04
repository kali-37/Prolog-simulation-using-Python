import Queries
import re

class Parser(Queries.Query):
    @staticmethod 
    def validate_query(argv):
        b_S=argv.count('(')
        b_C=argv.count(')')
        p_dot= '.' in argv        
        if b_S==b_C and p_dot:
            return True
        elif b_S != b_C:
            raise SyntaxError("SyntaxError: Unbalanced brackets detected. Ensure that the parentheses are properly matched.")
        else:
            raise SyntaxError("SyntaxError: Invalid syntax. Guess forgot '.' dot at the end of the query")

    @staticmethod 
    def seprate_query_elems(argv:str):
        result=list(filter(None,re.split(r'\(|\)|\.|\,|\n',argv)))
        key_tester=result.pop(0)
        return key_tester,result

  

    @staticmethod
    def check_arguments(argv:str,Pred:dict):
            key_tester,result=Parser.seprate_query_elems(argv) 
            return Queries.Query().single_test(key_tester,result,Pred)


    @staticmethod
    def build(arg): 
        if Parser.validate_query(arg):
            return Parser.seprate_query_elems(arg)