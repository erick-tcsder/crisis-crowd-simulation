from typing import Dict, List, Set, Tuple
from shapely import Point, Polygon, MultiPolygon, LineString
from shapely.ops import triangulate
from dataclasses import dataclass
import numpy as np

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
