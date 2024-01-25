import matplotlib
import numpy as np
import matplotlib.pyplot as plt

"""
{'735386': 6598, '386925': 3402}
{'799024': 2307, '364428': 6740, '801449': 953}
{'248218': 4533, '811261': 2560, '621471': 1625, '694817': 1282}
{'958883': 893, '629242': 3709, '858846': 3089, '594252': 814, '456300': 1495}
{'275154': 1710, '965412': 2354, '589207': 1864, '465655': 3162, '678576': 701, '554001': 209}
"""

values = [[6598, 3402], [2307, 6740, 953], [4533, 2560, 1625, 1282], [893, 3709, 3089, 814, 1495], [1710, 2354, 1864, 3162, 701, 209]]
# values = [[2554, 7446], [4128, 2405, 3467], [4251, 2998, 1521, 1230], [1478, 1983, 3496, 1988, 1055], [1994, 2848, 2047, 764, 1732, 615]]

# Plot avg of each group vs number of elements in group and mark each point in the line
plt.plot([2, 3, 4, 5, 6], 
                       [np.average(values[0]), np.average(values[1]), np.average(values[2]), 
                        np.average(values[3]), np.average(values[4])], label='Average', marker='o'
                        )

# Plot standard deviation of each group vs number of elements in group
plt.plot([2, 3, 4, 5, 6], 
                       [np.std(values[0]), np.std(values[1]), np.std(values[2]), 
                        np.std(values[3]), np.std(values[4])], label = 'Standard Deviation', marker='o'
                        )

# add labels
plt.xlabel('Number of Servers')
plt.ylabel('Load')
plt.legend()

plt.savefig('A-4_plot.png')