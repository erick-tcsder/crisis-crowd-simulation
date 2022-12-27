import math

def circle_to_polygon(center, radius, num_sides):
  # Calcula el ángulo en radianes entre cada lado del polígono
  angle = 2 * math.pi / num_sides

  # Crea una lista para almacenar las coordenadas de los vértices del polígono
  vertices = []

  # Calcula las coordenadas de cada vértice del polígono y las agrega a la lista
  for i in range(num_sides):
    x = center[0] + radius * math.cos(i * angle)
    y = center[1] + radius * math.sin(i * angle)
    vertices.append((x, y))

  return vertices

# Prueba la función con una circunferencia de centro (0, 0) y radio 1, y un polígono de 36 lados
center = (0, 0)
radius = 1
num_sides = 4
vertices = circle_to_polygon(center, radius, num_sides)
print(vertices)
