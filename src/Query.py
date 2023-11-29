
class query:
    
    @staticmethod
    def single_test(tester_key:str,tester_values:list,Pred:dict):
            seter=set() 
            for key,values in Pred.items():
                if tester_key == key:
                        for i in values.argv:
                            seter.update(i)
                        if set(tester_values).issubset(seter):
                            return True 
            return False

