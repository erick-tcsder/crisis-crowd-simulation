from dataclasses import dataclass
from typing import List
from typing_extensions import Self
import numpy as np
from shapely import Point, MultiPolygon, LineString, shortest_line, prepare, MultiLineString
from numpy.linalg import norm
import simulation.parameters as params


@dataclass(kw_only=True, slots=True)
class Pedestrian:
    map: MultiPolygon
    map_boundary: MultiLineString
    position: np.ndarray
    mass: float = params.PEDESTRIAN_MASS
    radius: float = params.PEDESTRIAN_RADIUS
    direction: np.ndarray = np.array([.0, .0])

    velocity = np.array([.0, .0])

    def repulsion_force(self, pedestrians: List[Self]):
        fij = np.zeros_like(self.p)
        p = Point(*self.position)

        prepare(p)

        # Add the force of interactions with the other pedestrians.
        for ped in pedestrians:
            if ped == self:
                continue

            # line = LineString([Point(*ped.p), Point(*self.p)])
            line = [
                np.array(Point(*p).xy)
                for p in LineString([Point(*ped.position), p]).coords]
            dif = np.fromiter((norm(x) for x in (line[1]-line[0])), dtype=float)

            j = self.radius + ped.radius

            fij += self.calculate_forces(dif, j)

        # Return the total force between pedestrian and others.
        return fij

    # Calculates the distance of a pedestrian to a wall.
    def wall_difference(self):
        p = self.position    # pedestrian position

        vp = list(shortest_line(self.map_boundary, Point(*p)).coords)
        vp = [np.array(Point(*p).xy) for p in vp]

        r = np.fromiter((norm(x) for x in (vp[1]-vp[0])), dtype=float)
        if Point(*p).within(self.map):
            return r*-1

    # Function to calculate the repulsion force with respect to the walls.
    def wall_force(self) -> float:
        # Initialize acceleration.
        fiW = np.zeros_like(self.p)

        # Add the force of interactions with the walls.
        dif = self.wall_difference()  # difference vector

        j = self.radius

        fiW += self.calculate_forces(dif, j)

        # Return the total force between pedestrian and walls.
        return fiW

    def calculate_forces(self, dif: np.ndarray, j: float) -> float:
        diW = norm(dif)
        r = self.radius                            # pedestrian radius
        niW = dif / diW                            # normalized difference vector

        f_repulsive = params.A_CONSTANT * np.exp(
            (r - diW) / params.B_CONSTANT) * niW

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
        e0 /= norm(e0)
        # We calculate the force of repulsion of this pedestrian with the others.
        fij = self.repulsion_force(pedestrians)
        # We calculate the repulsive force of this pedestrian with the walls.
        fiW = self.wall_force()

        # We calculate the pedestrians aceleration
        acc = (params.STANDARD_VELOCITY * self.direction -
               self.velocity) / params.TIME_STEP + (fij + fiW) / self.mass
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
