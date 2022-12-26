import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from shapely.geometry import Point, Polygon

# Class for pedestrian
class Pedestrian:
    def __init__(self, r, m, T, A, B, v_desired, boundary_min, boundary_max, min_distance,k):
        self.r = r #postition
        self.m = m #masa
        self.T = T #time
        self.A = A #intensidad de la fuerza repulsiva entre los peatones
        self.B = B #como la fuerza cambia en la distancia
        self.v_desired = v_desired #velocidty
        self.boundary_min = boundary_min #el límite inferior del espacio en el que se mueve el peatón.
        self.boundary_max = boundary_max #el límite superior del espacio en el que se mueve el peatón.
        self.min_distance = min_distance #la distancia mínima que el peatón debe mantener con respecto a otros peatones.
        self.v = np.zeros_like(r) #velocidad actual del peaton
        self.k = k #constante relacionada con la simulacion de matplotlib   
    
    def update_velocity(self, dt, pedestrians, walls, exits):
        # Initialize force
        f = np.zeros_like(self.r)

        # Add forces from interactions with other pedestrians
        for pedestrian in pedestrians:
            if pedestrian == self:
                continue

            # Calculate distance to other pedestrian
            r_diff = pedestrian.r - self.r
            r_norm = np.linalg.norm(r_diff)
            if r_norm < self.min_distance:
                # Repulsive force between pedestrians
                f_repulsive = self.A * np.exp((self.min_distance - r_norm) / self.B) * r_diff / r_norm
                # Add sliding friction force
                f_friction = -self.k * (r_norm - self.min_distance) * np.cross(self.v - pedestrian.v, r_diff) / r_norm
            else:
                f_repulsive = np.zeros_like(r_diff)
                f_friction = np.zeros_like(r_diff)

            # Add repulsive and friction forces to total force
            f += f_repulsive + f_friction

        # Add forces from interactions with walls
        for wall in walls:
            # Compute distance to wall
            distance = distance_to_wall(self, wall)
            if distance < self.T:
            # Repulsive force between pedestrian and wall
                if distance == 0:
                        # Asignar un valor distinto a f_repulsive
                    f_repulsive = np.zeros_like(self.r)
                else:
                    f_repulsive = self.A * np.exp((self.T - distance) / self.B) * (self.r - wall.r) / distance
            else:
                f_repulsive = np.zeros_like(self.r)

        # Add forces from interactions with exits
        found_exit = False
        for exit in exits:
            # Calculate attraction force towards exit
            r_exit = exit.r
            r_diff = r_exit - self.r
            r_norm = np.linalg.norm(r_diff)
            if r_norm < self.T:
                # Attraction force decreases as distance to exit decreases
                f_attraction = self.A * np.exp(-r_norm / self.B) * r_diff / r_norm
                found_exit = True
            else:
                f_attraction = np.zeros_like(r_diff)

            # Add attraction force to total force
            f += f_attraction

        # If no exit was found, add a random force to the velocity
        if not found_exit:
            f += np.random.uniform(-1, 1, size=2)

        # Update velocity according to acceleration equation
        self.v += (f / self.m - self.v / self.T) * dt

        # Limit velocity to desired velocity
        v_norm = np.linalg.norm(self.v)
        if v_norm > self.v_desired:
            self.v *= self.v_desired / v_norm

def distance_to_wall(pedestrian, wall):
    # Create a Shapely Point object from pedestrian position
    point = Point(pedestrian.r)
    # Create a Shapely Polygon object from wall vertices
    polygon = Polygon(wall.vertices)
    # Calculate minimum distance between point and polygon
    distance = point.distance(polygon)
    return distance

# Function to update position of pedestrian
def update_position(pedestrian, dt):
            
    # Update position according to velocity
    pedestrian.r += pedestrian.v * dt

    # Check if pedestrian has crossed boundary
    for i in range(2):
        if pedestrian.r[i] < pedestrian.boundary_min[i]:
            pedestrian.r[i] = pedestrian.boundary_min[i]
            pedestrian.v[i] = -pedestrian.v[i]
        elif pedestrian.r[i] > pedestrian.boundary_max[i]:
            pedestrian.r[i] = pedestrian.boundary_max[i]
            pedestrian.v[i] = -pedestrian.v[i]

class Wall:
    def __init__(self, vertices):
        self.vertices = vertices
        # Compute center of mass of wall
        self.r = np.mean(vertices, axis=0)

    def draw(self):
        plt.plot(self.vertices[:, 0], self.vertices[:, 1], 'k', lw=2)

class Exit:
    def __init__(self, vertices):
        self.vertices = vertices
        # Compute center of mass of wall
        self.r = np.mean(vertices, axis=0)

    def draw(self):
        plt.plot(self.vertices[:, 0], self.vertices[:, 1], 'r', lw=2)


# Set up parameters of simulation
dt = 0.5
n_steps = 300

# Set number of pedestrians
n_pedestrians = 100

# Set up boundaries of simulation
boundary_min = np.array([0, 0])
boundary_max = np.array([10, 10])

# Set up mass of pedestrians
m = 80

# Set up parameters of interaction forces
T = 0.5
A = 1
B = 0.5
k = 1

# Set up desired velocity of pedestrians
v_desired = 5

# Set up minimum distance between pedestrians
min_distance = 0.5

# Set up initial positions and velocities of pedestrians
pedestrians = []
for i in range(n_pedestrians):
    r = np.random.uniform(boundary_min, boundary_max, size=2)
    v = np.zeros(2)
    pedestrians.append(Pedestrian(r, m, T, A, B, v_desired, boundary_min, boundary_max, min_distance,k))

# Set up walls
walls = []
vertices = np.array([[0, 0], [10, 0], [10, 10], [0, 10]])
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
    scatters.append(ax.scatter([pedestrian.r[0]], [pedestrian.r[1]], color='k'))

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
        update_position(pedestrian, dt)
    # Update scatter plots for pedestrians
    for i, pedestrian in enumerate(pedestrians):
        scatters[i].set_offsets(pedestrian.r)

# Set up animation
anim = animation.FuncAnimation(fig, animate, frames=range(n_steps), interval=200)

# Show plot
plt.show()

#anim.save('animation.mp4')
#anim.show()
