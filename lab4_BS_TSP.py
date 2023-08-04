import heapq
import numpy as np
import RandomNumberGenerator
import array
from time import time
import matplotlib.pyplot as plt

random = RandomNumberGenerator.RandomNumberGenerator(5546568)

def generate_sym_graph(size: int): # symetryczny graf

    n_rows = size
    n_cols = size

    arr = np.empty((n_rows, n_cols))

    for i in range(0, size):
        for j in range(0, size):
            if [i] == [j]:
                arr[i][j] = np.inf
            else:
                arr[i][j] = np.array(random.nextInt(1, 30))
        for i in range(0, size):
            for j in range(i, size):
                arr[j][i] = arr[i][j]
    return arr

def generate_graph(size: int): # niesymetryczny graf

    n_rows = size
    n_cols = size

    arr = np.empty((n_rows, n_cols))

    for i in range(0, size):
        for j in range(0, size):
            if [i] == [j]:
                arr[i][j] = np.inf
            else:
                arr[i][j] = np.array(random.nextInt(1, 30))
    return arr

def nearest_neighbor(distances, start_node): # funkcja nearest neighbour

    n = distances.shape[0]
    unvisited_nodes = set(range(n))
    unvisited_nodes.remove(start_node)
    current_node = start_node
    tour = [current_node]
    total_distance = 0
    while unvisited_nodes:
        nearest_node = min(unvisited_nodes, key=lambda node: distances[current_node, node])
        unvisited_nodes.remove(nearest_node)
        tour.append(nearest_node)
        total_distance += distances[current_node, nearest_node]
        current_node = nearest_node
    total_distance += distances[current_node, start_node]
    tour.append(start_node)
    return tour, total_distance

def upper_bound(distances, beam_width): # funkcja do liczenia upper bound z nearest neighbour

    n = distances.shape[0]
    start_node = 0
    beam = [(0, [start_node])]
    upper_bound = nearest_neighbor(distances, start_node)[1]
    while beam:
        candidates = []
        for _, tour in beam:
            last_node = tour[-1]
            for next_node in range(n):
                if next_node not in tour:
                    new_tour = tour + [next_node]
                    new_distance = sum(distances[i, j] for i, j in zip(new_tour, new_tour[1:])) + distances[last_node, next_node]
                    if len(candidates) < beam_width or new_distance <= candidates[-1][0]:
                        heapq.heappush(candidates, (new_distance, new_tour))
                        if len(candidates) > beam_width:
                            heapq.heappop(candidates)
        beam = candidates
        if beam:
            upper_bound = beam[0][0]
    return upper_bound

def lower_bound(distances, partial_tour): # funkcja dla lower bound

    n = distances.shape[0]
    unvisited_nodes = set(range(n)) - set(partial_tour)
    current_node = partial_tour[-1]
    total_distance = sum(distances[i, j] for i, j in zip(partial_tour, partial_tour[1:]))
    while unvisited_nodes:
        nearest_node = min(unvisited_nodes, key=lambda node: distances[current_node, node])
        unvisited_nodes.remove(nearest_node)
        total_distance += distances[current_node, nearest_node]
        current_node = nearest_node
    total_distance += distances[current_node, partial_tour[0]]
    return total_distance

def tsp_beam_search(dist_matrix, beam_width, upper_bound):
    start = time()

    num_cities = dist_matrix.shape[0]

    start_state = (tuple([0]), 0)
    beam = [start_state]

    best_path = None
    best_cost = np.inf

    while beam:                       # działa dopóki lista beam nie będzie pusta, czyli dopóki algorytm nie przebada wszystkich stanów
        candidates = []               # tworzymy listę dla stanów, które spełnią warunki i będą potencjalnymi kandydatami
        for state, cost in beam:      # pobiera stan i koszt
            last_city = state[-1]     # przypisanie zmiennej 'last_city' ostatniego elementu z listy 'state'
            for next_city in range(num_cities):   # iteruje przez zbiór miast przypisujac next_city od 0 do 14
                if next_city not in state:        # sprawdza czy miasto nie znajduje się już w zbiorze stanów 'state'. Jeśli nie, wtedy jest to potencjalny kandydat.
                    new_state = state + (next_city,) # dla każdego miasta next_city spoza dotychczas odwiedzonych miast (czyli nie znajdującego się w tupli state), tworzony jest nowy stan new_state poprzez dodanie next_city do tupli state
                    new_cost = cost + dist_matrix[last_city, next_city] # obliczany jest koszt new_cost przejścia z ostatnio odwiedzonego miasta (czyli ostatniej wartości w tupli state) do miasta next_city, a następnie dodany do kosztu cost
                    if lower_bound(dist_matrix, new_state) <= upper_bound and new_cost <= upper_bound: # sprawdza czy dolne ograniczenie lower_bound dla kosztu podróży między miastami last_city i next_city jest mniejsze lub równe górnemu ograniczeniu.  Drugi warunek sprawdza, czy koszt new_cost jest mniejszy lub równy upper_bound.
                        candidates.append((new_state, new_cost)) # jeśli spełnia oba warunki, zostaje dodany do listy 'candidates'

        beam = heapq.nsmallest(beam_width, candidates, key=lambda x: x[1])     # spośród kandydatów wybierani są ci z najniższym kosztem i zapisywani na liście 'beam'

        for state, cost in beam:
            last_city = state[-1]     # przypisuje ostatnie miasto ze state do last_city
            total_cost = cost + dist_matrix[last_city, 0]    # oblicza łączny koszt podróży dodając koszt 'cost' do odległości między 'last_city', a miastem początkowym
            if len(state) == num_cities and total_cost < best_cost:   # sprawdza, czy liczba miast w 'state' jest równa liczbie wszystkim miast i czy 'total_cost' jest mniejszy od dotychczasowego najlepszego kosztu 'best_cost'
                best_path = state    # Jeśli tak, to przypisuje 'state' do 'best_path'
                best_cost = total_cost   # ... i aktualizuje 'best_cost'

        if not any(cost <= upper_bound for _, cost in beam):   # sprawdza, czy drugi element kroki, czyli 'cost' dla jakiegokolwiek miasta jest mniejszy lub równy 'upper_bound'
            break   # przerywa, bo dalsze przetwarzanie nie ma sensu, gdyż żaden koszt nie mieści się w granicy 'upper_bound'

    best_path = best_path + (0,)
    best_cost = best_cost + dist_matrix[last_city, 0]
    end = time()
    return best_cost, best_path

# Zmienne
size = 15
dist_matrix = generate_graph(size)
beam_width = 5 # 2, 5, 10, 15, 20

for i in range(15):
    print(dist_matrix[i])

print('--------------------------------------------------------------------------')
print('\t\t\tTraveling Salesman Problem using Beam Search')
print('--------------------------------------------------------------------------')

best_cost, best_path = tsp_beam_search(dist_matrix, beam_width, upper_bound(dist_matrix, beam_width))

print("Best cost: ", best_cost)
print("Best state: ", best_path)

