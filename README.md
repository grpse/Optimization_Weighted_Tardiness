# Weighted Tardiness
- Weighted job scheduling

## Number of instances for each file {40, 50, 100}
- 125

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

|Job    | Time before       | Time after        | Tardiness | Cost      |
|-------|-------------------|-------------------|-----------|-----------|
|5      | 0                 | 1                 | 0         | 0         |
|2      | 1                 | 2                 | 0         | 0         |
|3      | 2                 | 3                 | 0         | 0         |
|1      | 3                 | 6                 | 5         | 15        |
|6      | 6                 | 11                | 10        | 40        |
|4      | 11                | 16                | 15        | 15        |
