import random
import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Rastrigin function
def rastrigin_function(position):
    A = 10
    n = len(position)
    return A * n + sum([(x ** 2 - A * np.cos(2 * math.pi * x)) for x in position])

# Particle class
class Particle:
    def __init__(self, dimensions, bounds):
        self.dimensions = dimensions
        self.bounds = bounds
        self.position = [random.uniform(bounds[i][0], bounds[i][1]) for i in range(dimensions)] # generowanie losowej pozycji z zakresu ograniczeń bounds[i][0] do bounds[i][1]
        self.velocity = [random.uniform(-1, 1) for _ in range(dimensions)] # Prędkość jest inicjalizowana losowo w przedziale od -1 do 1, co umożliwia cząstkom eksplorowanie przestrzeni poszukiwań w różnych kierunkach
        self.best_position = self.position[:]
        self.best_fitness = rastrigin_function(self.position)

    def update_velocity(self, global_best_position, w, c1, c2):
        for i in range(self.dimensions):
            r1 = random.random()
            r2 = random.random()

            # NAJWAŻNIEJSZE RÓWNANIE
            cognitive_component = c1 * r1 * (self.best_position[i] - self.position[i]) # dążenie do lokalnego
            social_component = c2 * r2 * (global_best_position[i] - self.position[i]) # dążenie do globalnego
            self.velocity[i] = w * self.velocity[i] + cognitive_component + social_component

    def update_position(self):
        for i in range(self.dimensions):
            self.position[i] += self.velocity[i]

            # W ten sposób sprawdzamy i korygujemy pozycję cząstki, aby pozostała w określonych granicach
            if self.position[i] < self.bounds[i][0]:
                self.position[i] = self.bounds[i][0]
            elif self.position[i] > self.bounds[i][1]:
                self.position[i] = self.bounds[i][1]

        fitness = rastrigin_function(self.position)

        if fitness < self.best_fitness:
            self.best_position = self.position[:]
            self.best_fitness = fitness

def particle_swarm_optimization(dimensions, bounds, num_particles, max_iterations, w, c1, c2):
    particles = [Particle(dimensions, bounds) for _ in range(num_particles)]

    global_best_position = particles[0].best_position[:]
    global_best_fitness = particles[0].best_fitness

    for i in range(1, num_particles):
        if particles[i].best_fitness < global_best_fitness:
            global_best_position = particles[i].best_position[:]
            global_best_fitness = particles[i].best_fitness

    all_particle_positions = [particle.position[:] for particle in particles]

    for _ in range(max_iterations):
        for particle in particles:
            particle.update_velocity(global_best_position, w, c1, c2)
            particle.update_position()

            if particle.best_fitness < global_best_fitness:
                global_best_position = particle.best_position[:]
                global_best_fitness = particle.best_fitness

            all_particle_positions.append(particle.position[:])

    return global_best_position, global_best_fitness, all_particle_positions
    #return global_best_fitness


# Parameters
dimensions = 2
bounds = [(-5.12, 5.12)] * dimensions
num_particles = 30
max_iterations = 100
w = 0.5
c1 = 1.0
c2 = 1.0

# Generate grid points for visualization
x = np.linspace(bounds[0][0], bounds[0][1], 100)
y = np.linspace(bounds[1][0], bounds[1][1], 100)
X, Y = np.meshgrid(x, y)
Z = np.zeros_like(X)

for i in range(len(x)):
    for j in range(len(y)):
        Z[i, j] = rastrigin_function([X[i, j], Y[i, j]])

# PSO optimization
best_position, best_fitness, all_particle_positions = particle_swarm_optimization(
    dimensions, bounds, num_particles, max_iterations, w, c1, c2
)

# Plotting
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, cmap='viridis')
ax.scatter(
    [position[0] for position in all_particle_positions],
    [position[1] for position in all_particle_positions],
    [rastrigin_function(position) for position in all_particle_positions],
    color='b',
    label='Particle Positions'
)
ax.scatter(best_position[0], best_position[1], best_fitness, color='r', label='Global Best')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Fitness')
ax.set_title('Rastrigin Function')

plt.legend()
plt.show()
"""

times = dict()
pomiar_swap_basic = []
pomiar_insert_basic = []
pomiar_swap_extended = []
pomiar_insert_extended = []

for num_particles in range(1, 50):
    times[num_particles] = []
    t = particle_swarm_optimization(dimensions, bounds, num_particles, max_iterations, w, c1, c2)
    times[num_particles].append(t)

for n in times:
    stamps = times[n]
    avg = sum(stamps) / 10
    pomiar_swap_basic.append(avg)

x = list(range(1, 50))
a = pomiar_swap_basic
# b = pomiar_swap_extended

# plt.plot(x,b, label = "Gorsza kalibracja")
plt.plot(x,a, label = "Particle swarm optimization")

print(x, a)

plt.xlabel('Ilość cząstek')
plt.ylabel('Wartość rozwiązania')
plt.title("Zależność rozwiązania od ilości cząstek")
plt.legend()
plt.show()
"""