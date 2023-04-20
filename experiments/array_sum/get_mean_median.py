import matplotlib.pyplot as plt
import sys

path = sys.argv[1]

unit = ''
opt = []
unopt = []
cur = None
with open(path, 'r') as log:
    for line in log:
        if ' OPT' in line:
            cur = 'OPT'
        elif 'UNOPT' in line:
            cur = 'UNOPT'
        elif '=' not in line:
            unit = line[-3:]
            if cur == 'OPT':
                opt.append(int(line[:-3].split()[-1]))
            elif cur == 'UNOPT':
                unopt.append(int(line[:-3].split()[-1]))

mean_opt = sum(opt)/len(opt)
mean_unopt = sum(unopt)/len(unopt)

opt.sort()
unopt.sort()
median_opt = -1
median_unopt = -1

if len(opt) % 2 == 0:
    idx1 = len(opt) / 2
    idx2 = idx1 - 1
    median_opt = (opt[idx1] + opt[idx2])/2
else:
    idx = len(opt) // 2
    median_opt = opt[idx]
if len(unopt) % 2 == 0:
    idx1 = len(unopt) / 2
    idx2 = idx1 - 1
    median_unopt = (unopt[idx1] + unopt[idx2])/2
else:
    idx = len(unopt) // 2
    median_unopt = unopt[idx]

unit = unit.strip()
print("Optimized mean:", mean_opt, unit)
print("Optimized median:", median_opt, unit)
print("Unoptimized mean:", mean_unopt, unit)
print("Unoptimized median:", median_unopt, unit)
print("Speedup:", mean_unopt/mean_opt)

names = ["Opt Mean", "Opt Median", "Unopt Mean", "Unopt Median"]
values = [mean_opt, median_opt, mean_unopt, median_unopt]
plt.bar(names[:2], values[:2], color='b')
plt.bar(names[2:], values[2:], color='r')
plt. title("Runtime variation in optimized (Opt) and unoptimized (Unopt) variants")
plt.ylabel("Execution time in " + unit)
plt.savefig('array_sum.png')
