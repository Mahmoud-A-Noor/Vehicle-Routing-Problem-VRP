class selection:
    # Selection Requirements
    def sort(population):
        d = {}
        for i in range(len(population[0])):
            d[str(population[1][i])] = population[0][i]
        d = dict(sorted(d.items(),reverse=True))
        return d

    def filterPopulation(population):
        dict = selection.sort(population)
        populationList = []

        for v in dict.values():
            populationList.append(v)
            
        return populationList

    def createRoullet(population):
        populationList = selection.filterPopulation(population)
        sum = 0
        for j in range(0, len(populationList)):
            sum += 1 / (j + 1)
        return sum