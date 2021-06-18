# Computing Krippendorff 's Alpha-Reliability

This module follows the instructions in the paper
[Krippendorff, K. (2011). Computing Krippendorff's Alpha-Reliability](http://repository.upenn.edu/asc_papers/43)
to compute reliability coefficient Krippendorff’s alpha on a dataset with
- nominal data, 
- any number of observers, 
- missing data.

For example, for a 4 observers-by-12 units reliability data matrix

| Units u:   | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|------------|---|---|---|---|---|---|---|---|---|----|----|----|
| Observer A | 1 | 2 | 3 | 3 | 2 | 1 | 4 | 1 | 2 | .  | .  | .  |
| Observer B | 1 | 2 | 3 | 3 | 2 | 2 | 4 | 1 | 2 | 5  | .  | 3  |
| Observer C | . | 3 | 3 | 3 | 2 | 3 | 4 | 2 | 2 | 5  | 1  | .  |
| Observer D | 1 | 2 | 3 | 3 | 2 | 4 | 4 | 1 | 2 | 5  | 1  | .  |

we can find the Krippendorff's Alpha using the module in this repository:

```python
from krippendorff import DataMatrix

observers = [
    # Observer A
    {'1': 1, '3': 3, '2': 2, '5': 2, '4': 3, '7': 4, '6': 1, '9': 2, '8': 1, '11': None, '10': None, '12': None},
    # Observer B
    {'1': 1, '3': 3, '2': 2, '5': 2, '4': 3, '7': 4, '6': 2, '9': 2, '8': 1, '11': None, '10': 5, '12': 3},
    # Observer C
    {'1': None, '3': 3, '2': 3, '5': 2, '4': 3, '7': 4, '6': 3, '9': 2, '8': 2, '11': 1, '10': 5, '12': None},
    # Observer D
    {'1': 1, '3': 3, '2': 2, '5': 2, '4': 3, '7': 4, '6': 4, '9': 2, '8': 1, '11': 1, '10': 5, '12': None},
]

dm = DataMatrix(observers)
print(dm)
# Outputs:
# 	|	1	2	3	4	5	|
# ――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――
# 1	|	7	4/3	1/3	1/3	0	|	9
# 2	|	4/3	10	4/3	1/3	0	|	13
# 3	|	1/3	4/3	8	1/3	0	|	10
# 4	|	1/3	1/3	1/3	4	0	|	5
# 5	|	0	0	0	0	3	|	3
# ――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――
# 	|	9	13	10	5	3	|	40

alpha = dm.compute_krippendorff_alpha()
print(f'alpha = {alpha}')          # alpha = 113/152
print(f'alpha ~= {float(alpha)}')  # alpha ~= 0.743421052631579
```
