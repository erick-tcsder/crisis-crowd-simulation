import math
from typing import List, Tuple
from numpy.linalg import norm
import numpy as np
import numpy as np
from shapely.geometry import Polygon
from shapely.ops import triangulate
import geopandas as gpd
from geovoronoi import voronoi_regions_from_coords


def to_triangles(polygon):

    poly_points = []

    gdf_poly_exterior = gpd.GeoDataFrame(
        {'geometry': [polygon.exterior]}).explode().reset_index()
    for geom in gdf_poly_exterior.geometry:
        poly_points += np.array(geom.coords).tolist()

    try:
        polygon.interiors[0]
    except:
        poly_points = poly_points
    else:
        gdf_poly_interior = gpd.GeoDataFrame(
            {'geometry': [polygon.interiors]}).explode().reset_index()
        for geom in gdf_poly_interior.geometry:
          poly_points += np.array(geom.coords).tolist()

    poly_points = np.array(
        [item for sublist in poly_points for item in sublist]).reshape(-1, 2)

    poly_shapes, pts = voronoi_regions_from_coords(poly_points, polygon)
    gdf_poly_voronoi = gpd.GeoDataFrame(
        {'geometry': poly_shapes}).explode().reset_index()

    tri_geom = []
    for geom in gdf_poly_voronoi.geometry:
        inside_triangles = [tri for tri in triangulate(
            geom) if tri.centroid.within(polygon)]
        tri_geom += inside_triangles

    return tri_geom

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
  