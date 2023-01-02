from functools import reduce
from typing import List

import numpy as np
from shapely import MultiPolygon, Point, Polygon, prepare

import parameters as params

from .agents import Pedestrian
from .environment.blueprint import Blueprint
from .environment.enviroment_objects import Door, EnvObj
from .navmesh import Navmesh, build_navmesh, a_star, clamp_route


class SimulationContext:
    map_blueprint: Blueprint
    agents: List[Pedestrian]

    obstacle_map: MultiPolygon  # Map is what is'nt obstacle
    safe_zone_map: MultiPolygon  # Map is what is safe zone
    danger_zone_map: MultiPolygon  # Map is what is danger zone

    danger_zones: List[Polygon]
    safe_zones: List[Polygon]

    navmesh: Navmesh
    routes: List[List[Point]]

    def __init__(self, map: Blueprint) -> None:
        self.map_blueprint = map

        obs: List[Polygon] = []
        cull: List[Polygon] = []
        sz: List[Polygon] = []
        dz: List[EnvObj] = []

        for obj in map.objects:
            # Classifies objects
            # NOTE: This depends of the current implementation for the object types
            obj: EnvObj
            try:
                is_obs = obj.isObstacle
                if is_obs:
                    obs.append(Polygon(obj.getRoundingBox()))
            except:
                pass
            if isinstance(obj, Door):
                cull.append(Polygon(obj.getRoundingBox()))
            try:
                is_sz = obj.isSafeZone
                if is_sz:
                    sz.append(Polygon(obj.getRoundingBox()))
            except:
                pass
            try:
                _ = obj.damageFactor
                dz.append(obj)
            except:
                pass
            self.danger_zones = dz
            self.safe_zones = sz

        # Generate all maps
        b_x = [.0]*2+[self.map_blueprint.width]*2
        b_y = [.0]+[self.map_blueprint.height]*2+[.0]

        base = MultiPolygon([Polygon(zip(b_x, b_y))])
        self.obstacle_map = base
        # Cut the obstacles
        for ob in obs:
            self.obstacle_map = self.obstacle_map.difference(
                Polygon(ob.getRoundingBox())
            )

        # Paste the doors
        for d in cull:
            self.obstacle_map = self.obstacle_map.union(
                Polygon(d.getRoundingBox())
            )

        # Fit the place
        self.obstacle_map = self.obstacle_map.intersection(base)

        # Put some safety distance
        map = map.buffer(-.01, cap_style='flat', join_style='bevel')

        self.safe_zone_map: MultiPolygon = reduce(
            lambda x, y: x.union(y),  # union
            [Polygon(obj.getRoundingBox()) for obj in sz]  # of all safe zones
        )

        self.danger_zone_map: MultiPolygon = reduce(
            lambda x, y: x.union(y),  # union
            [Polygon(obj.getRoundingBox()) for obj in dz]  # of all danger zones
        )

    def setup_navmesh(self):
        del self.navmesh
        self.agents.clear()
        self.routes.clear()

        self.navmesh = build_navmesh(
            self.obstacle_map, params.NAVEGABLE_MINIMUM_DISTANCE)

    def setup_pdestrians(self, pedestrians: int = 30, seed: int | None = None):
        self.agents.clear()
        self.routes.clear()

        rs = np.random.RandomState(seed)

        flat = self.navmesh.flat_polygon
        prepare(flat)

        width = self.map_blueprint.width
        height = self.map_blueprint.height

        # Independent pedestrians position has uniform distribution
        xs = rs.uniform(0, width, pedestrians)
        ys = rs.uniform(0, height, pedestrians)

        # Force it to be inside the navmesh
        for i, (x, y) in enumerate(zip(xs, ys)):
            while (not Point(x, y).within(flat)):
                x = rs.uniform(0, width)
                y = rs.uniform(0, height)
            xs[i] = x
            ys[i] = y

        # Assumed ages between 18 and 65. Distribution and parameters
        # from DOI:10.1111/j.1539-6924.2006.00856.x
        ms = rs.lognormal(79.96, 20.73, pedestrians)

        # Radius (distance from shoulder to shoulder) has uniform distribution
        rads = rs.uniform(.25, .35, pedestrians)

        self.agents = [
            Pedestrian(
                map=self.obstacle_map,
                map_boundary=self.obstacle_map.boundary,
                danger_zones=self.danger_zones,
                position=np.array(x, y),
                mass=m,
                radius=rad
            ) for x, y, m, rad in zip(xs, ys, ms, rads)
        ]

    def setup_routes(self, seed: int | None = None):
        self.routes.clear()

        rs = np.random.RandomState(seed)

        zone_to_go = rs.randint(0, len(self.safe_zones), len(self.agents))
        dests = [self.safe_zones[i].centroid for i in zone_to_go]

        for i, p in enumerate(self.agents):
            r, _ = a_star(self.navmesh, p.position_point, dests[i])

            self.routes.append(r[1:])

    def update(self):
        for i in range(len(self.agents)):
            a = self.agents[i]
            r = self.routes[i]

            # Update direction according to route and position
            self.routes[i], _ = clamp_route(
                self.navmesh, a.position_point, r)

            vector = np.array(r[0].xy)-a.position

            a.direction = vector/np.linalg.norm(vector)

            # Update model data
            a.update_velocity(self.agents)
            a.update_position()
