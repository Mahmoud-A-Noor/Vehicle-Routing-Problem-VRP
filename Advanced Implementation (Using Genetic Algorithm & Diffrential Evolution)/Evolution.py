from Selection import selection
from EV import evolution as EV
from random import randint, sample

def crossOver(parents,randIndividuals,cities):
    '''Return population composed of parents, children and some random individuals'''
    population = EV.includeParents(parents)
    for p in parents:

        parent1 = p[0]
        parent2 = p[1]

        r = randint(1 , len(p[0])-1)
        
        child1 = parent1[:r]
        child2 = parent2[:r]

        for i in range(r,len(parent1)):
            if parent2[i] not in child1:
                child1 += parent2[i]
            elif parent2[i] != ' ':
                child1 += '*'
            else:
                child1 += parent2[i]
            
            if parent1[i] not in child2:
                child2 += parent1[i]
            elif parent1[i] != ' ':
                child2 += '*'
            else:
                child2 += parent1[i]

        cities1 = EV.filterCities(child1,cities)
        cities2 = EV.filterCities(child2,cities)

        list1 = list(child1)
        list2 = list(child2)

        for x in range(r,len(child1)):
            if child1[x] == '*':
                c = cities1[0]
                list1[x] = c
                cities1.remove(c)

            if child2[x] == '*':
                c = cities2[0]
                list2[x] = c
                cities2.remove(c)

        child1 = ''.join(list1)
        child2 = ''.join(list2)

        population.append(child1)
        population.append(child2)

    population =  EV.includeRands(population , randIndividuals)

    return population
    
def randomIndividuals(pop,rate):
    rate = int(rate * len(pop[0]))
    individuals = sample(pop[0],rate)
    indices = [individuals.index(i) for i in individuals]
    return [individuals,indices]

def mutate(population,rate=0.25):
    '''Return partially Inversed individual according to mutation rate'''
    indices = randomIndividuals(population,rate)[1]
    for i in indices:
        s = population[i]
        s = EV.reflect(s)
        population[i] = s
     
    return population

def evolve(population,mutation_rate=0.45):
    selected = selection(population,0.20, 0.20) 
    parents = selected[0]
    randIndividuals = selected[1]
    cities = EV.getCities(parents)

    population = crossOver(parents,randIndividuals,cities)
    
    mutate(population,mutation_rate)
    
    return population