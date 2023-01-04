from dataclasses import dataclass
from typing import List
from typing_extensions import Self
import numpy as np
from shapely import Point, MultiPolygon, LineString, shortest_line, prepare, MultiLineString, Polygon
from numpy.linalg import norm
from ..environment.environment_objects import EnvObj
import simulation.parameters as params


@dataclass(kw_only=True, slots=True, eq=False, repr=False)
class Pedestrian:
    map: MultiPolygon
    map_boundary: MultiLineString
    danger_zones: List[EnvObj]
    position: np.ndarray
    position_point: Point
    mass: float = params.PEDESTRIAN_MASS
    radius: float = params.PEDESTRIAN_RADIUS
    direction: np.ndarray = np.array([.0, .0])
    id: int

    velocity: np.ndarray = np.array([.0, .0])

    def __repr__(self) -> str:
        return f'Pedestrian {self.id} [{self.position[0]:.2f} x {self.position[1]:.2f}]'

    def repulsion_force(self, pedestrians: List[Self]):
        fij = np.zeros_like(self.position)

        # Add the force of interactions with the other pedestrians.
        for ped in pedestrians:
            if ped == self:
                continue

            dif = self.position-ped.position

            j = self.radius + ped.radius

            fij += self.calculate_forces(dif, j)

        # Return the total force between pedestrian and others.
        return fij

    # Calculates the distance of a pedestrian to a wall.
    def wall_difference(self, geo=None, geo_boundary=None):
        if geo is None:
            geo = self.map
        if geo_boundary is None:
            geo_boundary = self.map_boundary
        p = self.position    # pedestrian position

        vp = list(shortest_line(geo_boundary, self.position_point).coords)
        vp = [np.array([Point(p).x, Point(p).y]) for p in vp]

        r = np.fromiter((norm(x) for x in (vp[1]-vp[0])), dtype=float)

        if self.position_point.within(geo):
            return r*-1

        return r

    # Function to calculate the repulsion force with respect to the walls.
    def wall_force(self) -> float:
        # Initialize acceleration.
        fiW = np.zeros_like(self.position)

        # Add the force of interactions with the walls.
        dif = self.wall_difference()  # difference vector

        j = self.radius

        fiW += self.calculate_forces(dif, j)

        # Return the total force between pedestrian and walls.
        return fiW

    # Function to calculate the repulsion force with respect to the danger zones.
    def danger_force(self) -> float:
        # Initialize acceleration.
        fiF = np.zeros_like(self.position)

        for zone in self.danger_zones:
            geo = Polygon(zone.getRoundingBox())
            # Add the force of interactions with the zone.
            dif = self.wall_difference(
                geo, geo.boundary
            )  # difference vector

            j = self.radius

            fiF += self.calculate_forces(
                dif, j, zone.damageFactor*params.DANGER_MULTIPLIER, params.DANGER_DISTANCE_RATIO)

        # Return the total force between pedestrian and walls.
        return fiF

    def calculate_forces(self, dif: np.ndarray, j: float,
                         a: float = params.A_CONSTANT,
                         b: float = params.B_CONSTANT) -> float:
        diW = norm(dif)
        r = self.radius                            # pedestrian radius
        niW = dif / diW                            # normalized difference vector

        f_repulsive = a * np.exp(
            (r - diW) / b) * niW

        f_total = f_repulsive

        # If the pedestrian is too close to the wall.
        if diW < j:
            # tiW = np.flip(niW).copy()          # tangential direction
            # tiW[0] = -tiW[0]
            # dv = np.dot(self.v, tiW)           # tangential velocity

            # Body force that the pedestrian exerts on the wall.
            f_body = (params.K1_CONSTANT * (r - diW)) * niW

            # Friction force between pedestrian and wall.
            # f_friction = (self.K * (r - diW) * dv) * tiW
            f_friction = 0

            # Sum all forces to calculate the total force.
            f_total += f_body + f_friction

        return f_total

    # Function to update the pedestrian speed.
    def update_velocity(self,
                        pedestrians: List[Self]):
        # e0 /= norm(e0)
        # We calculate the force of repulsion of this pedestrian with the others.
        fij = self.repulsion_force(pedestrians)
        # We calculate the repulsive force of this pedestrian with the walls.
        fiW = self.wall_force()

        fiF = self.danger_force()

        # We calculate the pedestrians aceleration
        acc = (params.STANDARD_VELOCITY * self.direction -
               self.velocity) / params.TIME_STEP + (fij + fiW + fiF) / self.mass
        # Update
        self.velocity += acc * params.TIME_STEP

        # Limit velocity to desired velocity
        v_norm = norm(self.velocity)
        if v_norm > params.MAXIMUM_VELOCITY:
            self.velocity *= params.MAXIMUM_VELOCITY / v_norm

    # Function to update pedestrian speed
    def update_position(self):
        # Updates the position with respect to speed and elapsed time (p = v * t)
        self.position += self.velocity * params.TIME_STEP
        self.position_point = Point(*self.position)

    def toJson(self):
        return {
            'id': self.id,
            'top': self.position[1],
            'left': self.position[0],
            'width': self.radius*2,
            'status': 'ALIVE'
        }