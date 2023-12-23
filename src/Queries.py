import logging
from re import T

if __name__=="__main__":
    from main import Predicate

class Query:
    @staticmethod
    def single_test(tester_key:str,tester_values:list,Pred:dict[str,"Predicate"])->None | bool | list |set:
            logging.info("QUERY_single_test started")
            nums:int =0
            _index_nums=[]
            # logging.log(logging.WARN,msg=f"{logging.WARN} logg 0")
            _values=None
            for _key,values in Pred.items():
                if  _key==tester_key  :
                    if isinstance(values.argv,list):
                        _values=values.argv
            # try:
                logging.info("QUERY_single_test -> TRY >>")
                _real=None 
                if  _values:
                    for i in _values:
                            _copy_tester=tuple(tester_values) 
                            if not  len(i)==len(tester_values) or not set(i).intersection(set(_copy_tester)) :
                                continue
                            # logging.warning(f"watchout",i)
                            for ie in range(len(_copy_tester)):

                                if len(_copy_tester[ie])==1 and _copy_tester[ie].isupper():
                                    nums+=1
                                    _index_nums.append(ie)
                                    tester_values.remove(_copy_tester[ie]) 
                                else :
                                        try:
                                            if _copy_tester[ie]!=i[ie] and ie<=len(_copy_tester)-1:
                                                raise ValueError("ERROR: INDEXING IS HANDELED STRICTLY ")

                                        except ValueError as e:
                                            print(e)
                                            return False
                    
                            return Query.test_calculation(tester_values,i,nums,_index_nums)

            return False

    @staticmethod 
    def calc_value_within(tester_values,values,nums,_index_nums) ->bool | list |None |set:
        if set(tester_values).issubset(set(values)):
            if len(tester_values)+nums==len(values) :
                return set(values[i] for i in _index_nums)
            elif not nums:
                 return True 
        else :
             return False

                                
    @staticmethod
    # search tester_key(tester_values:list) in Predicate dictionary 
    def test_calculation(tester_values:list,Pred_values:list|str,nums,_index_nums) ->bool | list |set|None:
                    returned_value=Query.calc_value_within(tester_values,Pred_values,nums,_index_nums)
                    if type(returned_value)==bool:
                        return returned_value
                    elif type(returned_value)==set :
                       return returned_value 
                    else:
                        return returned_value

