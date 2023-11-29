import Query
import re

class Parser(Query.query):


    @staticmethod 
    def arg_calculator(argv):
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
    def seprator(argv:str):
        result=list(filter(None,re.split(r'\(|\)|\.|\,',argv)))
        key_tester=result.pop(0)
        return key_tester,result



    @staticmethod
    def arg_checker(argv:str,Pred:dict):
        if Parser.arg_calculator(argv):
            key_tester,result=Parser.seprator(argv) 
            return Query.query().single_test(key_tester,result,Pred)

class Predicate_builder:

    @staticmethod
    def build(arg): 
        if Parser.arg_calculator(arg):
            # key_tester,result=Parser.seprator(arg)
            # return key_tester,result 
            return Parser.seprator(arg)
        