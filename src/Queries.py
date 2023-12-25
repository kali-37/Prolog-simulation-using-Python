import copy
import logging

if __name__=="__main__":
    from main import Predicate

class Query:
    @staticmethod
    def single_test(tester_key:str,tester_values:list|tuple,Pred:dict[str,"Predicate"])->None | bool | list |set:
            logging.info("QUERY_single_test started")
            nums:int =0
            results=[]

            _index_nums=[]
            _indx_err=False
            _values=None
            for _key,values in Pred.items():
                if  _key==tester_key  :
                    if isinstance(values.argv,list):
                        _values=values.argv
                _master_tester=tester_values
                logging.info("QUERY_single_test ")
                _real=None 
                if  _values:
                    for i in _values:
                            tester_values=copy.copy(_master_tester)
                            _copy_tester=tuple(tester_values) 
                            if not  len(i)==len(tester_values) or not set(i).intersection(set(_copy_tester)) :
                                continue
                            _indx_err=False
                            nums=0
                            for ie in range(len(_copy_tester)):
                                if len(_copy_tester[ie])==1 and _copy_tester[ie].isupper():
                                    nums+=1
                                    _index_nums.append(ie)
                                    tester_values.remove(_copy_tester[ie]) 
#                                else :
#                                        try:
#                                            if _copy_tester[ie]!=i[ie] and ie<=len(_copy_tester)-1:
#                                                raise ValueError("ERROR: INDEXING IS HANDELED STRICTLY ")
#
#                                        except ValueError as e:
#                                            print(e)
#                                            return False
#                            return Query.test_calculation(tester_values,i,nums,_index_nums)
#            return False
                                else:
                                    if _copy_tester[ie]!=i[ie] and ie<=len(_copy_tester)-1:
                                            _indx_err=True
                            if not _indx_err :
                                results.append([tester_values,i,nums,_index_nums] )
            if results:
                return Query.test_calculation(results)
            if _indx_err:
                print("ERROR : Indexing must be strict , Irregular Flow detected")
                return False
            return False
    @staticmethod 
    def calc_value_within(tester_values,values,nums,_index_nums) ->bool | list |None |set:
        if set(tester_values).issubset(set(values)):
            if not nums:
                return True 
            elif len(tester_values)+nums==len(values) :
                return set(values[i] for i in _index_nums)
        else :
             return False

                                
    @staticmethod
    # search tester_key(tester_values:list) in Predicate dictionary 
    # def test_calculation(tester_values:list,Pred_values:list|str,nums,_index_nums) ->bool | list |set|None:
    #                 returned_value=Query.calc_value_within(tester_values,Pred_values,nums,_index_nums)
    #                 if type(returned_value)==bool:
    #                     return returned_value
    #                 elif type(returned_value)==set :
    #                    return returned_value 
    #                 else:
    #                     return returned_value

    def test_calculation(returned_values):
                    _finally=[]
                    for returned_value in returned_values:
                        returned_value=Query.calc_value_within(returned_value[0],returned_value[1],returned_value[2],returned_value[3])
                        if type(returned_value)==bool:
                            return returned_value
                        elif type(returned_value)==set :
                            _finally.append(returned_value)
                        #    return returned_value 
                        else:
                            return returned_value
                    return  _finally

