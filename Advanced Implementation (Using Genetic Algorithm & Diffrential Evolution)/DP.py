import pandas as pd

class preparation:
    x = 0
    y = 0
    def __init__(self, x, y):
        preparation.x = x
        preparation.y = y

    # Data Preparation Requirements
    def startNode(x=200,y=100):
        x = preparation.x
        y = preparation.y
        Direct = [x,y]
        return Direct

    def get_cities():
        df = pd.read_excel (r'data.xlsx')
        locations = []
        for i in range(len(df['x'])):
            locations.append(df['city'][i])
        return locations

    def get_coordinates():
        df = pd.read_excel (r'data.xlsx')
        coordinates = []
        for i in range(len(df['x'])):
            coordinates.append([df['x'][i], df['y'][i]])    
        return coordinates

    def create_dictionary():
        cities = preparation.get_cities()
        coordinates = preparation.get_coordinates()
        map = {}
        map["Start"] = preparation.startNode()
        for i in range(len(cities)):
            map[cities[i]] = coordinates[i]
        return map

    def calc_distance(x1, y1, x2, y2):
        return ( ((x2 - x1 )**2) + ((y2-y1)**2) )**0.5

    def calc_cost(population):
        dict = preparation.create_dictionary()
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

                    if j == 0 or j == len(x)-1:
                        x1 = dict['Start'][0]
                        y1 = dict['Start'][1]
                        x2 = dict[x[j]][0]
                        y2 = dict[x[j]][1]
                        dist = preparation.calc_distance(x1, y1, x2, y2)
                        sum += dist
                        continue

                    x1 = dict[x[j]][0]
                    y1 = dict[x[j]][1]
                    x2 = dict[x[j-1]][0]
                    y2 = dict[x[j-1]][1]
                    dist = preparation.calc_distance(x1, y1, x2, y2)
                    sum += dist

            totalCost.append(int(sum) * cost)
            sum = 0
        return totalCost

    def calc_fitness(population, target=30000):
        fit = []

        total = preparation.calc_cost(population)
        for x in total:
            fit.append(target - x)
        return fit

    def merge(list):
        newlist = list.copy()
        for i in range(len(list[0])):
            newlist[0][i] += ' ' + str(newlist[1][i])
        del newlist[1]
        newlist = newlist[0]
        return newlist

    def represent(dict):
        fit = []
        ind = []
        for k,v in dict.items():
            fit.append(int(k))
            ind.append(v)

        m = [fit,ind]
        return m