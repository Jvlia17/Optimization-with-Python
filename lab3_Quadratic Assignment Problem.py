# trzy - dwa takie same, jeden moze byc ten sam.
# Wszystkie mogą być dyskretne lub ciągłe.
# jak sie zmienia czas podczas zwiekszania danych

from docplex.mp.model import Model

n = 4 #liczba zakładów
k = 4 #liczba lokalizacji

m = Model(name="kwadratowe-zagadnienie-przydzialu")

x = []
for i in range(0,n):
    x.append([m.binary_var(name="x_{0}_{1}".format(i+1,j+1)) for j in range(0,k)])

przeplyw = [ #macierz kosztów
    [100, 29, 42, 36],
    [39, 100, 47, 2],
    [41, 17, 100, 25],
    [10, 48, 1, 100]
];

odleglosc = [ #macierz kosztów
    [100, 6, 47, 41],
    [13, 100, 37, 18],
    [23, 28, 100, 42],
    [18, 44, 29, 100]
];

m.minimize(m.sum(x[i][j]*przeplyw[i][j]*odleglosc[i][j] for i in range(0,n) for j in range(0,k)))

for i in range(0, n):
    for j in range(0, k):
        m.add_constraint(m.sum(x[i][j] for i in range(0, n)) == 1)
        m.add_constraint(m.sum(x[i][j] for j in range(0, k)) == 1)

m.solve()

m.print_solution()