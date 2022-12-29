import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from shapely.geometry import Point, Polygon
from numpy.linalg import norm


# Class for pedestrian
class Pedestrian:
    def __init__(self, p: np.array, m: float, t: float, A: float, B: float, j: float, s: float, r: float,
                 k: float, K: float, v0: float, boundary_min: np.array, boundary_max: np.array):
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
        self.boundary_min = boundary_min    # lower limit of the space in which the pedestrian moves
        self.boundary_max = boundary_max    # upper limit of the space in which the pedestrian moves

        self.s = s
    # Función para calcular la fuerza de repulsión respecto al resto de peatones.
    def repulsion_force(self, pedestrians: ['Pedestrian']):
        # Initialize acceleration.
        fij = np.zeros_like(self.p)

        # Add the force of interactions with other pedestrians.
        for pedestrian in pedestrians:
            # Ignore this pedestrian (it doesn't make sense to consider self-interactions).
            if pedestrian == self:
                continue

            # Calculate the distance from this pedestrian to the other.
            dif = pedestrian.p - self.p                # difference vector
            dij = norm(dif)                            # norm of difference vector (distance)

            # If the pedestrian is too close to the wall.
            if dij < self.j:
                nij = dif / dij                            # normalized difference vector
                rij = self.r + pedestrian.r                # sum of the radii of both pedestrians
                tij = np.flip(nij)                         # tangential direction
                tij[0] = -tij[0]
                dv = np.cross(pedestrian.v - self.v, tij)  # tangential velocity difference

                # Repulsion force between pedestrians
                f_repulsive = self.A * np.exp((rij - dij) / self.B) * nij

                # Body force between pedestrians.
                f_body = (self.k * (rij - dij) if dij > rij else 0) * nij

                f_friction = (self.K * (rij - dij) * dv if dij > rij else 0) * tij

                # Sum all forces to calculate the total force.
                fij += f_repulsive + f_body + f_friction

        # Return the total repulsion force between pedestrians.
        return fij

    # Calculates the distance of a pedestrian to a wall.
    def wall_difference(self, wall: 'Wall'):
        p = self.p    # pedestrian position
        p1 = wall.start  # wall start coordinate
        p2 = wall.end  # wall end coordinate

        # Check that the point does not correspond to the ends of the segment.
        if all(p1 == p) or all(p2 == p):
            return np.zeros_like(p)

        # Calculate the angle between AB and AP, if it is greater than 90 degrees return the distance between p1 and p
        elif np.arccos(np.dot((p - p1) / norm(p - p1), (p2 - p1) / norm(p2 - p1))) > np.pi / 2:
            return p - p1

        # Calculate the angle between AB and BP, if it is greater than 90 degrees return the distance between p2 and p.
        elif np.arccos(np.dot((p - p2) / norm(p - p2), (p1 - p2) / norm(p1 - p2))) > np.pi / 2:
            return p - p2

        p_o = norm(np.cross(p2 - p1, p1 - p)) / norm(p2 - p1)  # Calculate the length of the hypotenuse.
        p_p1 = norm(p - p1)                                    # Calculate the length of the first leg.
        p1_o = np.sqrt(p_p1**2 - p_o**2)                       # Calculate the length of the second leg.

        # Determine the point o by explicitly calculating the orthogonal vector.
        o = p1 + (p2 - p1) / norm(p2 - p1) * p1_o
        
        # Return the orthogonal vector.
        return p - o

    #Function to calculate the repulsion force with respect to the walls.
    def wall_force(self, walls: ['Wall']):
        # Initialize acceleration.
        fiW = np.zeros_like(self.p)

        # Add the force of interactions with the walls.
        for wall in walls:
            # Calculate the distance from this pedestrian to the wall.
            dif = self.wall_difference(wall)           # difference vector
            diW = norm(dif)                            # norm of difference vector (distance)

            # If the pedestrian is too close to the wall.
            if diW < self.j:
                niW = dif / diW             # normalized difference vector
                r = self.r                  # pedestrian radius
                tiW = np.flip(niW)          # tangential direction
                tiW[0] = -tiW[0]
                dv = np.cross(self.v, tiW)  # tangential velocity

                # Repulsion force between pedestrian and wall
                f_repulsive = self.A * np.exp((r - diW) / self.B) * niW

                # Body force that the pedestrian exerts on the wall.
                f_body = (self.k * (r - diW) if diW > r else 0) * niW

                # Friction force between pedestrian and wall.
                f_friction = (self.K * (r - diW) * dv if diW > r else 0) * tiW

                # Sum all forces to calculate the total force.
                fiW += f_repulsive + f_body + f_friction

        # Return the total repulsion force between pedestrian and walls.
        return fiW


    # Function to update the pedestrian speed.
    def update_velocity(self, dt: float,e0: np.array, pedestrians: ['Pedestrian'], walls: ['Wall']):
        fij = self.repulsion_force(pedestrians)  # We calculate the force of repulsion of this pedestrian with the others.
        fiW = self.wall_force(walls)             # We calculate the repulsive force of this pedestrian with the walls.

        # We calculate the pedestrians aceleration
        acc = (self.v0 * e0 - self.v) / self.t + (fij + fiW) / self.m
        # Update
        self.v += acc * dt

        # Limit velocity to desired velocity
        v_norm = norm(self.v)
        if v_norm > self.v0:
            self.v *= self.v0 / v_norm

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

class Wall:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def draw(self):
        plt.plot([self.start[0], self.end[0]], [self.start[1], self.end[1]], 'k', lw=2)


class Exit:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def draw(self):
        plt.plot([self.start[0], self.end[0]], [self.start[1], self.end[1]], 'r', lw=2)



# Set up parameters of simulation
dt = 1 # Tiempo transcurrido entre pasos de la simulación
n_steps = 300

# Set number of pedestrians
n_pedestrians = 10

# Set up boundaries of simulation
boundary_min = np.array([0, 0])
boundary_max = np.array([100, 100])

# Set up mass of pedestrians
m = 80
# Set up desired velocity of pedestrians
v0 = 5
# Set up parameters of interaction forces
t = 0.5
# Repulsion force
A = 2*10e3
# Repulsion distance
B = 0.08
# Repulsion constants
k = 1.2*10e5
K = 2.4*10e5
# Radios of pedestrians.
r = 0.5
# Set up minimum distance between pedestrians
j = 1
# Set up maximum attraction distance between pedestrian and exits
s = 100

# Set up initial positions and velocities of pedestrians
pedestrians = []
for i in range(n_pedestrians):
    p = np.random.uniform(boundary_min, boundary_max, size=2)
    v = np.zeros(2)
    pedestrians.append(Pedestrian(p, m, t, A, B, j, s, r, k, K, v0, boundary_min, boundary_max))

# Set up walls
walls = []  # Rectangulos interiores

start = np.array([0, 0])
end = np.array([100, 0])
walls.append(Wall(start, end))

start = np.array([100, 0])
end = np.array([100, 100])
walls.append(Wall(start, end))

start = np.array([100, 100])
end = np.array([0, 100])
walls.append(Wall(start, end))

start = np.array([0, 100])
end = np.array([0, 0])
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
        pedestrian.update_velocity(dt, exit.end - pedestrian.p, pedestrians, walls)
        pedestrian.update_position()
    # Update scatter plots for pedestrians
    for i, pedestrian in enumerate(pedestrians):
        scatters[i].set_offsets(pedestrian.p)


# Set up animation
anim = animation.FuncAnimation(fig, animate, frames=range(n_steps), interval=200)

# Show plot
plt.show()
