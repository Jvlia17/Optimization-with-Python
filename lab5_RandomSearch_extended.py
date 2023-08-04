"""

TODO

Dostrojenie i badanie algorytmu:
• sprawdzenie różnych sąsiedztw,
• sprawdzenie różnych rozwiązań początkowych,
• kalibracja parametrów liczbowych,
• inne, w zależności od algorytmu (schemat chłodzenia, forma listy tabu)

Warunki stopu:
• osiągnięto minimum lokalne,
• przekroczony czas obliczeń,
• przekroczona liczba iteracji od czasu ostatniej poprawy,
• kombinacja więcej niż jednego warunku stopu.

Reprezentacja rozwiązania w postaci kolejności wykonywania zadań
Extended: Rozwiązanie początkowe jako najlepsze ze 100, kombinacja dwóch warunków stopu: przekroczona liczba iteracji i liczba iteracji bez poprawy rozwiązania

"""""

import RandomNumberGenerator
import numpy as np
from time import time
import matplotlib.pyplot as plt

random = RandomNumberGenerator.RandomNumberGenerator(5546568)

def generate_matrix(number_jobs):
    jobs = []
    S = 0
    for i in range(number_jobs):
        pi = random.nextInt(1, 30)
        wi = random.nextInt(1, 30)
        jobs.append((pi, wi))
        S += pi

    for i in range(number_jobs):
        di = random.nextInt(1, S)
        jobs[i] += (di,)

    return jobs

def calculate_tardiness(schedule, jobs):
    completion_time = 0
    total_tardiness = 0
    for job_id in schedule:
        job = jobs[job_id]
        completion_time += job[0]  # Processing time
        tardiness = max(0, completion_time - job[1])  # Tardiness = max(0, completion time - due date)
        total_tardiness += tardiness * job[2]  # Weighted tardiness = tardiness * weight
    return total_tardiness

def generate_random_schedule(jobs):
    return np.random.permutation(len(jobs))


def generate_swap_neighbor(solution):
    neighbor_solution = solution.copy()
    i = random.nextInt(0, len(solution)-1)
    j = random.nextInt(0, len(solution)-1)
    neighbor_solution[i], neighbor_solution[j] = neighbor_solution[j], neighbor_solution[i]
    return neighbor_solution

def generate_insert_neighbor(solution):
    neighbor_solution = solution.copy()
    i = random.nextInt(0, len(solution) - 1)
    j = random.nextInt(0, len(solution) - 1)
    job = neighbor_solution[i]
    neighbor_solution = np.delete(neighbor_solution, i)
    neighbor_solution = np.insert(neighbor_solution, j, job)
    return neighbor_solution

def best_of_100(jobs, num_iterations):

    for _ in range(num_iterations):  # funkcja zachłanna do szukania najlepszego rozwiązania
        schedule = generate_random_schedule(jobs)
        tardiness = calculate_tardiness(schedule, jobs)

        if tardiness < best_tardiness:
            best_of_100_schedule = schedule
            best_of_100_tardiness = tardiness

    return best_of_100_schedule, best_of_100_tardiness

def random_search(jobs, iterations, max_iterations_without_improvement, use_swap):
    start = time()

    best_schedule, best_tardiness = best_of_100(jobs, num_iterations) # wartość początkowa - wartość najlepsza ze 100 iteracji
    num_iterations_without_improvement = 0  # Liczba iteracji bez poprawy

    for _ in range(iterations):

        if use_swap:
            neighbor_schedule = generate_swap_neighbor(best_schedule)

        else:
            neighbor_schedule = generate_insert_neighbor(best_schedule)

        neighbor_tardiness = calculate_tardiness(neighbor_schedule, jobs)

        if neighbor_tardiness < best_tardiness:
            best_schedule = neighbor_schedule
            best_tardiness = neighbor_tardiness
            num_iterations_without_improvement = 0  # Zresetuj liczbę iteracji bez poprawy
        else:
            num_iterations_without_improvement += 1

        if num_iterations_without_improvement >= max_iterations_without_improvement:
            break

    end = time()

    return best_tardiness

# for i in range(number_jobs):
#    print(jobs[i])

# Variables
#number_jobs = 10
num_iterations = 100
max_iterations_without_improvement = 10
best_solution = None
best_tardiness = float('inf')

"""
jobs = generate_matrix(number_jobs)

print('-------------------------------------------------------------------------------------------------------')
print('\t\t\tScheduling on a single machine with total weighted tardiness using Random Search')
print('-------------------------------------------------------------------------------------------------------')

best_schedule, best_tardiness = random_search(jobs, num_iterations, max_iterations_without_improvement)

print("Najlepsza kolejność według random search:", best_schedule)
print("Najniższa wartość kary według random search:", best_tardiness)

"""


times = dict()
pomiar_swap = []
pomiar_insert = []

for number_jobs in range(1,100):
    times[number_jobs] = []
    jobs = generate_matrix(number_jobs)
    t = random_search(jobs, num_iterations, max_iterations_without_improvement, True) # swap
    times[number_jobs].append( t )

for n in times:
    stamps = times[n]
    avg = sum(stamps) / len(stamps)
    pomiar_swap.append(avg)

for number_jobs in range(1, 100):
    times[number_jobs] = []
    jobs = generate_matrix(number_jobs)
    t = random_search(jobs, num_iterations, max_iterations_without_improvement, False)  # insert
    times[number_jobs].append(t)

for n in times:
    stamps = times[n]
    avg = sum(stamps) / len(stamps)
    pomiar_insert.append(avg)

x = list(range(1, 100))
y = pomiar_swap
z = pomiar_insert

plt.plot(x,y, label = "Swap")
plt.plot(x,z, label = "Insert")
plt.xlabel('Ilość zadań')
plt.ylabel('Rozwiązanie')
plt.title("Zależność rozwiązania od ilości iteracji wersja rozszerzona")
plt.legend()
plt.show()