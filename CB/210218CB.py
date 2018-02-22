import deap.algorithms as algorithms
import deap.base as base
import deap.creator as creator
import deap.tools as tools
import numpy as np  
import random


'''
Cuando N es impar es facil realizar el cuadro magico siguiendo el siguiente algoritmo. 
N = 5;N2 = N**2; K=N*(N2+1)/2
Donde N es 5, el numero mayor del cuadro sera N cuadrado, y el numero que genera por cualquier lado sera K, 
que es la sumatoria de N hasta N cuadrado
'''

N = 5;N2 = N**2; K=N*(N2+1)/2

creator.create('FitnessMin',base.Fitness,weights = (-1.0,))
creator.create('Individual',list,fitness = creator.FitnessMin)
toolbox = base.Toolbox()

# Generador de atributos
toolbox.register('Indices',random.sample,range(1,N2+1),N2)

# Inicializadores de estructuras
toolbox.register('Individual',tools.initIterate,creator.Individual,toolbox.Indices)

# Generar la poblacion
toolbox.register('population',tools.initRepeat, list, toolbox.Individual)

def evalMS(individual):
    ms = np.array(individual).reshape((N,N))
    tot = 0.0
    for i in range(N):
        tot += abs(K-sum(ms[i,:]))
        tot += abs(K-sum(ms[:,i]))
        # ms[i,:] Estoy sumando lo que vale la fila i y el dos puntos indica que no me interesa 
        # El abs es valor absloluto
    tot += abs(K-sum(ms.diagonal()))
    tot += abs(K-sum(np.rot90(ms)))
    return tot,

toolbox.register('mate',tools.cxPartialyMatched)
toolbox.register('mutate', tools.mutShuffleIndexes,indpb = 0.05)
toolbox.register('select',tools.selTournament,toursize = 3)
toolbox.register('evaluate',evalMS)

def main():
    pop = toolbox.population(n = 50)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    
    stats.register('awg',np.mean)
    stats.register('std',np.std)

    # falta algo por poner.....
    algorithms.eaSimple(pop,toolbox,0.7,0.2,40, stats = stats, halloffame=hof)
    # 0.7 --> Que informacion genetica vamos a llevar
    # 0.2 --> Mutacion
    # 40  --> generaciones
    
    return pop


if __name__ == "__main__":
    print('Entro al main')
    print(main())

