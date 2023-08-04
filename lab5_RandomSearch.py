"""

Reprezentacja rozwiązania w postaci kolejności wykonywania zadań
Basic: rozwiązanie początkowe jako losowe, warunek stopu to maksymalna liczba iteracji
Sąsiedztwa: swap i insert

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

def best_of_100(jobs):

    for _ in range(1,100):  # funkcja zachłanna do szukania najlepszego rozwiązania
        schedule = generate_random_schedule(jobs)
        tardiness = calculate_tardiness(schedule, jobs)

        if tardiness < best_tardiness:
            best_of_100_schedule = schedule
            best_of_100_tardiness = tardiness

    return best_of_100_schedule, best_of_100_tardiness

def random_search(jobs, iterations, use_swap, use_extended, use_stop):
    start = time()
    max_iterations_without_improvement = 1/10 * iterations
    num_iterations_without_improvement = 0  # Liczba iteracji bez poprawy

    if use_extended:
        best_schedule, best_tardiness = best_of_100(jobs) # wartość początkowa - najlepsza ze 100
    else:
        best_schedule = generate_random_schedule(jobs) # wartość początkowa - losowo wybrana
        best_tardiness = calculate_tardiness(best_schedule, jobs)

    if use_stop:
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
                print("Zrywam petle")
                break
    else:
        for _ in range(iterations):
            if use_swap:
                neighbor_schedule = generate_swap_neighbor(best_schedule)
            else:
                neighbor_schedule = generate_insert_neighbor(best_schedule)

            neighbor_tardiness = calculate_tardiness(neighbor_schedule, jobs)

            if neighbor_tardiness < best_tardiness:
                best_schedule = neighbor_schedule
                best_tardiness = neighbor_tardiness

    end = time()

    return best_schedule, best_tardiness

# Variables
number_jobs = 10
num_iterations = 250000
best_solution = None
best_tardiness = float('inf')
jobs = generate_matrix(number_jobs)

print('-------------------------------------------------------------------------------------------------------')
print('\t\t\tScheduling on a single machine with total weighted tardiness using Random Search')
print('-------------------------------------------------------------------------------------------------------')

best_schedule, best_tardiness = random_search(jobs, num_iterations, False, False, False) # use_swap, use_extended, use_stop

print("Najlepsza kolejność według random search:", best_schedule)
print("Najniższa wartość kary według random search:", best_tardiness)

# Reprezentacja rozwiązania w postaci kolejności wykonywania zadań

"""
times = dict()
pomiar_swap_basic = []
pomiar_insert_basic = []
pomiar_swap_extended = []
pomiar_insert_extended = []

for number_jobs in range(3,40):
    jobs = generate_matrix(number_jobs)
    times[number_jobs] = []
    t = random_search(jobs, num_iterations, False, True, True) # use_swap, use_extended, use_stop
    times[number_jobs].append( t )
    print(number_jobs)

for n in times:
    stamps = times[n]
    avg = sum(stamps) / 10
    pomiar_swap_basic.append(avg)


for num_iterations in [100,200,300,400,500,600,700,800,900,1000]:
    jobs = generate_matrix(number_jobs)
    times[num_iterations] = []
    t = random_search(jobs, num_iterations, False, False, False)  # swap & extended & max iterations
    times[num_iterations].append(t)

for n in times:
    stamps1 = times[n]
    avg1 = sum(stamps1) / len(stamps1)
    pomiar_swap_extended.append(avg1)


x = list(range(3, 40))
a = pomiar_swap_basic
# b = pomiar_swap_extended

# plt.plot(x,b, label = "Gorsza kalibracja")
plt.plot(x,a, label = "Random search")

print(x, a)

plt.xlabel('Ilość zadań')
plt.ylabel('Rozwiązanie')
plt.title("Zależność rozwiązania od ilości zadań")
plt.legend()
plt.show()
"""