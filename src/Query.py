class so(list):
    def __hash__(self):
        temp=0
        for i in self:
            temp+=hash(i)# i.__hash__()
        return temp



class query:
    @staticmethod
    def single_test(tester:list,Pred:dict):
            tester.append("bobby")
            tester.append("new")
            print(tester[1:])
        
            for i in Pred:
                if tester[0] == i:
                        print("tester..>>",tester[1:],"pred..->",Pred[i].argv)
                        seter=set(Pred[i].argv)
                        # for arg in Pred[i].argv: 
                            # seter.add(arg) 
                        print(Pred[i].argv)
                        print(seter)
                        if set(tester[1:]).issubset(seter):
                            return True 
            return False



# Converting list to set in python as :
# set(list)




