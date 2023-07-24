import random
from DP import preparation as DP

def createPopulation(numOfTrucks=6):
    '''Return random initialized Population'''
    population = []
    cities = DP.get_cities()

    for i in range(100):
        cities = random.sample(cities, len(cities))

        individual = []

        for z in range(numOfTrucks):
            individual.append(" ")

        c=0
        for x in range(len(cities)):
            if(c==numOfTrucks):
                c=0
            individual[c] += cities[x]
            c+=1

        individual = ''.join(individual)

        population.append(individual.strip())

    fit = DP.calc_fitness(population)
    return [population,fit]