from typing import List
from typing_extensions import Self
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from shapely import Point, Polygon, LineString, shortest_line
from numpy.linalg import norm


class Wall:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def draw(self):
        plt.plot([self.start[0], self.end[0]], [
                 self.start[1], self.end[1]], color='k', lw=2)


class Exit:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def draw(self):
        plt.plot([self.start[0], self.end[0]], [
                 self.start[1], self.end[1]], color='r', lw=2)


# Class for pedestrian
class Pedestrian:
    def __init__(
            self, p: np.array, m: float, t: float, A: float, B: float, j: float,
            s: float, r: float, k: float, K: float, v0: float,
            boundary_min: np.array, boundary_max: np.array):
        self.p = p                      # position
        self.m = m                      # mass
        self.v = np.zeros_like(p)       # velocity
        self.t = t                      # update time
        self.A = A                      # intensity of repulsive force between pedestrians
        self.B = B                      # change factor of repulsive force with respect to distance
        self.j = j                      # minimum distance that the pedestrian must maintain with respect to others
        self.r = r                      # pedestrian radius
        self.k = k                      # body force constant
        self.K = K                      # friction constant

        self.v0 = v0             # desired speed
        # lower limit of the space in which the pedestrian moves
        self.boundary_min = boundary_min
        # upper limit of the space in which the pedestrian moves
        self.boundary_max = boundary_max

        self.s = s
    # Función para calcular la fuerza de repulsión respecto al resto de peatones.

    def repulsion_force(self, pedestrians: List[Self]):
        fij = np.zeros_like(self.p)

        # Add the force of interactions with the walls.
        for ped in pedestrians:
            if ped == self:
                continue

            # line = LineString([Point(*ped.p), Point(*self.p)])
            line = [
                np.array(Point(*p).xy)
                for p in LineString([Point(*ped.p),
                                     Point(*self.p)]).coords]
            dif = np.fromiter((norm(x) for x in (line[1]-line[0])), dtype=float)

            j = self.r + ped.r

            fij += self.calculate_forces(dif, j)

        # Return the total force between pedestrian and walls.
        return fij

    # Calculates the distance of a pedestrian to a wall.
    def wall_difference(self, wall: Wall):
        p = self.p    # pedestrian position
        p1 = wall.start  # wall start coordinate
        p2 = wall.end  # wall end coordinate

        line = LineString(
            [Point(*p1), Point(*p2)])

        vp = list(shortest_line(line, Point(*p)).coords)
        vp = [np.array(Point(*p).xy) for p in vp]

        return np.fromiter((norm(x) for x in (vp[1]-vp[0])), dtype=float)

    # Function to calculate the repulsion force with respect to the walls.
    def wall_force(self, walls: List[Wall]) -> float:
        # Initialize acceleration.
        fiW = np.zeros_like(self.p)

        # Add the force of interactions with the walls.
        for wall in walls:
            # Calculate the distance from this pedestrian to the wall.
            dif = self.wall_difference(wall)           # difference vector

            j = r

            fiW += self.calculate_forces(dif, j)

        # Return the total force between pedestrian and walls.
        return fiW

    def calculate_forces(self, dif: np.ndarray, j: float) -> float:
        diW = norm(dif)
        r = self.r                                 # pedestrian radius
        niW = dif / diW                            # normalized difference vector

        f_repulsive = self.A * np.exp((r - diW) / self.B) * niW

        f_total = f_repulsive

        # If the pedestrian is too close to the wall.
        if diW < j:
            tiW = np.flip(niW).copy()          # tangential direction
            tiW[0] = -tiW[0]
            dv = np.dot(self.v, tiW)           # tangential velocity

            # Body force that the pedestrian exerts on the wall.
            f_body = (self.k * (r - diW)) * niW

            # Friction force between pedestrian and wall.
            # f_friction = (self.K * (r - diW) * dv) * tiW
            f_friction = 0

            # Sum all forces to calculate the total force.
            f_total += f_body + f_friction

        return f_total

    # Function to update the pedestrian speed.
    def update_velocity(self, dt: float, e0: np.array,
                        pedestrians: List[Self],
                        walls: List[Wall]):
        e0 /= norm(e0)
        # We calculate the force of repulsion of this pedestrian with the others.
        fij = self.repulsion_force(pedestrians)
        # We calculate the repulsive force of this pedestrian with the walls.
        fiW = self.wall_force(walls)

        # We calculate the pedestrians aceleration
        acc = (self.v0 * e0 - self.v) / self.t + (fij + fiW) / self.m
        # Update
        self.v += acc * t

        # Limit velocity to desired velocity
        v_norm = norm(self.v)
        if v_norm > 8:
            self.v *= 8 / v_norm

    # Function to update pedestrian speed
    def update_position(self):
        # Updates the position with respect to speed and elapsed time (p = v * t)
        self.p += self.v * t

        # Verifica si el peatón se ha pasado de los bordes
        for i in range(2):
            if self.p[i] < self.boundary_min[i]:
                self.p[i] = self.boundary_min[i]
                self.v[i] = -self.v[i]
            elif self.p[i] > self.boundary_max[i]:
                self.p[i] = self.boundary_max[i]
                self.v[i] = -self.v[i]


# Set up parameters of simulation
dt = 1  # Tiempo transcurrido entre pasos de la simulación
n_steps = 300

# Set number of pedestrians
n_pedestrians = 20

# Set up boundaries of simulation
boundary_min = np.array([0, 0])
boundary_max = np.array([100, 100])

# Set up mass of pedestrians
m = 80
# Set up desired velocity of pedestrians
v0 = 3
# Set up parameters of interaction forces
t = 0.125
# Repulsion force
A = 2e3
# Repulsion distance
B = 0.08
# Repulsion constants
k = 1.2e5
K = 2.4e5
# Radios of pedestrians.
r = 0.5
# Set up minimum distance between pedestrians
j = .5
# Set up maximum attraction distance between pedestrian and exits
s = 100

# Set up initial positions and velocities of pedestrians
pedestrians = []
for i in range(n_pedestrians):
    p = np.random.uniform([0, 50], boundary_max, size=2)
    v = np.zeros(2)
    pedestrians.append(
        Pedestrian(
            p, m, t, A, B, j, s, r, k, K, v0, boundary_min,
            boundary_max))

# Set up walls
walls = []  # Rectangulos interiores

start = np.array([0, 50])
end = np.array([100, 50])
walls.append(Wall(start, end))

# Set up exits
exits = []

start = np.array([10, 10])
end = np.array([20, 10])
exits.append(Exit(start, end))

# Set up figure and axes
fig, ax = plt.subplots()

# Set up limits of axes
ax.set_xlim((boundary_min[0], boundary_max[0]))
ax.set_ylim((boundary_min[1], boundary_max[1]))

# Initialize list of scatter plots for pedestrians
scatters = []
for pedestrian in pedestrians:
    scatters.append(ax.scatter([pedestrian.p[0]], [pedestrian.p[1]], color='k'))

# Set up plots for walls and exits
for wall in walls:
    wall.draw()
for exit in exits:
    exit.draw()


# Set up animation function
def animate(i):
    # Update positions and velocities of pedestrians
    for pedestrian in pedestrians:
        pedestrian.update_velocity(
            dt, exit.end - pedestrian.p, pedestrians, walls)
        pedestrian.update_position()
    # Update scatter plots for pedestrians
    for i, pedestrian in enumerate(pedestrians):
        scatters[i].set_offsets(pedestrian.p)


# Set up animation
anim = animation.FuncAnimation(
    fig, animate, frames=range(n_steps),
    interval=125)

# Show plot
plt.show()
