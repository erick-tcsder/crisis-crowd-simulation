from utils.position import *
from abc import abstractmethod, ABC

class ObjEntity:
    def __init__(self, name, position: Position):
        self.id  = name;
        self.pos= position
    
    @abstractmethod
    def interact(self): pass
    
    @abstractmethod
    def interact(self,value): pass
    
    @abstractmethod
    def relevance(self): pass
    
    @abstractmethod
    def relevance(self,value): pass
    
    @abstractmethod   
    def initializeParameters(self):pass

