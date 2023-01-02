from enum import Enum
from typing import List
from .environment_objects import EnvObj
from .environment_objects import *


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
    case ObjectCategory.RectObstacle.value:
      return RectObs.fromJson(json)
    case ObjectCategory.CircObstacle.value:
      return CircleObs.fromJson(json)
    case ObjectCategory.Door.value:
      return Door.fromJson(json)
    case ObjectCategory.Stairs.value:
      return Stairs.fromJson(json)
    case ObjectCategory.Elevator.value:
      return Elevator.fromJson(json)
    case ObjectCategory.SafeZone.value:
      return SafeZone.fromJson(json)
    case ObjectCategory.EvacExit.value:
      return EvacExit.fromJson(json)
    case ObjectCategory.EvacSign.value:
      return EvacSign.fromJson(json)
    case ObjectCategory.DamageZone.value:
      return DamageZone.fromJson(json)


class Blueprint:
  width: int
  height: int
  name: str
  objects: List[EnvObj]

  def __init__(self, w: int, h: int, name: str) -> None:
    self.height = h
    self.width = w
    self.name = name
    self.objects = []

  @staticmethod
  def fromJson(json):
    blueprint = Blueprint(json.width, json.height, json.name)
    blueprint.objects = [toObj(obj) for obj in json.items]
    return blueprint

  def toJson(self):
    return {
        'width': self.width,
        'height': self.height,
        'name': self.name,
        'items': [obj.toJson() for obj in self.objects]
    }
