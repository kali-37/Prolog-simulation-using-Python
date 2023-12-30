from typing import Sequence, Union
class Relations:    
    _relation_obj:list["Relations"]=[]
    # predicate,predicate_instances , operator:str    -> bulk_
    def __init__(self,relate,queries_map:list[str],bulk_: Sequence[Union[str,list[str]]]):
        self.relate=relate 
        self.bulk_=bulk_ # For : Predicate, Predicate_instance and operator :
        self.queries_map=queries_map
        # self.predicate=predicate 
        # self.operator=operator 
        Relations._relation_obj.append(self)
        self.Query_dict={}
        self.map_query_variations()

    def map_query_variations(self):
        for _x in self.queries_map:
            self.Query_dict[_x]=""


    def __repr__(self):
        return self.relate       
