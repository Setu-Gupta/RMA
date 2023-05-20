import matplotlib.pyplot as plt
import numpy as np
import sys

if len(sys.argv) <= 1:
    print("Usage: The first argument is the results file")

names = []
values = []
names_RMA = []
values_RMA = []
name_best = []
value_best = []
with open(sys.argv[1], 'r') as results:
    for line in results.readlines():
        name, value = line.split(':')
        name = name.strip().split("MPKI for ")[-1].replace("with", "with\n")

        value = 100 - ((1000 - float(value.strip()))/10)
        if "MarkerBP" in name:
            if "default not taken" in name:
                name_best.append(name)
                value_best.append(value)
            else:
                names_RMA.append(name)
                values_RMA.append(value)
        else:
            names.append(name)
            values.append(value)

all_labels = names + names_RMA + name_best
all_values = values + values_RMA + value_best
all_label_positions = np.arange(len(all_labels))
plt.title("Branch Misprediction rate for different Branch Predictors", fontsize=24)
plt.xlabel("% Mispredictions", fontsize=24)
plt.ylabel("Configurations", fontsize=24)
plt.barh(all_label_positions[:len(names)], values, color='r')
plt.barh(all_label_positions[len(names):len(names) + len(names_RMA)], values_RMA, color='b')
plt.barh(all_label_positions[len(names) + len(names_RMA):], value_best, color='g')
plt.yticks(all_label_positions, labels=all_labels, fontsize=20)
plt.xticks(fontsize=20)
plt.show()
