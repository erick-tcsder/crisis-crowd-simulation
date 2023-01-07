from functools import reduce
from typing import List

import numpy as np
from shapely import MultiPolygon, Point, Polygon, prepare

from .parameters import *

from .agents import Pedestrian, Status
from .environment.blueprint import Blueprint
from .environment.environment_objects import Door, EnvObj, DamageZone
from .navmesh import Navmesh, build_navmesh, a_star, clamp_route


class SimulationContext:
    map_blueprint: Blueprint
    agents: List[Pedestrian] = []

    obstacle_map: MultiPolygon  # Map is what is'nt obstacle
    safe_zone_map: MultiPolygon  # Map is what is safe zone
    danger_zone_map: MultiPolygon  # Map is what is danger zone

    danger_zones: List[DamageZone]
    safe_zones: List[Polygon]

    navmesh: Navmesh

    # Matrix with the zones in order of priority for every pedestrian (rows)
    zones_to_go: np.ndarray
    zone_choosed: np.ndarray  # Index of which zone is searching right now

    routes: List[List[Point]] = []
    ticks: int = 0

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
                ob
            )

        # Paste the doors
        for d in cull:
            self.obstacle_map = self.obstacle_map.union(
                d
            )

        # Fit the place
        self.obstacle_map = self.obstacle_map.intersection(base)

        # Put some safety distance
        self.obstacle_map = self.obstacle_map.buffer(
            -.01, cap_style='flat', join_style='bevel')
        if isinstance(self.obstacle_map, Polygon):
            self.obstacle_map = MultiPolygon([self.obstacle_map])

        self.safe_zone_map: MultiPolygon = reduce(
            lambda x, y: x.union(y),  # union
            sz  # of all safe zones
        )

        self.danger_zone_map: MultiPolygon = reduce(
            lambda x, y: x.union(y),  # union
            [Polygon(obj.getRoundingBox()) for obj in dz]  # of all danger zones
        )

    def setup_navmesh(self):
        self.agents.clear()
        self.routes.clear()
        print("Building navmesh...")
        self.navmesh = build_navmesh(
            self.obstacle_map, NAVEGABLE_MINIMUM_DISTANCE)

    def setup_pedestrians(self, pedestrians: int = 30, seed: int | None = None):
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
        median = np.log(79.96**2/np.sqrt(79.96**2+20.73**2))
        std = np.sqrt(np.log(1+(20.73**2)/(79.96**2)))
        ms = rs.lognormal(median, std, pedestrians)

        # Radius (distance from shoulder to shoulder) has uniform distribution
        rads = rs.uniform(.25, .35, pedestrians)

        r = rs.randint(10000, size=pedestrians)

        self.agents = [
            Pedestrian(
                map=self.obstacle_map,
                map_boundary=self.obstacle_map.boundary,
                danger_zones=self.danger_zones,
                position=np.array([x, y]),
                mass=m,
                radius=rad,
                position_point=Point(x, y),
                id=f'{i}'
            ) for x, y, m, rad, i in zip(xs, ys, ms, rads, r)
        ]

    def setup_routes(self, seed: int | None = None):
        self.routes.clear()

        rs = np.random.RandomState(seed)

        zs = np.concatenate(
            [rs.permutation(len(self.safe_zones))
             for _ in range(len(self.agents))])
        zs = zs.reshape((len(self.agents), -1))
        self.zones_to_go = zs
        self.zone_choosed = np.repeat(0, len(self.agents))

        dests = [zone.centroid for zone in self.safe_zones]

        i = 0
        while i < len(self.agents):
            p = self.agents[i]
            choosed_index = self.zone_choosed[i]
            if choosed_index >= len(self.safe_zones):
                p.status = Status.DEAD
                continue

            r, l = a_star(self.navmesh, p.position_point, dests[
                self.zones_to_go[i, choosed_index]
            ])

            if l == -1:
                self.zone_choosed[i] += 1
                i -= 1
                continue

            self.routes.append(r[1:])
            i += 1

    def update(self):
        self.update_routes()
        for a in self.agents:
            # Update model data
            a.update_velocity(self.agents)
            a.update_position()

        self.ticks += 1
        self.update_safes()
        self.update_danger()
        return all((a.status != Status.ALIVE for a in self.agents))

    def update_safes(self):
        for i in range(len(self.agents)):
            if self.agents[i].status != Status.SAFE and\
                    self.agents[i].position_point.within(self.safe_zone_map) and\
                    np.random.rand() < .05:
                self.agents[i].status = Status.SAFE

    def update_danger(self):
        for d in self.danger_zones:
            d.damageFactor = 1/(self.time+1)

    def update_routes(self):
        for i in range(len(self.agents)):
            a = self.agents[i]
            r = self.routes[i]

            if len(r) == 0:
                continue

            # Update direction according to route and position
            r, good = clamp_route(
                self.navmesh, a.position_point, r)

            if not good:
                r, c = a_star(self.navmesh, a.position_point, r[-1])
                r = r[1:]
                self.routes[i] = r

                if c == -1:
                    a.status = Status.DEAD

            vector = np.array([r[0].x, r[0].y])-a.position

            a.direction = vector/np.linalg.norm(vector)

    @property
    def time(self) -> float:
        return self.ticks*TIME_STEP
