# -*- coding: utf-8 -*-

import random


# 'MAX_GENERATIONS' Número máximo de generaciones a la que el algoritmo seguirá
# seguirá iterando si no encuentra un individuo con un fitness óptimo.
MAX_GENERATIONS = 1000

# 'MAX_GENERATIONS' Número predeteminado de la población
POPULATION_SIZE = 50

# 'QUEENS_SIZE' Se puede hacer de n-reínas
QUEENS_SIZE = 8


class Genetic_Operator(object):
    # 'MUTATION_PROBABLITY_FACTOR' Factor de probabilidad de la mutación.
    MUTATION_PROBABLITY_FACTOR = 0.02

    @staticmethod
    def recombination(individual1, individual2, individual_size):
        r = random.randint(0, individual_size-1)
        new_board = individual1.board[0:r] + individual2.board[r:individual_size]
        return Individual(individual_size, new_board)

    @staticmethod
    def mutate(individual, individual_size):
        if random.random() < Genetic_Operator.MUTATION_PROBABLITY_FACTOR:
            a = random.randint(1, individual_size)
            i = random.randint(0, individual_size-1)
            new_board = individual.board
            new_board[i] = a

            return Individual(individual_size, new_board)
    
        return individual


class Individual(object):

    def __init__(self, size, board=None):
        if board is None:
            self.board = [random.randint(1,size) for _ in range(size)]
        else:
            self.board = board

        self.max_fitness = size * (size -1)
        self.fitness = self.get_fitness()

    def get_fitness(self):
        n = len(self.board)
        horizontal_clashes, diagonal_clashes = 0, 0

        # Horizontal
        for x in self.board:
            horizontal_clashes += self.board.count(x) - 1

        # Diagonales
        for i in range(n):
            for j in range(n):
                if i < j:
                    if self.board[i] + abs(i-j) == self.board[j]:
                        diagonal_clashes += 1
                elif i > j:
                    if self.board[j] - abs(i-j) == self.board[i]:
                        diagonal_clashes += 1

        return self.max_fitness - (horizontal_clashes + diagonal_clashes)

    def probability(self):
        return self.fitness / self.max_fitness

    @staticmethod
    def optimum_fitness(board_size):
        return board_size * (board_size - 1)


class Population(object):

    def __init__(self, population_size, individual_size, population=None):
        if population is None:
            self.population = [Individual(individual_size) for _ in range(population_size)]
        else:
            self.population = population

    def roulette_selection(self):
        n = len(self.population)
        return self.population[random.randint(0, n-1)]

    def get_optimum_individual(self):
        return max(self.population, key=lambda x: x.fitness)


if __name__ == '__main__':
    population = Population(POPULATION_SIZE, QUEENS_SIZE)
    generation = 0

    optimum_fitness = Individual.optimum_fitness(QUEENS_SIZE)
    solution = None

    print('Fitness óptima = ', optimum_fitness)

    while generation <= MAX_GENERATIONS:

        current_optimum_individual = population.get_optimum_individual()

        if generation % 50 == 0:
            print('{}, generacion={}, fitness={}'
                        .format(current_optimum_individual.board, generation,current_optimum_individual.fitness))

        if optimum_fitness == current_optimum_individual.fitness:
            solution = current_optimum_individual
            break

        new_population = Population(POPULATION_SIZE, QUEENS_SIZE, [current_optimum_individual])

        while len(new_population.population) < POPULATION_SIZE:
            individual1 = population.roulette_selection()
            individual2 = population.roulette_selection()
            # Verificar que sí sean diferentes.
            while individual1 != individual2:
                individual2 = population.roulette_selection()

            child = Genetic_Operator.recombination(individual1, individual2, QUEENS_SIZE)

            child = Genetic_Operator.mutate(child, QUEENS_SIZE)
            new_population.population.append(child)

        population = new_population
        generation += 1

    if solution is None:
        print('No se encontró una solución pero se encontró un buen candidato :(')
        print(population.get_optimum_individual().board)
    else:
        print('Se encontró una solución :D en la generación ', generation)
        print(solution.board)
