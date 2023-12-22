import logging
# logging.basicConfig()
if __name__=="__main__":
    from main import Predicate

class Query:
    @staticmethod
    def single_test(tester_key:str,tester_values:list,Pred:dict[str,"Predicate"])->None | bool | list |set:
            nums:int=0
            # logging.log(logging.WARN,msg=f"{logging.WARN} logg 0")
            for _key,values in Pred.items():
                 print(_key,type(values.argv))
                 if  _key==tester_key and  values.argv :
                    for i in values.argv:
                        print("HERE WE GO ")
                        if len(i)==len(tester_key):
                            logging.critical("watchout") 
                            for i in set(tester_values):
                                if len(i)==1 and i.isupper():
                                    nums+=1
                                    tester_values.remove(i) 
                                    print("N",nums)
                                return Query.test_calculation(tester_key,tester_values,i,nums)
            return False
    @staticmethod 
    def calc_value_within(tester_values,values,nums) ->bool | list |None |set:
        leter=set()
        # if len(tester_values)==0:
        #     for i in values.argv:
        #         if len(i)+1==nums:
        #             return i
        Found=False
        for i in values.argv:
            if set(tester_values).issubset(set(i)):
                Found=True
                leter=set(i) 
        if not Found:
            return False 
        elif set(tester_values).issubset(leter) and not  nums:
            return True 
        else : 
            return leter 

    @staticmethod
    # search tester_key(tester_values:list) in Predicate dictionary 
    def test_calculation(tester_key:str,tester_values:list,Pred_values:list,nums) ->bool | list |set|None:
            #     if tester_key == key:
                    print("TOO>>>")
                    returned_value=Query.calc_value_within(tester_values,Pred_values,nums)
                    if type(returned_value)==bool:
                        return returned_value
                    elif type(returned_value)==set :
                       return  Query.furtherCalc(returned_value,nums,tester_values)
                    else:
                        return returned_value

    @staticmethod
    def furtherCalc(values,nums,tester_values)->set|None:
        return values-set(tester_values).intersection(values)
