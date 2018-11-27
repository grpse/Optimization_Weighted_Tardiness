import math
import random
import sys
import re

def sigmoid(gamma):
    if gamma < 0:
        return 1 - 1/(1 + math.exp(gamma))
    else:
        return 1/(1 + math.exp(-gamma))

def SA(S, T, C, p, w, d, cooling_factor, neighborhood_length, calculate_solution_value, generate_neighborhood, select_best_neighbor):

    MAX_C = C
    S_current = S
    S_currentV = calculate_solution_value(S, p, w, d)

    while(C > 0 or T > 0):
        N = generate_neighborhood(S, neighborhood_length)
        [S_Nv_best, S_N_best] = select_best_neighbor(N, calculate_solution_value, p, w, d)
        
        delta = S_currentV - S_Nv_best
        minus_delta_over_t = delta / T
        prob_select_worst_solution = 1.0 / math.exp(minus_delta_over_t) # 1 / exp((S - S')/T)
        print(prob_select_worst_solution)

        # min < to find a solution with the minimum tardiness
        if (S_Nv_best < S_currentV):
            S_current = S_N_best
            S_currentV = S_Nv_best
            C = MAX_C
        elif (random.random() >= prob_select_worst_solution):
            S_current = S_N_best
            S_currentV = S_Nv_best
            C = C - 1

        print("C = ", C, "S v = ", S_currentV)

        T = T - T * cooling_factor

    return [S_currentV, S_current]
        

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
            repeated = repeated or (n_permutations[j] == cur_array)

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

def print_help():
    print("You should provide the 6 parameters for this SA to work")
    print("1 - instance length {40, 50, 100}")
    print("2 - random seed (number)")
    print("3 - initial temperature (float)")
    print("4 - max number of iterations without improve (int)")
    print("5 - cooling factor (float percentage [0; 1])")
    print("6 - neighborhood size (int, DONT DO THIS TOO HIGH)")

if len(sys.argv) < 7:
    print(sys.argv)
    print_help()
    sys.exit(-1)

instance_length = int(sys.argv[1])
randoness_seed = float(sys.argv[2])
temperature = float(sys.argv[3])
max_number_of_iterations_without_improved_solution = int(sys.argv[4])
cooling_factor = max(min(float(sys.argv[5]), 1.0), 0.0)
neighborhood_length = int(sys.argv[6])
[p, w, d] = read_instances(instance_length)

# set seed
random.seed(randoness_seed)

# initial solution is an order 1..instance length
# S = [i for i in range(instance_length)]
# SA(S, temperature, max_number_of_iterations_without_improved_solution, p, w, d, cooling_factor, neighborhood_length, objective_function_value_calculation, generate_neighborhood, select_best_neighbor)

# testing  [5, 2, 3, 1, 6, 4]
solution = [4, 1, 2, 0, 5, 3]
p = [3, 1, 1, 5, 1, 5]
w = [3, 5, 1, 1, 4, 4]
d = [1, 5, 3, 1, 3, 1]

# output should print 70
# print(objective_function_value_calculation(solution, p, w, d))
[best_solution, best_solution_schedule] = SA(solution, temperature, max_number_of_iterations_without_improved_solution, p, w, d, cooling_factor, neighborhood_length, objective_function_value_calculation, generate_neighborhood, select_best_neighbor)
print(best_solution)