class Building:
  def __init__(self, agents, graph):
    self.agents = agents  # Lista de agentes en el edificio
    self.graph = graph  # Grafo que representa las posibles rutas en el edificio
    self.exited_agents = []  # Lista de agentes que han logrado salir del edificio

  def simulate(self, steps, move_random=False, move_a_star=False, heuristic=None):
    # steps es el número de pasos que se van a simular
    for i in range(steps):
      # Se recorren todos los agentes y se les permite moverse o interactuar
      # de acuerdo a los argumentos proporcionados
      for agent in self.agents:
        if move_random:
        # Si move_random es True, se permite que el agente se mueva
            pass
        if move_a_star:
        # Si move_a_star es True, se permite que el agente se mueva
            pass