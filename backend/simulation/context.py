from functools import reduce
from typing import List

import numpy as np
from shapely import MultiPolygon, Point, Polygon, prepare

import parameters as params

from .agents import Pedestrian
from .environment.blueprint import Blueprint
from .environment.enviroment_objects import Door, EnvObj
from .navmesh import Navmesh, build_navmesh


class SimulationContext:
    map_blueprint: Blueprint
    agents: List[Pedestrian]

    obstacle_map: MultiPolygon  # Map is what is'nt obstacle
    safe_zone_map: MultiPolygon  # Map is what is safe zone
    danger_zone_map: MultiPolygon  # Map is what is danger zone

    navmesh: Navmesh
    routes: List[List[Point]]

    def __init__(self, map: Blueprint) -> None:
        self.map_blueprint = map

        obs: List[EnvObj] = []
        cull: List[EnvObj] = []
        sz: List[EnvObj] = []
        dz: List[EnvObj] = []

        for obj in map.objects:
            # Classifies objects
            # NOTE: This depends of the current implementation for the object types
            obj: EnvObj
            try:
                is_obs = obj.isObstacle
                if is_obs:
                    obs.append(obj)
            except:
                pass
            if isinstance(obj, Door):
                cull.append()
            try:
                is_sz = obj.isSafeZone
                if is_sz:
                    sz.append(obj)
            except:
                pass
            try:
                _ = obj.damageFactor
                dz.append(obj)
            except:
                pass

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
        self.navmesh = build_navmesh(
            self.obstacle_map, params.NAVEGABLE_MINIMUM_DISTANCE)

    def setup_pdestrians(self, pedestrians: int = 30, seed: int | None = None):
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

        # Generate mass of pedestrians
        # TODO: Use random variable
        ms = np.repeat(params.PEDESTRIAN_MASS, pedestrians)

        # Radius (distance from shoulder to shoulder) has uniform distribution
        rads = rs.uniform(.25, .35)

        # TODO: Create Pedestrian objects
