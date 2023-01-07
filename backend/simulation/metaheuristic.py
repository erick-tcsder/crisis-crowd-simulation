from typing import List

import numpy as np
from shapely import LineString, Point, distance, prepare

import parameters as params
from context import SimulationContext
from environment.blueprint import Blueprint
from environment.environment_objects import DamageZone
from genetic import *


def vulnerability_data(map: Blueprint, damage_radius: float):
    map.objects = [obj for obj in map.objects if not isDamage(obj)]

    def isDamage(obj):
        try:
            _ = obj.damageFactor
            return True
        except:
            return False

    def test_position(p: Point) -> float:
        # Points to create the sphere
        p1 = np.array([p.x*map.width, p.y*map.height])  # center
        # point at distance equals to the radius from the center
        p2 = damage_radius*(np.array([(map.width/2), (map.height/2)])-p1)

        # Put the bomb
        map.objects.append(DamageZone(
            [tuple(p1), tuple(p2)],
            0.9
        ))

        # Population of the simulation
        pop = np.random.randint(params.VULNERABILITY_POP_MIN,
                                params.VULNERABILITY_POP_MAX+1)

        # start simulation
        sim_context = SimulationContext(map)

        # Do setup without actually run simulation
        sim_context.setup_navmesh()
        sim_context.setup_pedestrians(pop)
        sim_context.setup_routes()

        # Create a line string from the route of the pedestrians
        strings = [LineString(path) if len(
            path) != 0 else None for path in sim_context.routes]

        dmg_zone = sim_context.danger_zone_map
        prepare(dmg_zone)

        # Calculate the distance from the bomb (approx) to each route.
        # Distance is 0 if the pedestrians even had a chance to move.
        d = np.fromiter((0
                         if line is None else distance(dmg_zone, line)
                         for line in strings),
                        dtype=float)

        # Before return clean the bombs in the map
        map.objects = [obj for obj in map.objects if not isDamage(obj)]

        # Return the median of the distance
        return d.mean()

    gen_engine = GeneticPoints(
        fit_func=test_position,
        mutation_maximum=15,
        inmutate_maximum=7,
        minimize=True
    )

    first_gen = [Point(np.random.rand(), np.random.rand())]

    new_gen = gen_engine.next_gen(first_gen)
    while True:
        limit = min(len(new_gen), 10)
        yield (gen_engine.generation, [(c.value.x*map.width, c.value.y*map.height) for c in new_gen[:limit]])
