import math
from typing import List, Tuple
from numpy.linalg import norm
import numpy as np

def internal_angles(p1: Tuple[float, float], 
                    p2: Tuple[float, float], 
                    p3: Tuple[float, float]) -> List[float]:
  v1 = (p2[0] - p1[0], p2[1] - p1[1])
  v2 = (p3[0] - p2[0], p3[1] - p2[1])
  v3 = (p1[0] - p3[0], p1[1] - p3[1])

  a1 = math.degrees(math.acos(
    (-1 * v1[0] * v2[0] - v1[1] * v2[1]) /
    (math.sqrt(v1[0] ** 2 + v1[1] ** 2) * math.sqrt(v2[0] ** 2 + v2[1] ** 2))
  ))
  a2 = math.degrees(math.acos(
    (-1 * v2[0] * v3[0] - v2[1] * v3[1]) /
    (math.sqrt(v2[0] ** 2 + v2[1] ** 2) * math.sqrt(v3[0] ** 2 + v3[1] ** 2))
  ))
  a3 = math.degrees(math.acos(
    (-1 * v3[0] * v1[0] - v3[1] * v1[1]) /
    (math.sqrt(v3[0] ** 2 + v3[1] ** 2) * math.sqrt(v1[0] ** 2 + v1[1] ** 2))
  ))

  return [a1, a2, a3]

def getDistanceAB(a: Tuple[float,float],b:Tuple[float,float]) -> float:
  return math.sqrt((a[1]-b[1])**2 + (a[0]-b[0])**2)

def getDistancePr(p: Tuple[float,float],r: Tuple[Tuple[float,float],Tuple[float,float]]) -> float:
  A,B = r
  if all(A==p) or all(B==p):
    return 0

  elif np.arccos(np.dot((p-A)/norm(p-A), (B-A)/norm(B-A))) > np.pi/2:
    return norm(p-A)

  elif np.arccos(np.dot((p-B)/norm(p-B), (A-B)/norm(A-B))) > np.pi/2:
    return norm(p-B)

  return norm(np.cross(B-A, A-p))/norm(B-A)
  
def getDistancePtoPolygon(p: Tuple[float,float], polygon: List[Tuple[float,float]])-> float:
  min = 10e8
  for i in range(len(polygon)):
    a = polygon[i]
    b = polygon[i+1 % len(polygon)]
    d = getDistancePr(p,(a,b))
    if d < min: min = d
  