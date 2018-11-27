import math
import random
import sys
import re
import time
import os
import signal

def SA(S, T, C, p, w, d, cooling_factor, neighborhood_length, calculate_solution_value, generate_neighborhood, select_best_neighbor):

    MAX_C = C
    S_current = S
    S_currentV = calculate_solution_value(S, p, w, d)

    S_best = S_current[:]
    S_bestV = S_currentV

    print('best:', S_bestV, S_best, T, C)
    hang_signal = False
    def signal_handler(sig, frame):
        hang_signal = True

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGUSR1, signal_handler)
    signal.siginterrupt(signal.SIGUSR1, False)

    while(C > 0 and T > 0 and not hang_signal):
        # Neighborhood
        N = generate_neighborhood(S, neighborhood_length)
        
        # For each 
        for i in range(len(N)):
            
            if hang_signal:
                break

            SN = N[i]
            SNv = calculate_solution_value(SN, p, w, d)

            delta = math.fabs(SNv - S_currentV)
            minus_delta_over_t = delta / T
            prob_select_worst_solution = math.exp(-minus_delta_over_t)

            # min < to find a solution with the minimum tardiness
            if SNv < S_currentV:
                S_current = SN[:]
                S_currentV = SNv
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

        T = T - T * cooling_factor

    return [S_bestV, S_best]
        

def select_best_neighbor(N, calculate_solution_value, p, w, d):
    """
    Select the best neighbor from neighborhood
    """
    bestNi = 0
    bestNv = calculate_solution_value(N[0], p, w, d)
    for i in range(1, len(N)):
        current_Nv = calculate_solution_value(N[i], p, w, d)

        if (current_Nv > bestNv):
            bestNi = i
            bestNv = current_Nv

    return [bestNv, N[bestNi]]

def generate_n_permutations(elements, n=1):
    
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

def generate_neighborhood(solution, neighborhood_length):
    """
    Generate a neighborhood for solution
    """
    return generate_n_permutations(solution, neighborhood_length)

def objective_function_value_calculation(solution, p, w, d):
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

def save_result(params, best_solution_value, execution_time):
    file = open('results.csv', 'a+')
    header = file.readline()
    if len(header) == 0:
        file.write("file name,instance length,random seed,initial temperture,max iterations without improvement,cooling factor,neighborhood size,test case number,execution time (seconds),best solution value\n")
    file.close()

    file = open('results.csv', 'a+')
    line = "wt" + str(instance_length) + ".txt,"
    for i in range(len(params)):
        line = line + str(params[i]) + ","

    line = line + str(execution_time) + "," + str(best_solution_value) + "\n"

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
print("initial solution:", objective_function_value_calculation(S, p, w, d))

time_before_execution = time.time()
[best_solution, best_solution_schedule] = SA(S, temperature, max_number_of_iterations_without_improved_solution, p, w, d, cooling_factor, neighborhood_length, objective_function_value_calculation, generate_neighborhood, select_best_neighbor)
elapsed_time = time.time() - time_before_execution

print(best_solution)
print(S)
print(best_solution_schedule)

save_result(sys.argv[1:], best_solution, elapsed_time)