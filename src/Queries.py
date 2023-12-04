class Query:
    @staticmethod
    def single_test(tester_key:str,tester_values:list,Pred:dict)->None | bool | list |set:
            nums:int=0
            for i in set(tester_values):
                if len(i)==1 and i.isupper():
                    nums+=1
                    tester_values.remove(i) 
            return Query.test_calculation(tester_key,tester_values,Pred,nums)


    @staticmethod 
    def calc_value_within(tester_values,values,nums) ->bool | list |None |set:
        leter=set()
        if len(tester_values)==0:
            for i in values.argv:
                if len(i)+1==nums:
                    return i
        for i in values.argv:
            if set(tester_values).issubset(set(i)):
                leter=set(i) 
        if set(tester_values).issubset(leter) and not  nums:
            return True 
        else : 
            return leter 


    @staticmethod
    def test_calculation(tester_key:str,tester_values:list,Pred:dict,nums) ->bool | list |set|None:
            for key,values in Pred.items():
                if tester_key == key:
                    returned_value=Query.calc_value_within(tester_values,values,nums)
                    if type(returned_value)==bool:
                        return True
                    elif type(returned_value)==set :
                       return  Query.furtherCalc(returned_value,nums,tester_values)
                    else:
                        return returned_value
            return False     

    @staticmethod
    def furtherCalc(values,nums,tester_values)->set|None:
        return values-set(tester_values).intersection(values)
        # return taka
