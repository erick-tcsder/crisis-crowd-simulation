from abc import abstractmethod
from typing import List, Tuple
import math

NAGON_SIDES = 10

class EnvObj:
  @abstractmethod
  def getRoundingBox(self)->List[Tuple[float,float]]:
    raise NotImplementedError()
  
  @abstractmethod
  def toJson(self)->dict:
    raise NotImplementedError()
  
  @abstractmethod
  @staticmethod
  def fromJson(json:dict):
    raise NotImplementedError()
  
  
  
class RectShaped(EnvObj):
  def __init__(self, coords: List[Tuple[float,float]]):
    self.coords = coords
    
  def getRoundingBox(self) -> List[Tuple[float,float]]:
    return self.coords
  
  
  
class CircleShaped(EnvObj):
  def __init__(self, coords: List[Tuple[float,float]]):
    self.coords = coords
    self.center = ((coords[0][0]+coords[2][0])/2,(coords[0][1]+coords[2][1])/2)
    self.radius = abs(coords[1][0] - coords[0][0])/2
    
  def getRoundingBox(self) -> List[Tuple[float, float]]:
    singleAngle = 2*math.pi/NAGON_SIDES
    halfDiag = self.radius / math.cos(singleAngle/2)
    box=[]
    for i in [i for i in range(NAGON_SIDES)]:
      box.append((self.center[0]+halfDiag*math.cos(i*singleAngle),self.center[1]+halfDiag*math.sin(i*singleAngle)))
    return box

class RectObs(RectShaped):
  def __init__(self, coords: List[Tuple[float,float]]):
    super.__init__(self,coords)
    self.isObstacle = True
    
  def toJson(self):
    return {
      'OBJECT_TYPE':'RECTANGULAR_OBSTACLE',
      'props': {
        'top':self.coords[0][1],
        'left':self.coords[0][0],
        'width':self.coords[1][0]-self.coords[0][0],
        'height':self.coords[1][1] - self.coords[0][1]
      }
    }
    
  def fromJson(json:dict):
    return RectObs([(json['props']['left'],json['props']['top']),(json['props']['left']+json['props']['width'],json['props']['top']+json['props']['height'])])

class CircleObs(CircleShaped):
  def __init__(self,coords:List[Tuple[float,float]]):
    super.__init__(coords)
    self.isObstacle = True
    
  def toJson(self):
    return {
      'OBJECT_TYPE':'CIRCULAR_OBSTACLE',
      'props': {
        'top': self.coords[0][1],
        'left': self.coords[0][0],
        'width': self.coords[1][0] - self.coords[0][0],
        'height': self.coords[1][1] - self.coords[0][1],
        'radius': self.radius*2
      }
    }
  def fromJson(json:dict):
    return CircleObs([(json['props']['left'],json['props']['top']),(json['props']['left']+json['props']['width'],json['props']['top']+json['props']['height'])])
  
class Door(RectShaped):
  def __init__(self, coords: List[Tuple[float,float]]):
    super.__init__(self,coords)
    self.isObstacle = False
    
  def toJson(self):
    return {
      'OBJECT_TYPE':'DOOR',
      'props': {
        'top':self.coords[0][1],
        'left':self.coords[0][0],
        'width':self.coords[1][0]-self.coords[0][0],
        'height':self.coords[1][1] - self.coords[0][1]
      }
    }
    
  def fromJson(json:dict):
    return Door([(json['props']['left'],json['props']['top']),(json['props']['left']+json['props']['width'],json['props']['top']+json['props']['height'])])
    
class Stairs(RectShaped):
  def __init__(self, coords: List[Tuple[float,float]], warpID:str):
    super.__init__(self,coords)
    self.isObstacle = False
    self.warpID = warpID
    
  def toJson(self):
    return {
      'OBJECT_TYPE':'STAIRS',
      'props': {
        'top':self.coords[0][1],
        'left':self.coords[0][0],
        'width':self.coords[1][0]-self.coords[0][0],
        'height':self.coords[1][1] - self.coords[0][1],
        'label':self.warpID
      }
    }
  
  def fromJson(json:dict):
    return Stairs([(json['props']['left'],json['props']['top']),(json['props']['left']+json['props']['width'],json['props']['top']+json['props']['height'])],json['props']['label'])
  
class Elevator(RectShaped):
  def __init__(self, coords: List[Tuple[float,float]], warpID:str):
    super.__init__(self,coords)
    self.isObstacle = False
    self.warpID = warpID
    
  def toJson(self):
    return {
      'OBJECT_TYPE':'STAIRS',
      'props': {
        'top':self.coords[0][1],
        'left':self.coords[0][0],
        'width':self.coords[1][0]-self.coords[0][0],
        'height':self.coords[1][1] - self.coords[0][1],
        'label':self.warpID
      }
    }
    
  def fromJson(json:dict):
    return Elevator([(json['props']['left'],json['props']['top']),(json['props']['left']+json['props']['width'],json['props']['top']+json['props']['height'])],json['props']['label'])
    
class SafeZone(RectShaped):
  def __init__(self, coords: List[Tuple[float,float]]):
    super.__init__(self,coords)
    self.isObstacle = False
    self.isSafeZone = True
    
  def toJson(self):
    return {
      'OBJECT_TYPE':'SAFE_ZONE',
      'props': {
        'top':self.coords[0][1],
        'left':self.coords[0][0],
        'width':self.coords[1][0]-self.coords[0][0],
        'height':self.coords[1][1] - self.coords[0][1]
      }
    }
  def fromJson(json:dict):
    return SafeZone([(json['props']['left'],json['props']['top']),(json['props']['left']+json['props']['width'],json['props']['top']+json['props']['height'])])
    
class EvacExit(RectShaped):
  def __init__(self, coords: List[Tuple[float,float]]):
    super.__init__(self,coords)
    self.isObstacle = False
    self.isSafeZone = True
    
  def toJson(self):
    return {
      'OBJECT_TYPE':'EVAC_EXIT',
      'props': {
        'top':self.coords[0][1],
        'left':self.coords[0][0],
        'width':self.coords[1][0]-self.coords[0][0],
        'height':self.coords[1][1] - self.coords[0][1]
      }
    }
  def fromJson(json:dict):
    return EvacExit([(json['props']['left'],json['props']['top']),(json['props']['left']+json['props']['width'],json['props']['top']+json['props']['height'])])
    
class EvacSign(RectShaped):
  def __init__(self, coords: List[Tuple[float,float]], angleDeg:float):
    super.__init__(self,coords)
    self.isObstacle = False
    self.angleDeg = angleDeg
  def toJson(self):
    return {
      'OBJECT_TYPE':'EVAC_SIGN',
      'props': {
        'top':self.coords[0][1],
        'left':self.coords[0][0],
        'width':self.coords[1][0]-self.coords[0][0],
        'height':self.coords[1][1] - self.coords[0][1],
        'direction': 'left' if self.angleDeg == 180 else ('right' if self.angleDeg == 0 else ('up' if self.angleDeg == 90 else 'down')) 
      }
    }
  def fromJson(json):
    angle = json['props']['direction']
    angle = 180 if angle == 'left' else (0 if angle == 'right' else (90 if angle == 'up' else 270))
    return EvacSign([(json['props']['left'],json['props']['top']),(json['props']['left']+json['props']['width'],json['props']['top']+json['props']['height'])],angle)
    
class DamageZone(RectShaped):
  def __init__(self, coords: List[Tuple[float,float]], damageFactor:float):
    super.__init__(self,coords)
    self.isObstacle = False
    self.damageFactor = damageFactor
    
  def toJson(self):
    return {
      'OBJECT_TYPE':'DAMAGE_ZONE',
      'props': {
        'top':self.coords[0][1],
        'left':self.coords[0][0],
        'width':self.coords[1][0]-self.coords[0][0],
        'height':self.coords[1][1] - self.coords[0][1],
        'damageFactor': self.damageFactor
      }
    }
    
  def fromJson(json):
    return DamageZone([(json['props']['left'],json['props']['top']),(json['props']['left']+json['props']['width'],json['props']['top']+json['props']['height'])],json['props']['damageFactor'])