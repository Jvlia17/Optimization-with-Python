# trzy - dwa takie same, jeden moze byc ten sam.
# Wszystkie mogą być dyskretne lub ciągłe.

from docplex.mp.model import Model
from RandomNumberGenerator import RandomNumberGenerator
from time import time
import matplotlib.pyplot as plt

def RunModel(seed, n): # n - liczba zadan i wykonawców
    gen = RandomNumberGenerator(seed)

    x = [] # rozwiązania
    values = [] # macierz kosztów

    for i in range(0,n):
        values.append([])
        for j in range(0,n):
            values[-1].append(gen.nextInt(1,50))

    print(values)

    # Model
    m = Model(name="zagadnienie-przydzialu")

    for i in range(0,n):
        x.append([m.binary_var(name="x_{0}_{1}".format(i+1,j+1)) for j in range(0,n)])

    m.minimize(m.sum(x[i][j] * values[i][j] for i in range(0, n) for j in range(0, n)))

    for i in range(0, n):
        for j in range(0, n):
            m.add_constraint(m.sum(x[i][j] for i in range(0, n)) == 1) # żeby każde zadanie miało jednego wykonawce i na odwrót
            m.add_constraint(m.sum(x[i][j] for j in range(0, n)) == 1)

    # Rozwiązanie i liczenie czasu
    start = time()
    m.solve()
    end = time()
    m.print_solution()
    return end - start

times = dict()
pomiar = []

for n in [3,6,9,12,15,18,21]:
    times[n] = []
    for seed in [ 10*i for i in range(1,10) ]:
        t = RunModel(seed, n)
        times[n].append( t )

for n in times:
    stamps = times[n]
    avg = sum(stamps) / len(stamps)
    print(avg)
    pomiar.append(avg)

print(pomiar)
x=[3,6,9,12,15,18,21]
y= pomiar
plt.plot(x,y)
plt.xlabel('Liczba parametrów n')
plt.ylabel('Czas w sekundach')
plt.title("Zależność czasu od ilości zmiennych")
plt.show()