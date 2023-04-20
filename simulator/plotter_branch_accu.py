import matplotlib.pyplot as plt
import numpy as np
import sys

if len(sys.argv) <= 1:
    print("Usage: The first argument is the results file")

names = []
values = []
with open(sys.argv[1], 'r') as results:
    for line in results.readlines():
        name, value = line.split(':')
        name = name.strip().split("MPKI for ")[-1].replace("with", "with\n")
        value = 100 - ((1000 - float(value.strip()))/10)
        names.append(name)
        values.append(value)

print(names)
print(values)

plt.title("Branch Mis-Prediction Rate for different branch predictors")
plt.xlabel("% Mispredictions")
plt.ylabel("Configurations")
plt.barh(np.arange(len(names)), values)
plt.yticks(np.arange(len(names)), labels = names)
plt.show()
