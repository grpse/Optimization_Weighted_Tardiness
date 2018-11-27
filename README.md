# Weighted Tardiness
- Weighted job scheduling

## For each file {40, 50, 100}
- number of instances: 125
- configuration n {40, 50, 100}
    - 1 * n = p(j)
    - 2 * n = w(j)
    - 3 * n = d(j)
    - 4 * n = p(j+1)
    - ...

## Optimal solutions in files
- wt40opt.txt
    - line 124
- wt50opt.txt
    - line 115
- The other instances and lines on opt and best files are the best known solutions at this time (BKS - 24/11/2018)
- The best solutions for wtbest100a.txt are the 

## Unsolved instances
- wt40.txt
    - 19
- wt50.txt
    - 11, 12, 14, 19, 36, 44, 66, 87, 88 and 111

## Simple example

### Instance
|Job j    |1 |2 |3 |4 |5 |6 |
|---------|--|--|--|--|--|--|
|p(j)     |3 |1 |1 |5 |1 |5 |
|w(j)     |3 |5 |1 |1 |4 |4 |
|d(j)     |1 |5 |3 |1 |3 |1 |


### Possible scheduling

|Job    | Time before       | Time after        | T = max(c - d, 0) | Weighted T.|
|-------|-------------------|-------------------|-------------------|------------|
|5      | 0                 | 1                 | 0                 | 0          |
|2      | 1                 | 2                 | 0                 | 0          |
|3      | 2                 | 3                 | 0                 | 0          |
|1      | 3                 | 6                 | 5                 | 15         |
|6      | 6                 | 11                | 10                | 40         |
|4      | 11                | 16                | 15                | 15         |

# Math Formulation

## Values explanation:
- Y<sub>sj</sub> = tardiness for schedule on position s for job j
- X<sub>sj</sub> = job j was executed on schedule position s

## Values explanation:
    p(j) = processing time for a job j
    w(j) = weight for a job j
    d(j) = due date ideal for job j
    c(j) = sum (up to job j) of processing time
    t(j) = { max(c(j) - d(j), 0) }
    c(s) = !GUESS -> sum of processing time for schedule s
    t(s) = !GUESS -> sum { j in J } t(s) = { max(c(s) - d(j), 0) }

# min &sum; <sub>j &isin; J</sub> &sum; <sub>s &isin; S</sub> w<sub>j</sub>Y<sub>sj</sub>

## Explanation for numbers:

1)  
2) Attach only one schedule position for each job
3) Attach only one job for each schedule position
4) 
5)
6)
7)
8)

# Meta-Heuristic

## Simulated Annealing

### Params
    S = Initial solution
    T = Initial temperture
    C = Max iterations without improvement
    F = Cooling factor for reducing temperture along iterations

### Stop criteria
- When max number of iterations are reached or temperture is 0

