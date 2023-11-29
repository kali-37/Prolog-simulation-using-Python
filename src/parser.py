import Query
import re

class Parser(Query.query):
    def arg_checker(self,argv:str,Pred:dict):
        b_S=argv.count('(')
        b_C=argv.count(')')
        p_dot= '.' in argv 
        if b_S==b_C and p_dot: 
            result=list(filter(None,re.split(r'\(|\)|\.|\,',argv)))
            key_tester=result.pop(0)
            return Query.query().single_test(key_tester,result,Pred)
        elif(b_S!=b_C):
           raise SyntaxError("SyntaxError: Unbalanced brackets detected. Ensure that the parentheses are properly matched.")
        else:
            raise SyntaxError("SyntaxError: Invalid syntax. Guess forgot '.' dot at the end of the query")