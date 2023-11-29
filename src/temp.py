from collections.abc import Iterable

class hash_list(list): 
    def __init__(self, *args): 
        if len(args) == 1 and isinstance(args[0], Iterable): 
            args = args[0] 
        super().__init__(args) 
         
    def __hash__(self): 
        return hash(e for e in self)


ser=[[1,3,4,4]]
print(hash(hash_list(ser)))
print(set(ser))