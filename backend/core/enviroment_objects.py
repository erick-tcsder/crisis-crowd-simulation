from abc import abstractmethod
from typing import List, Tuple
import math

NAGON_SIDES = 10

class EnvObj:
  @abstractmethod
  def getRoundingBox(self)->List[Tuple[float,float]]:
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
  
  

class Wall(EnvObj):
  def __init__(self,start:tuple[float],end:tuple[float]):
    self.start = start
    self.end = end
  
  def getRoundingBox(self) -> List[float]:
    pass

class RectObs(RectShaped):
  def __init__(self, coords: List[Tuple[float,float]]):
    super.__init__(self,coords)
    self.isObstacle = True
    
class CircleObs(CircleShaped):
  def __init__(self,coords:List[Tuple[float,float]]):
    super.__init__(coords)
    self.isObstacle = True
  
class Door(RectShaped):
  def __init__(self, coords: List[Tuple[float,float]]):
    super.__init__(self,coords)
    self.isObstacle = False
    
class Stairs(RectShaped):
  def __init__(self, coords: List[Tuple[float,float]], warpID:str):
    super.__init__(self,coords)
    self.isObstacle = False
    self.warpID = warpID
    
class Elevator(RectShaped):
  def __init__(self, coords: List[Tuple[float,float]], warpID:str):
    super.__init__(self,coords)
    self.isObstacle = False
    self.warpID = warpID
    
class SafeZone(RectShaped):
  def __init__(self, coords: List[Tuple[float,float]]):
    super.__init__(self,coords)
    self.isObstacle = False
    self.isSafeZone = True
    
class EvacExit(RectShaped):
  def __init__(self, coords: List[Tuple[float,float]]):
    super.__init__(self,coords)
    self.isObstacle = False
    self.isSafeZone = True
    
class EvacSign(RectShaped):
  def __init__(self, coords: List[Tuple[float,float]], angleDeg:float):
    super.__init__(self,coords)
    self.isObstacle = False
    self.angleDeg = angleDeg
    
class DamageZone(RectShaped):
  def __init__(self, coords: List[Tuple[float,float]], damageFactor:float):
    super.__init__(self,coords)
    self.isObstacle = False
    self.damageFactor = damageFactor