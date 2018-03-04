#!python2
# Magic Square

import deap.algorithms as algorithms
import deap.base    as base
import deap.creator as creator
import deap.tools   as tools
import numpy        as np
import random

N = 4; N2 = N**2; k = N*(N2+1)/2

creator.create('FitnessMin', base.Fitness, weights=(-1.0,))
creator.create('Individual', list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()

# Attribute generator
toolbox.register("indices", random.sample, range(1,N2+1), N2)

# Structure initializers
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evalMS(individual):
        ms = np.array(individual).reshape((N,N))
        tot = 0.0
        for i in range(N):
                tot += abs(k - sum(ms[i,:]))
                tot += abs(k - sum(ms[:,i]))
        tot += abs(k - sum(ms.diagonal()))
        tot += abs(k - sum(np.rot90(ms).diagonal()))
        return tot,

toolbox.register("mate", tools.cxPartialyMatched)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", evalMS)

def main():

        pop = toolbox.population(n=50)

        hof = tools.HallOfFame(1)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", np.mean)
        stats.register("std", np.std)
        stats.register("min", np.min)
        stats.register("max", np.max)

        algorithms.eaSimple(pop, toolbox, 0.7, 0.2, 40, stats=stats, halloffame=hof)

        return pop

print(main())