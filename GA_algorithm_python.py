import random


# test data


class Chromosome:

    def __init__(self):
        self._genes = []
        self._fitness = 0
        self.total_vol = 0
        self.total_price = 0
        i = 0
        while i < POPULATION_SIZE:
            if random.random() >= 0.5:
                self._genes.append(1)
            else:
                self._genes.append(0)
            i += 1

    def get_genes(self):
        return self._genes

    def calc_fitness(self):
        for i in range(self._genes.__len__()):
            if self._genes[i] == 1:
                self.total_vol += test_weights[i]
                self.total_price += test_prices[i]
                self._fitness += 1
            if self.total_vol > MAX_MASS:
                self.total_vol -= test_weights[i]
                self.total_price -= test_prices[i]
                self._fitness -= 1

            if self._fitness < 0:
                self._fitness = 0

    def get_fitness(self):
        return self._fitness

    def get_total_prices(self):
        return self.total_price

    def get_total_vol(self):
        return self.total_vol

    def __str__(self):
        return self._genes.__str__()


class Population:

    def __init__(self, size):
        self._chromosomes = []
        i = 0
        while i < size:
            self._chromosomes.append(Chromosome())
            i += 1

    def get_chromosomes(self):
        return self._chromosomes


class GeneticAlgorithm:
    """ """
    # TODO: Add evolve, crossover and mutate methods


# test data
test_prices = [100, 50, 200, 799, 650, 150, 185, 299, 399, 350]
test_weights = [1, 3, 5, 6, 10, 7, 2, 4, 3.5, 9]

# parameters
POPULATION_SIZE = 10
MAX_MASS = 20
MUTATION_RATE = 0.25
ELITE_CHROMOSOMES_NUM = 1
TOURNAMENT_SELECTION_SIZE = 4
population = Population(POPULATION_SIZE)


def calc_fitness_pop(pop):
    for x in pop.get_chromosomes():
        x.calc_fitness()


def print_population(pop, gen_num):
    print('Generation num ', gen_num)
    i = 0
    for x in pop.get_chromosomes():
        # x.calc_fitness()
        print('Chromosome: ', i, ":", x, " Fitness ", x.get_fitness())
        print("Volume ", x.get_total_vol(), "Price", x.get_total_prices())
        i += 1


calc_fitness_pop(population)
population.get_chromosomes().sort(key=lambda x: x.get_fitness(), reverse=True)
print_population(population, 0)
gen_number = 1
while population.get_chromosomes()[0].get_fitness() < POPULATION_SIZE:
    population = GeneticAlgorithm.evolve(population)
    calc_fitness_pop(population)
    population.get_chromosomes().sort(key=lambda x: x.get_fitness(), reverse=True)
    print_population(population, gen_number)
    gen_number += 1
