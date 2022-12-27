from enum import Enum

class ObjectCategory(Enum):
  Wall = 'WALL'
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
  match json.type:
    case ObjectCategory.Wall:
      pass
    case ObjectCategory.RectObstacle:
      pass
  
class Blueprint:
  width: int
  height: int
  def __init__(self,w:int,h:int) -> None:
    self.height = h
    self.width = w
  
class FloorBlueprint(Blueprint):
  objects = []
  def __init__(self, w: int, h: int) -> None:
    super().__init__(w, h)
    
  def readObjects(json):
    # TODO: read objects from json
    pass