from typing import Dict, List, Set, Tuple
from shapely import Point, Polygon, MultiPolygon, LineString
from shapely.ops import triangulate
from dataclasses import dataclass
import heapq as heap

ADJACENT_MATRIX = Dict[Point, Set[Point]]


@dataclass(slots=True)
class Navmesh:
    polygon: MultiPolygon
    adjacent: ADJACENT_MATRIX


def build_navmesh(
    map: Polygon,
    obstacles: List[Polygon],
    space: float = .005
) -> Navmesh:
    map = MultiPolygon([map])
    for obs in obstacles:
        map = map.difference(obs)

    # Space parameter define how much space is needed in an area
    # allow a person go through it
    map = map.buffer(-space, cap_style='flat', join_style='bevel')

    # Delaunay triangulation, works bad for non-convex
    tris = []
    for p in map.geoms:
        # For each polygon triangulate an select only the ones within
        # original figure (clip)
        tris.extend((t for t in triangulate(p) if t.within(map)))

    multi = MultiPolygon(tris)

    # Adjacent list, tells what are the neighbors points of a point
    adj: ADJACENT_MATRIX = {}

    for t in multi.geoms:
        center = Point(t.centroid)
        edge_t: LineString = t.boundary
        # Pair the points with the next one to get edges
        for edge in zip(edge_t.coords[:-1], edge_t.coords[1:]):
            # Sometimes shapely use tuples instead of point. Massive confusion.
            edge = (Point(edge[0]), Point(edge[1]))

            n0 = adj.get(edge[0], set())
            n1 = adj.get(edge[1], set())

            n0.add(edge[1])
            n1.add(edge[0])
            n0.add(center)
            n1.add(center)

            adj[edge[0]] = n0
            adj[edge[1]] = n1

            adj[center] = adj.get(center, set())
            adj[center].update(edge)

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

    # Find the tri with the minimum distance to the given point
    p_tri = (tris[0], p.distance(tris[0]))
    for t in tris[1:]:
        d = p.distance(t)
        if d < p_tri[1]:
            p_tri = (t, d)

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
        # Just return the centroid if the borders are not valid
        return (center, _in, True)


@dataclass(slots=True, order=True, unsafe_hash=True)
class __HeapObjectBase:
    weight: float


class HeapObject(__HeapObjectBase):
    __slots__ = ('route')

    route: List[Point]

    def __init__(self, weight: float, route: List[Point]):
        super().__init__(weight)
        self.route = route


def a_star(navmesh: Navmesh, start: Point, end: Point) -> Tuple[List[Point], float]:
    """
    Find the closest-enough path from `start` to `end` using the given navmesh, is not actually
    the closest path because the navmesh reduces the possible points where to find a path 
    in order to simplify the search space and therefore not optimum is assured. Returns a route
    to follow as a list of points.
    """
    # TODO: Fix slowness
    # TODO: Fix back-travel at start and end

    # First thing is to find the closest point in the navmesh to use as start and end
    a_star_s = approx_navmesh(navmesh, start)
    a_star_e = approx_navmesh(navmesh, end)

    # Heuristic function used, linear distance
    def heur(p: Point, *_) -> float:
        return p.distance(a_star_e[0])

    # Function to get all the neighbors possibles to a point
    def neigh(p: Point, *_) -> Set[Point]:
        return navmesh.adjacent[p]

    # Weight/distance function used for A* (distance_acc+heur).
    def weight(p: Point, parent: Tuple[float, Point]) -> float:
        # First point
        if parent is None:
            return heur(p)

        last_w = parent[0]
        last_p = parent[1]

        # Remove last point heuristic to get pure accumulative distance
        # Its possible to do this because heuristic function is fast
        last_w -= heur(last_p)

        # Accumulative distance until now plus the distance to go from
        # the last point to this plus the value of the heuristic in this
        # point
        return (p.distance(last_p)+last_w)+heur(p)

    h: List[HeapObject] = []  # Heap

    heap.heappush(h, HeapObject(weight(a_star_s[0], None), [a_star_s[0]]))
    while True:
        o = heap.heappop(h)
        w = o.weight
        route = o.route

        # The destination point was poped from the heap
        if route[-1].equals(a_star_e[0]):
            # So this is the route
            # Real start and end point must be added
            return (([start]+route+[end]), w)

        neighbors = neigh(route[-1])

        for n in neighbors:
            heap.heappush(h, HeapObject(weight(n, (w, route[-1])), route+[n]))
