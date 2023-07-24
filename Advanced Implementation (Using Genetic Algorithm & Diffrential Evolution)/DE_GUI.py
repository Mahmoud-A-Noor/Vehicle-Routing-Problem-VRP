import math
from random import sample, random
from tkinter import *
import matplotlib.pyplot as plt
from DP import preparation as DP
import pandas as pd


def get_cities():
    df = pd.read_excel(r'data.xlsx')
    cities = {}
    for i in range(len(df)):
        cities[df.iloc[i][0]] = [df.iloc[i][1], df.iloc[i][2]]
    return cities


cities = get_cities()
listOfCities = list(cities.keys())
best = []
generation = []


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
    population = convertPopulation(population, number=True)
    return population


def convertPopulation(population, number=False):
    convertedPopulation = []
    for individual in population:
        individualList = []
        for gene in individual:
            if number:
                individualList.append(ord(gene))
            else:
                individualList.append(chr(gene))
        if not number:
            individualList = ''.join(individualList)
        convertedPopulation.append(individualList)
    return convertedPopulation


def ensure(donor, bound):
    min = bound[0]
    max = bound[1]
    v = []

    for d in donor:
        if d == 32:
            v.append(32)
        else:
            if d < min:
                v.append(min)
            elif d > max:
                v.append(max)
            elif min <= d <= max:
                v.append(d)
    return v


def crossOver(target, donor, r):
    v = []
    for i in range(len(target)):
        rand = random()

        if r <= rand:
            v.append(donor[i])
        else:
            v.append(target[i])

    return v


def calc_distance(x1, y1, x2, y2):
    return (((x2 - x1) ** 2) + ((y2 - y1) ** 2)) ** 0.5


def calc_cost(population):
    dict = cities
    individual = {}
    cost = 2

    c = 0
    for x in population:
        individual[c] = x.split()
        c += 1

    sum = 0
    totalCost = []
    for v in individual.values():

        for x in v:

            for j in range(len(x)):

                if j == 0 or j == len(x) - 1:
                    x1 = dict['Start'][0]
                    y1 = dict['Start'][1]
                    x2 = dict[x[j]][0]
                    y2 = dict[x[j]][1]
                    dist = calc_distance(x1, y1, x2, y2)
                    sum += dist
                    continue

                x1 = dict[x[j]][0]
                y1 = dict[x[j]][1]
                x2 = dict[x[j - 1]][0]
                y2 = dict[x[j - 1]][1]
                dist = calc_distance(x1, y1, x2, y2)
                sum += dist

        totalCost.append(int(sum) * cost)
        sum = 0
    return totalCost


def calc_fitness(population, target=9000):
    fit = []
    total = calc_cost(population)
    for x in total:
        fit.append(target - x)
    return fit


def replaceDuplicates(individual):
    individualList = []
    for gene in individual:
        individualList.append(chr(gene))
    individual = ''.join(individualList)

    cities1 = listOfCities.copy()

    str1 = ""
    for i in individual:
        if i in cities1:
            cities1.remove(i)
            str1 += i
        else:
            if i == " ":
                str1 += " "
            else:
                str1 += "*"

    child1 = ""
    for i in str1:
        if i == "*":
            child1 += cities1[0]
            del cities1[0]
        else:
            child1 += i

    return child1


def select(population, j, target, trial):
    if calc_fitness([replaceDuplicates(target)])[0] > calc_fitness([replaceDuplicates(trial)])[0]:
        population[j] = target
    else:
        population[j] = trial


def mutate(randIndex, population, factor, bound):
    x_1 = population[randIndex[0]]
    x_2 = population[randIndex[1]]
    x_3 = population[randIndex[2]]

    diff = [x2 - x3 for x2, x3 in zip(x_2, x_3)]

    donor = [math.ceil(x1 + factor * diff_i) for x1, diff_i in zip(x_1, diff)]
    donor = ensure(donor, bound)
    return donor

gtarget = 9000
numberOfTrucks = 4
populationSize = 100
xx=0 
yy=0
def evolve(factor=0.5, Generationlimit=10, recombinationFactor=0.7, bound=[65, 90]):
    global truck, entry1, entry2, targetValue, gtarget, numberOfTrucks, populationSize, cities, xx, yy
    cities["Start"] = [float(entry1.get()), float(entry2.get())]
    gtarget = int(targetValue.get())
    numberOfTrucks = int(truck.get())
    populationSize = populationSize

    population = initializePopulation(populationSize, numberOfTrucks)
    bestIndividual = convertPopulation([population[0]])[0]

    for i in range(1, Generationlimit + 1):

        print('Generation #', i, ': ')

        for j in range(len(population)):

            indices = list(range(0, len(population)))
            indices.remove(j)
            xtarget = population[j]
            randIndex = sample(indices, 3)

            donor = mutate(randIndex, population, factor, bound)

            trial = crossOver(xtarget, donor, recombinationFactor)

            select(population, j, xtarget, trial)

            pop = convertPopulation(population)

            for p in pop:
                generation.append(p)
                if calc_fitness(bestIndividual) < calc_fitness(p):
                    bestIndividual = p
                    best.append(bestIndividual)

        print(calc_fitness([bestIndividual])[0], bestIndividual)

    create_map(generation,best)


def GUI():
    global entry1, entry2, truck, targetValue
    window = Tk()
    window.title('VRP')
    window.geometry('400x350')
    window.resizable(False, False)

    Label(window, text="Start Point", fg='blue', font=("Arial", 17)).place(x=160, y=20)

    Label(window, text="X :", font=("bold", 10)).place(x=120, y=70)

    Label(window, text="Y :", font=("bold", 10)).place(x=120, y=120)

    Label(window, text="Number of Trucks:", font=("bold", 10)).place(x=12, y=170)

    Label(window, text="Expected Value :", font=("bold", 10)).place(x=15, y=220)

    entry1 = Entry(window)
    entry1.place(x=150, y=70)

    entry2 = Entry(window)
    entry2.place(x=150, y=120)

    truck = Entry(window)
    truck.place(x=150, y=170)

    targetValue = Entry(window)
    targetValue.place(x=150, y=220)

    Button(window, text='Next', relief="flat", bg='blue', fg='white', font=("bold"), command=evolve).place(x=180, y=260)

    window.mainloop()


def create_line(coordinates, n):
    lineColor = ["red", "blue", "yellow", "green", "black", "brown", "cyan", "magenta"]
    for i in range(len(coordinates) - 1):
        plt.plot([coordinates[i][0], coordinates[i + 1][0]], [coordinates[i][1], coordinates[i + 1][1]],
                 color=lineColor[n])
        plt.pause(0.00001)


def create_map(generations, bestPath):
    m = DP.create_dictionary()
    lineColor = ["red", "blue", "yellow", "green", "black", "brown", "cyan", "magenta"]
    coordinates = []
    coordinates.append(m["Start"])
    c = 1
    n = 0
    for str in generations:

        str += " "
        plt.cla()
        plt.title("Locations", fontsize=20)
        plt.scatter(coordinates[0][0], coordinates[0][1], s=100, color=lineColor[0])
        plt.annotate("Start", (coordinates[0][0], coordinates[0][1] + 10))
        plt.xlabel("X", fontweight='bold')
        plt.ylabel("Y", fontweight='bold')
        for x in str:

            if (x == " "):
                coordinates.append(m["Start"])
                create_line(coordinates, n)
                coordinates = []
                coordinates.append(m["Start"])
                n += 1
                if n == len(lineColor):
                    n = 0
                c = 1
            else:
                coordinates.append(m[x])
                plt.scatter(coordinates[c][0], coordinates[c][1], s=40, color=lineColor[n])
                plt.annotate(x, (coordinates[c][0], coordinates[c][1] + 10))
                c += 1
        plt.pause(1)

    bestPath += " "
    plt.show()
    plt.title("Optimal Solution", fontsize=20)
    plt.scatter(coordinates[0][0], coordinates[0][1], s=100, color=lineColor[0])
    plt.annotate("Start", (coordinates[0][0], coordinates[0][1] + 10))
    plt.xlabel("X", fontweight='bold')
    plt.ylabel("Y", fontweight='bold')

    for z in bestPath:

        if (z == " "):
            coordinates.append(m["Start"])
            create_line(coordinates, n)
            coordinates = []
            coordinates.append(m["Start"])
            n += 1
            if n == len(lineColor):
                n = 0
            c = 1
        else:
            coordinates.append(m[z])
            plt.scatter(coordinates[c][0], coordinates[c][1], s=40, color=lineColor[n])
            plt.annotate(z, (coordinates[c][0], coordinates[c][1] + 10))
            c += 1