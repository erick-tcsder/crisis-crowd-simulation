import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from shapely.geometry import Point, Polygon

# Class for pedestrian
# Class for pedestrian
class Pedestrian:
    def __init__(self, p: np.array, m: float, t: float, A: float, B: float, j: float, r: float,
                 k: float, K: float, v_desired: float, boundary_min: np.array, boundary_max: np.array):
        self.p = p                  # posición
        self.m = m                  # masa
        self.v = np.zeros_like(p)   # velocidad
        self.t = t                  # tiempo de actualización
        self.A = A                  # intensidad de la fuerza repulsiva entre peatones
        self.B = B                  # factor de cambio de la fuerza repulsiva respecto la distancia
        self.j = j                  # la distancia mínima que el peatón debe mantener con respecto a otros
        self.r = r                  # radio del peatón            
        self.k = k                  # constante de fuerza corporal
        self.K = K                  # constante de fricción

        self.v_desired = v_desired          # velocidad deseada
        self.boundary_min = boundary_min    # límite inferior del espacio en el que se mueve el peatón
        self.boundary_max = boundary_max    # límite superior del espacio en el que se mueve el peatón  
    
    def wall_force(self, walls: ['Wall']):
         # Inicializamos la aceleración.
        fiW = np.zeros_like(self.p)

        # Añadimos la fuerza de las interacciones con las paredes.
        for wall in walls:
            # Calculamos la distancia de este peatón al otro.
            dif = self.wall_difference(wall)           # vector diferencia
            diW = norm(dif)                            # norma del vector diferencia (distancia)

            # Si el peatón está demasiado cerca de la pared.
            if diW < self.j:
                niW = dif / diW             # vector diferencia normalizado
                r = self.r                  # radio del peatón
                tiW = np.flip(niW)          # dirección tangencial
                tiW[0] = -tiW[0]
                dv = np.cross(self.v, tiW)  # velocidad tangencial

                # Fuerza de repulsión entre peatones
                f_repulsive = self.A * np.exp((r - diW) / self.B) * niW

                # Fuerza corporal que el peatón ejerce a la pared.
                # Si la distancia es menor que la suma de los radios, entonces los peatones se tocan.
                # Solo en estos casos interviene la fuerza corporal entre peatones.
                f_body = (self.k * (r - diW) if diW > r else 0) * niW

                # Si la distancia es menor que la suma de los radios, entonces los peatones se tocan.
                # Solo en estos casos interviene la fuerza corporal entre peatones.
                f_friction = (self.K * (r - diW) * dv if diW > r else 0) * tiW

                # Sumamos todas las fuerzas para calcular la fuerza total.
                fiW += f_repulsive + f_body + f_friction

        # Devolvemos la fuerza de repulsión total entre el peatón y las paredes.
        return fiW
    
    # Función para calcular la fuerza de repulsión respecto al resto de peatones.
    def repulsion_force(self,  pedestrians: ['Pedestrian']):
        # Inicializamos la aceleración.
        fij = np.zeros_like(self.p)

        # Añadimos la fuerza de las interacciones con otros peatones.
        for pedestrian in pedestrians:
            # Ignoramos a este peatón (no tiene sentido considerar las interacciones consigo mismo).
            if pedestrian == self:
                continue

            # Calculamos la distancia de este peatón al otro.
            dif = pedestrian.p - self.p                # vector diferencia
            dij = norm(dif)                            # norma del vector diferencia (distancia)

            # Si el peatón está demasiado cerca de la pared.
            if dij < self.j:
                nij = dif / dij                            # vector diferencia normalizado
                rij = self.r + pedestrian.r                # suma de los radios de ambos peatones
                tij = np.flip(nij)                         # dirección tangencial
                tij[0] = -tij[0]
                dv = np.cross(pedestrian.v - self.v, tij)  # diferencia de velocidad tangencial

                # Fuerza de repulsión entre peatones
                f_repulsive = self.A * np.exp((rij - dij) / self.B) * nij

                # Fuerza corporal entre peatones.
                # Si la distancia es menor que la suma de los radios, entonces los peatones se tocan.
                # Solo en estos casos interviene la fuerza corporal entre peatones.
                f_body = (self.k * (rij - dij) if dij > rij else 0) * nij

                # Si la distancia es menor que la suma de los radios, entonces los peatones se tocan.
                # Solo en estos casos interviene la fuerza corporal entre peatones.
                f_friction = (self.K * (rij - dij) * dv if dij > rij else 0) * tij

                # Sumamos todas las fuerzas para calcular la fuerza total.
                fij += f_repulsive + f_body + f_friction

        # Devolvemos la fuerza de repulsión total entre los peatones.
        return fij
    
    # Función para actualizar la velocidad del peatón.
    def update_velocity(self, dt: float, pedestrians: ['Pedestrian'], walls: ['Wall'], exits: ['Exit']):
        fij = self.repulsion_force(pedestrians)  # Calculamos la fuerza de repulsión de este peatón con los demás.
        fiW = self.wall_force(walls)             # Calculamos la fuerza de repulsión de este peatón con las paredes.

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
dt = 0.7
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
