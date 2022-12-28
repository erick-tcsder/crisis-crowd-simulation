from typing import Dict, List, Set, Tuple
from shapely import Point, Polygon, MultiPolygon, LineString
from shapely.ops import triangulate
from dataclasses import dataclass
import time

ADJACENT_MATRIX = Dict[Polygon, Set[Polygon]]


@dataclass(slots=True)
class Navmesh:
    polygon: MultiPolygon
    adjacent: ADJACENT_MATRIX


def build_navmesh(
    map: Polygon,
    obstacles: List[Polygon],
) -> Navmesh:
    map = MultiPolygon([map])
    for obs in obstacles:
        map = map.difference(obs)

    # Delaunay triangulation, works bad for non-convex
    tris = []
    for p in map.geoms:
        # For each polygon triangulate an select only the ones within
        # original figure (clip)
        tris.extend((t for t in triangulate(p) if t.within(map)))

    multi = MultiPolygon(tris)

    # Stores for every edge the maximum two triangles that have it
    twins: Dict[Tuple[Point, Point], List[Polygon]] = {}

    # Adjacent list, tells what are the neighbors tris of a tri
    adj: ADJACENT_MATRIX = {}

    for t in multi.geoms:
        edge_t: LineString = t.boundary
        # Pair the points with the next one to get edges
        for edge in zip(edge_t.coords[:-1], edge_t.coords[1:]):
            l = twins.get(edge, [])

            if len(l) == 0:
                l = twins.get(
                    (edge[1], edge[0]), [])  # may be in reverse
                twins[(edge[1], edge[0])] = l
            else:
                twins[edge] = l
            # t has this as an edge so add it
            l.append(t)

            # Already has two (the maximum)
            if len(l) == 2:
                # So they are neighbors
                adj[l[0]] = adj.get(l[0], set())
                adj[l[0]].add(l[1])
                adj[l[1]] = adj.get(l[1], set())
                adj[l[1]].add(l[0])

    return Navmesh(multi, adj)


def approx_navmesh(navmesh: Navmesh, p: Point, allow_borders=True) -> Tuple[Point, bool, bool]:
    """
    Given a navmesh and a point gives the closest point o the navmesh to the given point.
    If `allow_borders` is `True` it can give points that are in the borders of the navmesh.
    
    Returns a tuple (`p`,`in`,`center`) where:
    - `p` is the point of the navmesh.
    - `in` is a boolean that is `True` if the point given is at least inside the geometry
    of the navmesh, `False` otherwise.
    - `center` is a boolean that is `True` if the point in the return is the center of
    a triangle in the navmesh, `False` otherwise. Must be always `True` if `allow_borders`
    is `False`.
    """
    tris = list(navmesh.polygon.geoms)

    start = time.time()

    # Find the tri with the minimum distance to the given point
    p_tri = (tris[0], p.distance(tris[0]))
    for t in tris[1:]:
        d = p.distance(t)
        if d < p_tri[1]:
            p_tri = (t, d)

    print(f"Finished tri find in {time.time()-start:.3f}s")

    # If the distance is 0 or below is because is inside
    _in = p_tri[1] <= .0

    # Get the centroid of the closest triangle
    center = p_tri[0].centroid

    if allow_borders:
        # From all the points in the border pick the closest
        tri_points: List[Point] = [Point(p) for p in p_tri[0].boundary.coords]
        f_p = (tri_points[0], p.distance(tri_points[0]))
        for tp in tri_points[1:]:
            d = p.distance(tp)
            if d < f_p[1]:
                f_p = (tp, d)

        # Compare the closest border to the centroid and pick closest
        if p.distance(center) < f_p[1]:
            return (center, _in, True)  # Centroid is closer
        else:
            return (f_p[0], _in, False)  # The border was closer
    else:
        #Just return the centroid if the borders are not valid
        return (center, _in, True)


def a_star(navmesh: Navmesh, start: Point, end: Point) -> Tuple[List[Point], Point, Point]:
    # First thing is to find the closest point in the navmesh to use as start and end

    tris = navmesh.polygon.geoms

    # Get the closest tri to start point
    start_tri = (tris[0], start.distance(tris[0]))
    for t in tris[1:]:
        d = start.distance(t)
        if d < start_tri[1]:
            start_tri = (t, d)

    # Get the closest tri to end point
    end_tri = (tris[0], end.distance(tris[0]))
    for t in tris[1:]:
        d = end.distance(t)
        if d < end_tri[1]:
            end_tri = (t, d)

    # Get the closest point of each tri (Center or vertices)
    st_points: List[Point] = list(start_tri[0].coords)+[start_tri[0].centroid]
    end_points: List[Point] = list(end_tri[0].coords)+[end_tri[0].centroid]

    start_pos = (st_points[0], start)
    for p in st_points:
        pass
