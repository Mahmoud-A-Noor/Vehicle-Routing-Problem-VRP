import math
import numpy as np
import random
import matplotlib.pyplot as plt


class Gene:  # contains the region and (x,y) coordinate of the region
    def __init__(self, region, x, y):
        self.region = region
        self.x = x
        self.y = y


class Chromosome:  # contains the score, solution path and the fitness function
    def __init__(self, chromosome_genes):
        self.genes = chromosome_genes
        self.score = 0

    def __str__(self):
        string = ""
        for i in self.genes:
            string += i.region
        return string

    def __len__(self):
        return len(self.genes)


def initialize_population(n, genes):  # return list of chromosomes (initialize population)   n = size of population
    population = []
    for i in range(n):
        population.append(Chromosome(
            random.sample(genes, len(genes))))  # shuffle the genes and make chromosome then add it to population
    return population


def fitness(chromosome, start):  # set the score of chromosome to the current fitness and return the chromosome (helper function of calculate_fitness)
    chromosome.score = 0
    chromosome.genes.insert(0, start)
    for i in range(len(chromosome.genes) - 1):
        distance = 1 / np.sqrt(np.square(chromosome.genes[i + 1].x - chromosome.genes[i].x) + np.square(
            chromosome.genes[i + 1].y - chromosome.genes[i].y))
        chromosome.score += distance
    del chromosome.genes[0]
    return chromosome


def calculate_fitness(population, start):  # return new list of populations with score set to them
    population_with_score = []
    for chromosome in population:
        population_with_score.append(fitness(chromosome, start))
    return population_with_score


def sort_population(population):  # return a sorted copy of the population  THE HIGHEST SCORE => THE LOWEST SCORE
    return sorted(population, key=lambda x: x.score, reverse=True)


def mutate(chromosomes, probability):  # make mutation on a list of chromosomes
    mutated_chromosomes = []
    for chromosome in chromosomes:
        if probability > np.random.random():
            first = np.random.randint(low=0, high=len(chromosome))
            second = np.random.randint(low=0, high=len(chromosome))
            temp = chromosome.genes[first]
            chromosome.genes[first] = chromosome.genes[second]
            chromosome.genes[second] = temp
            mutated_chromosomes.append(chromosome)
        else:
            mutated_chromosomes.append(chromosome)
    del first, second, temp
    return mutated_chromosomes


def cross_over(population, CrossOverPoint, areas, genes):
    for i in np.arange(start=0, stop=len(population) - 1, step=2):
        chromosome1genes = population[i].genes
        chromosome2genes = population[i + 1].genes

        ##
        # for gene in chromosome1genes:
        #     print(gene.region, end=" > ")
        # print()
        # for gene in chromosome2genes:
        #     print(gene.region, end=" > ")
        ##

        regions = []
        temp1 = []
        for index in range(CrossOverPoint):
            temp1.append(chromosome1genes[index])
        for index in np.arange(start=CrossOverPoint, stop=len(chromosome1genes)):
            temp1.append(chromosome2genes[index])

        for gene in temp1:
            if gene.region in regions:
                regions.append("-1")
            else:
                regions.append(gene.region)

        for index, x in enumerate(areas):
            if x not in regions:
                for index2, gene in enumerate(temp1):
                    if gene.region == "-1":
                        temp1[index2] = genes[index]

        # temp1regions = []
        # for index in range(len(temp1)):
        #     temp1regions.append(temp1[index].region)
        #
        # for region in regions:
        #     counter = 0
        #     for index in range(len(temp1)):
        #         if region == temp1[index].region:
        #             counter += 1
        #     if counter == 2:
        #         for index in range(len(temp1)):
        #             if region == temp1[index].region:
        #                 temp1[index].region = "-1"
        #                 break


        # for ii, region in enumerate(regions):
        #     if region not in temp1regions:
        #         for index in range(len(temp1)):
        #             if temp1[index].region == "-1":
        #                 temp1[index] = genes[ii]
        #                 break

        temp2 = []
        for index in range(CrossOverPoint):
            temp2.append(chromosome2genes[index])
        for index in np.arange(start=CrossOverPoint, stop=len(chromosome1genes)):
            temp2.append(chromosome1genes[index])


        for gene in temp2:
            if gene.region in regions:
                regions.append("-1")
            else:
                regions.append(gene.region)

        for index, x in enumerate(areas):
            if x not in regions:
                for index2, gene in temp2:
                    if gene.region == "-1":
                        temp2[index2] = genes[index]

        # for region in regions:
        #     counter = 0
        #     for index in range(len(temp2)):
        #         if region == temp2[index].region:
        #             counter += 1
        #     if counter == 2 or counter == 0:
        #         for index in range(len(temp2)):
        #             if region == temp2[index].region:
        #                 temp2[index].region = "-1"
        #                 break
        # temp2regions = []
        # for index in range(len(temp2)):
        #     temp2regions.append(temp2[index].region)
        #
        # for ii, region in enumerate(regions):
        #     if region not in temp2regions:
        #         for index in range(len(temp2)):
        #             if temp2[index].region == "-1":
        #                 temp2[index] = genes[ii]
        #                 break

        population[i].genes = temp1
        population[i + 1].genes = temp2
        ##
        # for gene in population[i].genes:
        #     print(gene.region, end=" > ")
        # print()
        # for gene in population[i + 1].genes:
        #     print(gene.region, end=" > ")
        ##
    return population


# convergence

def main():
    genes = [
        Gene("A", 1, 1),
        Gene("B", 5, 2),
        Gene("C", 2, 5),
        Gene("D", 4, 0),
        Gene("E", 6, 3),
        Gene("F", 4.5, 6),
        Gene("G", 3, 4),
    ]
    start = Gene("E", 6, 3)

    for index, i in enumerate(genes):
        if i.region == start.region:
            del genes[index]
            break
    regions = []
    for i in genes:
        regions.append(i.region)

    population = initialize_population(10, genes)

    population = calculate_fitness(population, start)
    population = sort_population(population)

    mutated_population = mutate(population, 0.7)

    for i in mutated_population:
        for region in i.genes:
            print(region.region, end=" > ")
        print(i.score)
    print()

    new_generation = cross_over(mutated_population, math.ceil(len(mutated_population[0]) / 2.0), regions, genes)
    new_generation = calculate_fitness(new_generation, start)
    new_generation = sort_population(new_generation)

    for i in new_generation:
        for region in i.genes:
            print(region.region, end=" > ")
        print(i.score)
    print()
    # population = mutate(population,0.7)
    # for i in population:
    #     for region in i.genes:
    #         print(region.region, end=" > ")
    #     print(i.fitness())
    # print()

    # x = []
    # for i in genes:
    #     x.append(i.x)
    #
    # y = []
    # for i in genes:
    #     y.append(i.y)
    # plt.scatter(x, y)
    # plt.show()


if __name__ == "__main__":
    main()
