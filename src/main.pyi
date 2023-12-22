class Predicate:
    predicates:dict[str|float|int,"Predicate"] = {}

    def __init__(self,name:str)->None:
        self.name:str 
        self.argv:list[str] 
        ...
       
    def add_arg(self,argv: list[str|int|float])-> None:
        ...

    def __str__(self)->str:
        ...
