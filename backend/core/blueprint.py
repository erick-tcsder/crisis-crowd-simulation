from enum import Enum
from typing import List
from .enviroment_objects import EnvObj
from .enviroment_objects import *

class ObjectCategory(Enum):
  RectObstacle = 'RECTANGULAR_OBSTACLE'
  CircObstacle = 'CIRCLE_OBSTACLE'
  Door = 'DOOR'
  Stairs = 'STAIRS'
  Elevator = 'ELEVATOR'
  SafeZone = 'SAFE_ZONE'
  EvacExit = 'EVAC_EXIT'
  EvacSign = 'EVAC_SIGN'
  DamageZone = 'DAMAGE_ZONE'  
  
def toObj(json):
  match json["OBJECT_TYPE"]:
    case ObjectCategory.RectObstacle:
      RectObs.fromJson(json)
    case ObjectCategory.CircObstacle:
      CircleObs.fromJson(json)
    case ObjectCategory.Door:
      Door.fromJson(json)
    case ObjectCategory.Stairs:
      Stairs.fromJson(json)
    case ObjectCategory.Elevator:
      Elevator.fromJson(json)
    case ObjectCategory.SafeZone:
      SafeZone.fromJson(json)
    case ObjectCategory.EvacExit:
      EvacExit.fromJson(json)
    case ObjectCategory.EvacSign:
      EvacSign.fromJson(json)
    case ObjectCategory.DamageZone:
      DamageZone.fromJson(json)
  
class Blueprint:
  width: int
  height: int
  name: str
  objects: List[EnvObj]
  def __init__(self,w:int,h:int,name:str) -> None:
    self.height = h
    self.width = w
    self.name = name
    self.objects = []
    
  @staticmethod
  def fromJson(json):
    blueprint = Blueprint(json.width,json.height,json.name)
    blueprint = [toObj(obj) for obj in json.items]
    return blueprint
  
  def toJson(self):
    return {
      'width':self.width,
      'height':self.height,
      'name':self.name,
      'items':[obj.toJson() for obj in self.objects]
    }