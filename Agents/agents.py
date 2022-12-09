class Agent:
    def __init__(self, name, location, graph):
        self.name = name
        self.location = location
        self.out = False  # Indica si el agente ha logrado salir del edificio
        self.graph = graph  # Grafo que representa las posibles rutas en el edificio

    def move_random(self, destinations):
        # destinations es una lista de posibles destinos al que el agente puede
        # moverse, y se elige uno de forma aleatoria
        self.location = random.choice(destinations)

        # Si el agente se mueve a la ubicación de la salida del edificio, se marca
        # como habiendo logrado salir
        if self.location == "Exit":
            self.out = True

    def move_a_star(self, destinations, heuristic):
        # destinations es una lista de posibles destinos al que el agente puede
        # moverse, y se utiliza el algoritmo A* para seleccionar el camino más
        # cercano a la salida (indicada por la función heurística)
        path = A_star(self.graph, self.location, "Exit", heuristic)
        self.location = path[1]  # Se mueve al segundo nodo en el camino encontrado

        # Si el agente se mueve a la ubicación de la salida del edificio, se marca
        # como habiendo logrado salir
        if self.location == "Exit":
            self.out = True

    def interact(self, other):
        if self.location == other.location:
        # Si ambos agentes están en la misma ubicación, pueden interactuar
        # de acuerdo a una lógica específica, como, por ejemplo, ayudarse
        # mutuamente a evacuar el edificio o compartir información
