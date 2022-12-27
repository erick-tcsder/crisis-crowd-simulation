import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from shapely.geometry import Point, Polygon
from numpy.linalg import norm


# Class for pedestrian
class Pedestrian:
    def __init__(self, p: np.array, m: float, t: float, A: float, B: float, j: float, r: float,
                 k: float, K: float, v_desired: float, boundary_min: np.array, boundary_max: np.array):
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

        self.v_desired = v_desired          # desired speed
        self.boundary_min = boundary_min    # lower limit of the space in which the pedestrian moves
        self.boundary_max = boundary_max    # upper limit of the space in which the pedestrian moves

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
        p1 = wall.p1  # wall start coordinate
        p2 = wall.p2  # wall end coordinate

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
    def update_velocity(self, dt: float, pedestrians: ['Pedestrian'], walls: ['Wall'], exits: ['Exit']):
        fij = self.repulsion_force(pedestrians)  # We calculate the force of repulsion of this pedestrian with the others.
        fiW = self.wall_force(walls)             # We calculate the repulsive force of this pedestrian with the walls.

        # Add forces from interactions with exits
        found_exit = False
        for exit in exits:
            # Calculate attraction force towards exit
            r_exit = exit.p
            dif = r_exit - self.p
            dij = np.linalg.norm(dif)
            if dij < self.t:
                # Attraction force decreases as distance to exit decreases
                f_attraction = self.A * np.exp(-dij / self.B) * dif / dij
                found_exit = True
            else:
                f_attraction = np.zeros_like(dif)

            # Add attraction force to total force
            fij += f_attraction

        # If no exit was found, add A random force to the velocity
        if not found_exit:
            fij += np.random.uniform(-1, 1, size=2)

        # Update velocity according to acceleration equation
        self.v += (fij / self.m - self.v / self.t) * dt

        # Limit velocity to desired velocity
        v_norm = np.linalg.norm(self.v)
        if v_norm > self.v_desired:
            self.v *= self.v_desired / v_norm

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


# def distance_to_wall(pedestrian, wall):
#     # Create A Shapely Point object from pedestrian position
#     point = Point(pedestrian.p)
#     # Create A Shapely Polygon object from wall vertices
#     polygon = Polygon(wall.vertices)
#     # Calculate minimum distance between point and polygon
#     distance = point.distance(polygon)
#     return distance

class Wall:
    def __init__(self, vertices):
        self.vertices = vertices
        # Compute center of mass of wall
        self.p = np.mean(vertices, axis=0)
        self.p1 = np.array([1, 2])
        self.p2 = np.array([3, 4])

    def draw(self):
        plt.plot(self.vertices[:, 0], self.vertices[:, 1], 'k', lw=2)


class Exit:
    def __init__(self, vertices):
        self.vertices = vertices
        # Compute center of mass of wall
        self.p = np.mean(vertices, axis=0)

    def draw(self):
        plt.plot(self.vertices[:, 0], self.vertices[:, 1], 'r', lw=2)


# Set up parameters of simulation
dt = 1 # Tiempo transcurrido entre pasos de la simulación
n_steps = 300

# Set number of pedestrians
n_pedestrians = 100

# Set up boundaries of simulation
boundary_min = np.array([0, 0])
boundary_max = np.array([10, 10])

# Set up mass of pedestrians
m = 80

# Set up parameters of interaction forces
t = 1
A = 1
B = 0.5
k = 1
K = 1
r = 0.5

# Set up desired velocity of pedestrians
v_desired = 5

# Set up minimum distance between pedestrians
j = 0.5

# Set up initial positions and velocities of pedestrians
pedestrians = []
for i in range(n_pedestrians):
    p = np.random.uniform(boundary_min, boundary_max, size=2)
    v = np.zeros(2)
    pedestrians.append(Pedestrian(p, m, t, A, B, j, r, k, K, v_desired, boundary_min, boundary_max))

# Set up walls
walls = [] # Rectangulos interiores
vertices = np.array([[0, 0], [10, 0], [10, 10], [0, 10]]) # Vertices del rectangulo
walls.append(Wall(vertices))

# Set up exits
exits = []
vertices = np.array([[5.5, 0], [10, 0], [10, 0.5]])
exits.append(Exit(vertices))

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
lines_walls = []
for wall in walls:
    lines_walls.append(ax.plot(wall.vertices[:, 0], wall.vertices[:, 1], color='k'))
lines_exits = []
for exit in exits:
    lines_exits.append(ax.plot(exit.vertices[:, 0], exit.vertices[:, 1], color='r'))


# Set up animation function
def animate(i):
    # Update positions and velocities of pedestrians
    for pedestrian in pedestrians:
        pedestrian.update_velocity(dt, pedestrians, walls, exits)
        pedestrian.update_position()
    # Update scatter plots for pedestrians
    for i, pedestrian in enumerate(pedestrians):
        scatters[i].set_offsets(pedestrian.p)


# Set up animation
anim = animation.FuncAnimation(fig, animate, frames=range(n_steps), interval=200)

# Show plot
plt.show()

# anim.save('animation.mp4')
# anim.show()
