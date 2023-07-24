from random import randint

class evolution:
    
    # Evolution Requirements
    def getCities(parents):
        cities = list(parents[0][0].replace(" ",""))
        return cities

    def filterCities(child , cities):
        copy = cities.copy()
        for x in cities:
            if x in child:
                copy.remove(x)
        return copy

    def reflect(str):
        s = str.split()
        length = len(s)

        r1 = randint(0,int((length-1)/2))
        r2 = randint(int(length/2),length-1)

        s1 = s[r1]
        s2 = s[r2]

        s1 = s1[::-1]
        s2 = s2[::-1]

        s[r1] = s1
        s[r2] = s2

        individual = []
        for i in range(length-1):
            individual.append(s[i])
            individual.append(' ')

        individual.append(s[length-1])

        return ''.join(individual)

    def swap(str,r1,r2):
        l = list(str)
        c1 = str[r1]
        c2 = str[r2]
        if c1==" ":
            r1 += 1
            c1 = str[r1]
        if c2==" ":
            r2 += 1
            c2 = str[r2]
        l[r1] = c2
        l[r2] = c1
        return ''.join(l)

    def includeParents(parents):
        population = []

        for i in range(len(parents)):
            for j in range(2):
                population.append(parents[i][j])

        return population

    def includeRands(pop , rands):
        for x in rands:
            pop.append(x)
        return pop

    def testPopulation(pop,cities):
        f = 0
        for x in pop:
            for i in range(len(cities)-1):
                if x.count(cities[i]) != 1:
                    f += 1
                    print(x,' ',cities[i])
        print(f'{f} faliure')