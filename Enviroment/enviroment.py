from utils.position import *
from objEntities import *
from abc import ABC

class Floor:
    def __init__(self, n_windows: int, n_doors: int, n_evacuation_signals: int, floor_number: int, n_stairs,
                 objEntities: list(ObjEntity), length: int, width: int, n_agents):
        self.n_windows = n_windows
        self.n_doors = n_doors
        self.n_evacuation_signals = n_evacuation_signals
        self.n_stairs = n_stairs
        self.n_agent = n_agents
        self.id = floor_number
        self.objEntities = objEntities
        self.length = length
        self.width = width
        self.structure = objEntities[length,width]
    
    def initializeParameters(self):
        pass

class Building:
    def __init__(self, n_floors: int, n_doors: int):
        self.n_floors = n_floors
        self.n_doors = n_doors        
    
    def initializeParameters(self):
        pass