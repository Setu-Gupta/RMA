import matplotlib.pyplot as plt
import numpy as np
import sys

if len(sys.argv) <= 1:
    print("Usage: The first argument is the results file")
    print("Usage: The second argument is the ratio of branches and other instructions")

names = []
values = []
with open(sys.argv[1], 'r') as results:
    for line in results.readlines():
        name, value = line.split(':')
        name = name.strip().split("MPKI for ")[-1].replace("with", "with\n")
        value = float(value.strip()) * float(sys.argv[2])
        names.append(name)
        values.append(value)

print(names)
print(values)

plt.title("Misses per kilo instructions (MPKI) for different branch predictors")
plt.xlabel("MPKI")
plt.ylabel("Configurations")
plt.barh(np.arange(len(names)), values)
plt.yticks(np.arange(len(names)), labels = names)
plt.show()
