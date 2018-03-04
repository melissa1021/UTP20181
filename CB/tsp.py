
'''
import matplotlib.pyplot as plt
import random
import time
import itertools
import urllib
import csv
import functools
from statistics import mean, stdev

def alltours_tsp(cities):
    "Generate all possible tours of the cities and choose the shortest tour."
    return shortest_tour(alltours(cities))

def shortest_tour(tours): 
    "Choose the tour with the minimum tour length."
    return min(tours, key=tour_length)


alltours = itertools.permutations

cities = {1, 2, 3}

list(alltours(cities))

def tour_length(tour):
    "The total of distances between each pair of consecutive cities in the tour."
    return sum(distance(tour[i], tour[i-1]) 
               for i in range(len(tour)))


class Point(complex):
    x = property(lambda p: p.real)
    y = property(lambda p: p.imag)
    
City = Point

def distance(A, B): 
    "The distance between two points."
    return abs(A - B)


A = City(3, 0)
B = City(0, 4)
distance(A, B)

'''



import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx

import random, operator, time, itertools, math
import numpy

#%config InlineBackend.figure_format = 'retina'
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.rcParams['text.latex.preamble'] ='\\usepackage{libertine}\n\\usepackage[utf8]{inputenc}'

import seaborn
seaborn.set(style='whitegrid')
seaborn.set_context('notebook')



def exact_TSP(cities):
    'Genere todos los recorridos posibles de las ciudades y elija el mÃ¡s corto.'
    return shortest(alltours(cities))

def shortest(tours): 
    'Devuelve el recorrido con la distancia total mÃ­nima.'
    return min(tours, key=total_distance)

alltours = itertools.permutations # The permutation function is already defined in the itertools module
cities = {1, 2, 3}
list(alltours(cities))


def total_distance(tour):
    'La distancia total entre cada par de ciudades consecutivas en el recorrido.'
    return sum(distance(tour[i], tour[i-1]) 
               for i in range(len(tour)))


City = complex # Constructor para nuevas ciudades, p. City(300, 400)

def distance(A, B):
    'La distancia euclidiana entre dos ciudades.'
    return abs(A - B)

A = City(300, 0)
B = City(0, 400)
distance(A, B)

def generate_cities(n):
    'Haz un conjunto de n ciudades, cada una con coordenadas al azar.'
    return set(City(random.randrange(10, 890), 
                    random.randrange(10, 590)) 
               for c in range(n))
                   
                   
cities8, cities10, cities100, cities1000 = generate_cities(8), generate_cities(10), generate_cities(100), generate_cities(1000)
cities8

def plot_tour(tour, alpha=1, color=None):
    'Dibuja el recorrido con lÃ­neas azules entre cÃ­rculos azules, y la ciudad de inicio como un cuadrado rojo.'
    plotline(list(tour) + [tour[0]], alpha=alpha, color=color)
    plotline([tour[0]], style='gD', alpha=alpha, size=10)
    # plt.show()
    
def plotline(points, style='bo-', alpha=1, size=7, color=None):
    'Dibuja una lista de puntos (nÃºmeros complejos) en el plano 2-D.'
    X, Y = XY(points)
    
    if color:
        plt.plot(X, Y, style, alpha=alpha, markersize=size, color=color)
    else:
        plt.plot(X, Y, style, alpha=alpha, markersize=size)
    
def XY(points):
    'Dada una lista de puntos, devuelve dos listas: coordenadas X y Y.'
    return [p.real for p in points], [p.imag for p in points]


tour = exact_TSP(cities8)

plot_tour(tour)