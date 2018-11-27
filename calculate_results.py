import csv
import math
import sys
csv_file_path = 'results.csv'

results = dict()

with open(csv_file_path, 'r') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')
    first = True
    for row in csv_reader:
        if first:
            first = False
            continue

        key = row[0] + row[7]
        if key in results:
            results[key].append(row)
        else:
            results[key] = [row]


# S percentual
BKS = dict()
BKS["wt40.txt9"] = 16225
BKS["wt40.txt28"] = 15
BKS["wt40.txt105"] = 0.00000000000000001
BKS["wt50.txt41"] = 71111
BKS["wt50.txt77"] = 0.00000000000000001
BKS["wt50.txt119"] = 106043
BKS["wt100.txt26"] = 8
BKS["wt100.txt30"] = 50
BKS["wt100.txt46"] = 829828
BKS["wt100.txt80"] = 0.00000000000000001


key = "wt40.tx9"

for key in results.keys():
    
    # diff percentual
    my_best_solution = sys.maxint
    for i in range(len(results[key])):
        instance = results[key][i]
        solution_value = float(instance[9])

        if solution_value < my_best_solution:
            my_best_solution = solution_value

    percentual_deviation = 100.0 * ((my_best_solution - BKS[key])/BKS[key])
    #print(key, percentual_deviation)
    #print('best solution for ', key,':', my_best_solution)

    mean = 0
    for i in range(len(results[key])):
        instance = results[key][i]
        solution_value = float(instance[9])
        mean = mean + solution_value

    mean = mean / 5

    std_dev = 0
    for i in range(len(results[key])):
        instance = results[key][i]
        solution_value = float(instance[9])

        std_dev = std_dev + math.pow(solution_value - mean, 2)


    std_dev = math.sqrt(std_dev/5)

    mean = 0
    for i in range(len(results[key])):
        instance = results[key][i]
        solution_value = float(instance[10])
        mean = mean + solution_value

    mean = mean / 5

    print(key, mean)









    