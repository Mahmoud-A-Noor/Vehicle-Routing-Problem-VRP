from random import sample, randint

import numpy as np

cities = {
    'A': [45, 400],
    'B': [100, 200],
    'C': [300, 600],
    'D': [120, 100],
    'E': [247, 200],
    'F': [290, 150],
    'G': [332, 100],
    'H': [375, 50],
    'I': [417, 0],
    'J': [460, 50],
    'K': [502, 100],
    'L': [545, 150],
    'M': [587, 200],
    'N': [630, 250],
    'O': [672, 300],
    'P': [715, 350],
    'Q': [757, 400],
    'R': [800, 450],
    'S': [842, 500],
    'T': [885, 550],
    'U': [927, 600],
    'V': [970, 650],
    'W': [1012, 700],
    'X': [1055, 750],
    'Y': [1097, 800],
    'Z': [1140, 850],
}
startPoint = input("start point: ")
listOfCities = list(cities.keys())
listOfCities.remove(startPoint)


def initializePopulation(populationSize=100, numberOfTrucks=4):
    population = []
    for i in range(populationSize):
        shuffuledCities = sample(listOfCities, len(listOfCities))

        individual = []

        for z in range(numberOfTrucks):
            individual.append(" ")

        c = 0
        for x in range(len(shuffuledCities)):
            if (c == numberOfTrucks):
                c = 0
            individual[c] += shuffuledCities[x]
            c += 1

        individual = ''.join(individual)

        population.append(individual.strip())
    return population


def crossOver(population):
    mylist = []
    for index in range(0, len(population) - 1, 2):
        cities1 = list(population[index].replace(" ", ""))
        cities2 = list(population[index + 1].replace(" ", ""))
        parent1 = population[index].split(" ")
        parent2 = population[index + 1].split(" ")

        child1 = ""
        child2 = ""

        for c1, c2 in zip(parent1, parent2):
            randompoint = randint(0, len(c1))
            child1 += c1[:randompoint] + c2[randompoint:]
            child2 += c2[:randompoint] + c1[randompoint:]
            child1 += " "
            child2 += " "

        child1 = child1.strip()
        child2 = child2.strip()
        str1 = ""
        str2 = ""
        for i, j in zip(child1, child2):
            if i in cities1:
                cities1.remove(i)
                str1 += i
            else:
                if i == " ":
                    str1 += " "
                else:
                    str1 += "*"
            if j in cities2:
                cities2.remove(j)
                str2 += j
            else:
                if j == " ":
                    str2 += " "
                else:
                    str2 += "*"
        child1 = ""
        child2 = ""
        for i, j in zip(str1, str2):
            if i == "*":
                child1 += cities1[0]
                del cities1[0]
            else:
                child1 += i
            if j == "*":
                child2 += cities2[0]
                del cities2[0]
            else:
                child2 += j

        mylist.append(child1)
        mylist.append(child2)

    return mylist


def mutate(population, mutationRate=0.3):
    mutatedList = []
    notSpaceIndex = [index for index, x in enumerate(population[0]) if x != " "]
    for index, i in enumerate(population):
        if randint(0, 100) < mutationRate * 100:
            randomPoint1 = sample(notSpaceIndex, 1)[0]
            randomPoint2 = sample(notSpaceIndex, 1)[0]
            x = list(i)
            temp = x[randomPoint1]
            x[randomPoint1] = x[randomPoint2]
            x[randomPoint2] = temp
            mutatedList.append(''.join(x))
        else:
            mutatedList.append(i)
    return mutatedList


def getIndevidualFitness(individual):  # helper function for getAndAppendFitnessToPopulation function
    fitness = 0
    truckpaths = individual.split(" ")
    for i in range(len(truckpaths)):
        path = truckpaths[i]
        tmpstr = startPoint
        tmpstr += path
        tmpstr += startPoint
        truckpaths[i] = tmpstr

    for tp in truckpaths:
        if len(tp) % 2 == 0:
            for i in range(0, len(tp) - 1, 2):
                distance = 1 / np.sqrt(
                    pow(cities[tp[i + 1]][0] - cities[tp[i]][0], 2) + pow(cities[tp[i + 1]][1] - cities[tp[i]][1], 2))
                fitness += distance
        else:
            for i in range(0, len(tp) - 2, 2):
                distance = 1 / np.sqrt(np.square(cities[tp[i + 1]][0] - cities[tp[i]][0]) + np.square(
                    cities[tp[i + 1]][1] - cities[tp[i]][1]))
                fitness += distance
            distance = 1 / np.sqrt(
                np.square(cities[tp[-1]][0] - cities[tp[-2]][0]) + np.square(cities[tp[-1]][1] - cities[tp[-2]][1]))
            fitness += distance
    return fitness


def getAndAppendFitnessToPopulation(population):
    populationWithFitness = []
    for i in population:
        fitness = " "
        fitness += str(getIndevidualFitness(i))
        populationWithFitness.append(i + fitness)
    return populationWithFitness


def removeFitnessFromPopulation(population):
    populationWithoutFitness = []
    for i in population:
        x = i.split(" ")[:-1]
        tmpstr = ""
        for element in x:
            tmpstr += element
            tmpstr += " "
        tmpstr = tmpstr.strip()
        populationWithoutFitness.append(tmpstr)
    return populationWithoutFitness


def sortPopulation(population):  ### use it after appending the fitness to popuation
    return sorted(population, key=lambda x: float(x.split(" ")[-1]), reverse=True)


def selectNewPopulation(oldPopulation, newPopulation, oldPopulationRatio=0.2, newPopulationRatio=0.8):
    oldPopulation = getAndAppendFitnessToPopulation(oldPopulation)
    oldPopulation = sortPopulation(oldPopulation)

    newPopulation = getAndAppendFitnessToPopulation(newPopulation)
    newPopulation = sortPopulation(newPopulation)

    selectedPopulation = newPopulation[:int(len(newPopulation) * newPopulationRatio)] + oldPopulation[:int(
        len(oldPopulation) * oldPopulationRatio)]
    selectedPopulation = selectedPopulation[:101]
    selectedPopulation = sortPopulation(selectedPopulation)
    selectedPopulation = removeFitnessFromPopulation(selectedPopulation)
    return selectedPopulation


# Usage

newPopulation = []
population = initializePopulation(100)
bestIndividual = population[0]

for i in range(70):
    newPopulation = crossOver(population)
    newPopulation = mutate(newPopulation)
    newPopulation = selectNewPopulation(population, newPopulation)

    if getIndevidualFitness(newPopulation[0]) > getIndevidualFitness(bestIndividual) or bestIndividual == "":
        bestIndividual = newPopulation[0]
        print("********************************************************")
        print(bestIndividual)
        print("********************************************************")

    population = newPopulation
