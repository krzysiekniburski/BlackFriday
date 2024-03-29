import random
import pymysql as sql


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

    def new_empty_chromosome(self):
        self._genes = []
        i = 0
        while i < POPULATION_SIZE:
            self._genes.append(0)
            i += 1

    def set_genes(self, genes):
        self._genes = genes

    def get_genes(self):
        return self._genes

    def calc_fitness(self):
        self._fitness = 0
        for i in range(self._genes.__len__()):
            if self._genes[i] == 1:
                self.total_vol += test_weights[i]
                self.total_price += test_prices[i]
                self._fitness += test_prices[i]

            if self.total_vol > MAX_MASS:
                self._fitness = 0
                #self.total_vol -= test_weights[i]
                #self.total_price -= test_prices[i]
                #self._fitness -= test_weights[i]


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
        while i < 200:
            self._chromosomes.append(Chromosome())
            i += 1

    def get_chromosomes(self):
        return self._chromosomes


class GeneticAlgorithm:

    @staticmethod
    def evolve(pop):
        best1 = pop.get_chromosomes()[0]
        best2 = pop.get_chromosomes()[1]

        chromosome1 = Chromosome()
        chromosome1.new_empty_chromosome()
        chromosome1.set_genes(best1.get_genes()[:])

        chromosome2 = Chromosome()
        chromosome2.new_empty_chromosome()
        chromosome2.set_genes(best2.get_genes()[:])

        GeneticAlgorithm.crossover(pop, chromosome1, chromosome2)

        return pop

    @staticmethod
    def crossover(pop, chromosome1, chromosome2):

        crossover_point = random.randint(1, POPULATION_SIZE - 1)

        for i in range(0, crossover_point):
            tmp = chromosome1.get_genes()[i]
            chromosome1.get_genes()[i] = chromosome2.get_genes()[i]
            chromosome2.get_genes()[i] = tmp

        if random.random() % 7 < 0.1:
            GeneticAlgorithm.mutate(pop, chromosome1, chromosome2)
        else:
            GeneticAlgorithm.get_fittest_and_replace(pop, chromosome1, chromosome2)

    @staticmethod
    def mutate(pop, ch1, ch2):
        random_point1 = random.randint(0, POPULATION_SIZE - 1)

        if ch1.get_genes()[random_point1] == 1:
            ch1.get_genes()[random_point1] = 0
        else:
            ch1.get_genes()[random_point1] = 1

        random_point2 = random.randint(0, POPULATION_SIZE - 1)

        if ch2.get_genes()[random_point2] == 1:
            ch2.get_genes()[random_point2] = 0
        else:
            ch2.get_genes()[random_point2] = 1

        GeneticAlgorithm.get_fittest_and_replace(pop, ch1, ch2)

    @staticmethod
    def get_fittest_and_replace(pop, off1, off2):

        off1.calc_fitness()
        off2.calc_fitness()

        if off1.get_fitness() > off2.get_fitness():
            pop.get_chromosomes()[POPULATION_SIZE - 1] = off1
        else:
            pop.get_chromosomes()[POPULATION_SIZE - 1] = off2


test_names = []
test_prices = []
test_weights = []

conn = sql.Connect(host='localhost', unix_socket='', user='root', passwd='', db='agd')
cursor = conn.cursor()

stat = 'SELECT * FROM stuff'

cursor.execute(stat)

lista = list(cursor.fetchall())

for row in lista:
    test_names.append(row[1])
    test_prices.append(row[2])
    test_weights.append(row[3])

# More random numbers
# fake = Faker()
# name = []
# test_prices = []
# test_weights = []
# for i in range(0, 10):
#     name.append(fake.first_name())
#     test_prices.append(random.randint(1, 10))
#     test_weights.append(random.randint(1, 15))

#test_prices = [21, 5, 8, 12]
#test_weights = [7, 12, 6, 8]

# parameters
POPULATION_SIZE = 10
MAX_MASS = 100
population = Population(POPULATION_SIZE)


def calc_fitness_pop(pop):
    for x in pop.get_chromosomes():
        x.calc_fitness()


def print_population(pop, gen_num):
    print('----------------------------------------------------------------------------')
    print('Generation num ', gen_num)
    print('----------------------------------------------------------------------------')
    i = 0
    for x in pop.get_chromosomes():
        # x.calc_fitness()
        print(test_prices)
        print(test_weights)
        print('Chromosome: ', i, ":", x, " Fitness ", x.get_fitness())
        print("Volume ", x.get_total_vol(), "Price", x.get_total_prices())
        i += 1


def print_best_score(pop):
    best = pop.get_chromosomes()[0]
    print('----------------------------------------------------------------------------')
    print('Best score: ')
    print('Chromosome: ', best, "Fitness: ", best.get_fitness())
    print('Total volume: ', best.get_total_vol(), "Total price: ", best.get_total_prices())
    print('----------------------------------------------------------------------------')


calc_fitness_pop(population)
population.get_chromosomes().sort(key=lambda x: x.get_fitness(), reverse=True)
print_population(population, 0)
gen_number = 1
GeneticAlgorithm.evolve(population)
population.get_chromosomes().sort(key=lambda x: x.get_fitness(), reverse=True)
print_population(population, 1)


while population.get_chromosomes()[0].get_fitness() != 0:
#for k in range(50):
    population = GeneticAlgorithm.evolve(population)
    population.get_chromosomes().sort(key=lambda x: x.get_fitness(), reverse=True)
    print_population(population, gen_number)
    gen_number += 1

print_best_score(population)

# print("Tablice name, test_prices and test_weights:")
# #print("names: ",name)
# print("Prices: ",test_prices)
# print("Weights:", test_weights)
