from functools import lru_cache, total_ordering
from typing import Dict, List, Set, Tuple
from shapely import Point, Polygon, MultiPolygon, LineString, prepare
from utils.geometry import to_triangles as triangulate
from dataclasses import dataclass
import heapq as heap

ADJACENT_MATRIX = Dict[Point, Set[Point]]


@lru_cache(maxsize=None)
def get_cached_distance(p1: Point, p2: Point) -> float:
    return p1.distance(p2)


@dataclass(slots=True)
class Navmesh:
    flat_polygon: MultiPolygon
    polygon: MultiPolygon
    adjacent: ADJACENT_MATRIX
    distances: Dict[Tuple[Point, Point], float]


def build_navmesh(
    map: MultiPolygon,
    space: float = .5
) -> Navmesh:

    # Space parameter define how much space is needed in an area
    # allow a person go through it
    map = map.buffer(-space, cap_style='flat', join_style='bevel')
    if isinstance(map, Polygon):
        map = MultiPolygon([map])

    prepare(map)

    # Delaunay triangulation, works bad for non-convex
    tris = []
    for p in map.geoms:
        # For each polygon triangulate an select only the ones within
        # original figure (clip)
        tris.extend((t for t in triangulate(p)))

    multi = MultiPolygon(tris)

    # Adjacent list, tells what are the neighbors points of a point
    adj: ADJACENT_MATRIX = {}

    prepare(multi)

    nv = Navmesh(map, multi, {}, {})
    adj: ADJACENT_MATRIX = nv.adjacent

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

            # Call the function to create a cache of distances among points in the navmesh
            get_cached_distance(edge[0], edge[1])
            get_cached_distance(center, edge[1])
            get_cached_distance(edge[0], center)

            adj[edge[0]] = n0
            adj[edge[1]] = n1

            adj[center] = adj.get(center, set())
            adj[center].update(edge)

    return nv


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


@total_ordering
class HeapObject:
    __slots__ = ('weight', 'route')

    weight: Tuple[float, float]
    route: List[Point]

    def __init__(self, weight: Tuple[float, float], route: List[Point]):
        self.weight = weight
        self.route = route

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, HeapObject):
            return sum(self.weight) == sum(__o.weight)
        else:
            return False

    def __lt__(self, __o: object) -> bool:
        return sum(self.weight) < sum(__o.weight)


def a_star(navmesh: Navmesh, start: Point, end: Point) -> Tuple[List[Point], float]:
    """
    Find the closest-enough path from `start` to `end` using the given navmesh, is not actually
    the closest path because the navmesh reduces the possible points where to find a path 
    in order to simplify the search space and therefore not optimum is assured. Returns a route
    to follow as a list of points.
    """
    # First thing is to find the closest point in the navmesh to use as start and end
    a_star_s = approx_navmesh(navmesh, start)
    a_star_e = approx_navmesh(navmesh, end)

    passed: Set[Point] = set()

    # Heuristic function used, linear distance
    def heur(p: Point, *_) -> float:
        return get_cached_distance(p, (a_star_e[0]))

    # Function to get all the neighbors possibles to a point
    def neigh(p: Point, *_) -> Set[Point]:
        return navmesh.adjacent[p]

    # Weight/distance function used for A* (distance_acc+heur).
    def weight(p: Point, parent: Tuple[Tuple[float, float],
                                       Point]) -> Tuple[float, float]:
        # First point
        if parent is None:
            return (.0, heur(p))

        last_w = parent[0]
        last_p = parent[1]

        # Take only accumulative, don't use heuristic weight
        last_w = last_w[0]

        # Accumulative distance until now plus the distance to go from
        # the last point to this plus the value of the heuristic in this
        # point
        return ((get_cached_distance(p, (last_p))+last_w), heur(p))

    h: List[HeapObject] = []  # Heap

    heap.heappush(h, HeapObject(weight(a_star_s[0], None), [a_star_s[0]]))
    while True:
        if len(h) == 0:
            return ([], -1)

        o = heap.heappop(h)
        w = o.weight
        route = o.route

        if route[-1] in passed:
            continue

        # The destination point was poped from the heap
        if route[-1].equals(a_star_e[0]):
            route=[start]+route+[end]
            # Patch to fix back-travel. Essentially check if the way between
            # the second point of the route in the A* and the real start point
            # is walkable, if that so then delete the first point in the route.
            # This will always shorten the path.
            if LineString([start, route[2]]).within(navmesh.flat_polygon):
                route = [start]+route[2:]
            # Similar process but with the last points
            if len(route) != 2:
                if LineString([end, route[-2]]).within(navmesh.flat_polygon):
                    route = route[:-2]+[end]

            # So this is the route
            # Real start and end point must be added
            full_route = [start]+route+[end]
            return (full_route, w[0])

        neighbors = neigh(route[-1])

        for n in neighbors:
            heap.heappush(h, HeapObject(weight(n, (w, route[-1])), route+[n]))

        passed.add(route[-1])


def clamp_route(navmesh: Navmesh, point: Point, route: List[Point]) -> Tuple[List[Point], bool]:
    """
    Reduce the route if the given point can go directly to a late point on the route.
    Returns the route and a boolean telling if it changed or not.
    """
    for pi in range(len(route)-1, -1, -1):
        p = route[pi]
        if LineString([point, p]).within(navmesh.flat_polygon):
            return (route[pi:], True)
    return (route, False)
