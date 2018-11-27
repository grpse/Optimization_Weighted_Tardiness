import math
import random
import sys
import re
import time
import os
import signal

class SimulatedAnnealing:

    def __init__(self, data, neighborhood_size):
        self.data = data
        self.neighborhood_size = neighborhood_size
        self.hang_signal = False
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGUSR1, self.signal_handler)
        signal.siginterrupt(signal.SIGUSR1, False)
    
    # inner definition for hang signal (CTRL+C) to cancel execution, but return the best solution found
    def signal_handler(self, sig, frame):
        self.hang_signal = True

    def improve_solution(self, S, T, C, cooling_factor):
        """
        given a initial solution S, initial temperature T, max iterations without improvement C, the vectors of processing time, weight
        and ideal due date, the cooling factor, the neighborhood size 
        """
        # initial solution value calculation
        S0v = self.objective_function_value_calculation(S)

        # initialize current solution copy
        S_current = S
        S_currentV = self.objective_function_value_calculation(S)

        # select the best solution as the initial solution
        S_best = S_current[:]
        S_bestV = S_currentV

        print('initial solution:', S_bestV, S_best, T, C)

        while(C > 0 and T > 0 and not self.hang_signal):
            # Neighborhood
            N = self.generate_neighborhood(S)
            
            # For each generated neighbor
            for i in range(len(N)):
                
                if self.hang_signal:
                    break

                # calculate neighbor solution value
                SN = N[i]
                SNv = self.objective_function_value_calculation(SN)

                # calculate the probability to select worst solution
                delta = math.fabs(SNv - S_currentV)
                minus_delta_over_t = delta / T
                prob_select_worst_solution = math.exp(-minus_delta_over_t)

                # min < to find a solution with the minimum tardiness
                if SNv < S_currentV:
                    S_current = SN[:]
                    S_currentV = SNv
                # selection of worst solution
                elif (prob_select_worst_solution > random.random()):
                    S_current = SN[:]
                    S_currentV = SNv
                    C = C - 1
                else:
                    C = C - 1

                # save the best results
                if S_currentV < S_bestV:
                    S_best = SN[:]
                    S_bestV = SNv
                    print(prob_select_worst_solution)
                    print('improved:', S_bestV, S_best, T, C)

            # decrease cooling factor
            T = T - T * cooling_factor
        # return a tuple of best solution value and it's schedule
        return [S0v, S_bestV, S_best]        

    def generate_neighborhood(self, solution):
        """
        Generate a neighborhood for solution
        """
        return self.generate_n_permutations(solution, self.neighborhood_size)

    def generate_n_permutations(self, elements, n=1):
        """
        generate n randomly and non-repeated permutations of a list.
        DONT ALLOW RUNNING WITH N > len(element)! ITS NOT POSSIBLE
        """
        # dont ultrapass max number of permutations
        max_permutations = math.factorial(len(elements))
        if n >= max_permutations:
            n = max_permutations - 1

        n_permutations = []
        cur_array = elements[:]
        while n > 0:
            repeated = False
            random.shuffle(cur_array)

            for j in range(len(n_permutations)):
                repeated = repeated or (n_permutations[j] == cur_array) or (n_permutations[j] == elements)

            if repeated:
                continue
            else:
                n_permutations.append(cur_array[:])
                n = n - 1
        
        return n_permutations

    def objective_function_value_calculation(self, solution):
        """
        Calculate the weighted tardiness
        """
        p = self.data[0]
        w = self.data[1]
        d = self.data[2]
        c = [0] * len(solution)
        t = [0] * len(solution)
        wt = [0] * len(solution)
        for i in range(len(solution)):
            j_minus_1 = solution[max(i-1, 0)]
            j = solution[i]
            c[j] = c[j_minus_1] + p[j]
            t[j] = max(c[j] - d[j], 0)
            wt[j] = w[j] * t[j]

        return sum(wt)

def read_instances(instance_length):
    """
    Reads an instance from stdin
    """
    p = [0] * instance_length 
    w = [0] * instance_length
    d = [0] * instance_length

    # Pj
    for i in range(instance_length):
        p[i] = input()

    # Wj
    for i in range(instance_length):
        w[i] = input()

    # Dj
    for i in range(instance_length):
        d[i] = input()

    return [p, w, d]

def save_result(params, initial_solution_value, best_solution_value, execution_time):
    """
    Saves the result of a instance run to 'results.csv' file
    """

    file = open('results.csv', 'a+')
    header = file.readline()
    if len(header) == 0:
        file.write("file name,instance length,random seed,initial temperture,max iterations without improvement,cooling factor,neighborhood size,test case number,execution time (seconds),best solution value, initial solution value\n")
    file.close()

    file = open('results.csv', 'a+')
    line = "wt" + str(instance_length) + ".txt,"
    for i in range(len(params)):
        line = line + str(params[i]) + ","

    line = line + str(execution_time) + "," + str(best_solution_value) + "," + str(initial_solution_value) + "\n"

    file.write(line)
    file.close()


def print_help():
    print("You should provide the 7 parameters for this SA to work")
    print("1 - instance length {40, 50, 100}")
    print("2 - random seed (number)")
    print("3 - initial temperature (float)")
    print("4 - max number of iterations without improve (int)")
    print("5 - cooling factor (float percentage [0; 1])")
    print("6 - neighborhood size (int)")
    print("7 - test case number")

if len(sys.argv) < 8:
    print(sys.argv)
    print_help()
    sys.exit(-1)

instance_length = int(sys.argv[1])
randoness_seed = float(sys.argv[2])
temperature = float(sys.argv[3])
max_number_of_iterations_without_improved_solution = int(sys.argv[4])
cooling_factor = max(min(float(sys.argv[5]), 1.0), 0.0)
neighborhood_length = int(sys.argv[6])
instance_index = int(sys.argv[7])
[p, w, d] = read_instances(instance_length)

# set seed
random.seed(randoness_seed)

# initial solution is an order 1..instance length shuffled
S = range(instance_length)
random.shuffle(S)

time_before_execution = time.time()

sa = SimulatedAnnealing([p, w, d], neighborhood_length)
[initial_solution_value, best_solution, best_solution_schedule] = sa.improve_solution(S, temperature, max_number_of_iterations_without_improved_solution, cooling_factor)#SA(S, temperature, max_number_of_iterations_without_improved_solution, p, w, d, cooling_factor, neighborhood_length, objective_function_value_calculation, generate_neighborhood, select_best_neighbor)
elapsed_time = time.time() - time_before_execution

print(best_solution)
print(S)
print(best_solution_schedule)

save_result(sys.argv[1:], initial_solution_value, best_solution, elapsed_time)