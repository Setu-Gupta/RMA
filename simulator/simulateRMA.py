import sys
from BPs import *

if len(sys.argv) <= 2:
    print("Usage: The first argument is the trace file")
    print("Usage: The second argument is the pattern file")
    exit(-1)

# Extract the patterns from the pattern file
patterns = {}
length = 0
with open(sys.argv[2], 'r') as pattern_file:
    for line in pattern_file.readlines():
        if '->' in line:
            pat, target = line.split('->')
            pat = pat.strip()
            target = target.strip()

            taken = False
            if target == 'T':
                taken = True
            
            pattern = []
            for marker in pat.split():
                pattern.append(int(marker))
            
            length = max(length, len(pattern))
            patterns[tuple(pattern)] = taken

# Create the four test cases
BP1 = MarkerBP_defaultT(patterns, length)
BP2 = MarkerBP_defaultNT(patterns, length)
BP3 = MarkerBP_Last(patterns, length)
BP4 = MarkerBP_Hist(patterns, length)
BP5 = BP_Last()
BP6 = BP_Hist()

total_branches = 0
BP1_miss = 0
BP2_miss = 0
BP3_miss = 0
BP4_miss = 0
BP5_miss = 0
BP6_miss = 0

with open(sys.argv[1], 'r') as trace_file:
    for line in trace_file.readlines():
        line = line.strip()
        
        if line[0] == 'B':   # Branch instruction
            
            # Get the true state
            true = line[1] == '1'

            # Get the estimate
            est1 = BP1.pred()
            est2 = BP2.pred()
            est3 = BP3.pred()
            est4 = BP4.pred()
            est5 = BP5.pred()
            est6 = BP6.pred()
            
            # Update the stats
            total_branches += 1            
            if true:
                BP1_miss += (est1 == False)
                BP2_miss += (est2 == False)
                BP3_miss += (est3 == False)
                BP4_miss += (est4 == False)
                BP5_miss += (est5 == False)
                BP6_miss += (est6 == False)
            else:
                BP1_miss += (est1 == True)
                BP2_miss += (est2 == True)
                BP3_miss += (est3 == True)
                BP4_miss += (est4 == True)
                BP5_miss += (est5 == True)
                BP6_miss += (est6 == True)
            
            # Update the state
            BP3.updateBranch(true)
            BP4.updateBranch(true)
            BP5.updateBranch(true)
            BP6.updateBranch(true)

        else:   # Marker Instruction
            marker = int(line)
            BP1.update(marker)
            BP2.update(marker)
            BP3.update(marker)
            BP4.update(marker)

mpki1 = (BP1_miss/total_branches) * 100
mpki2 = (BP2_miss/total_branches) * 100
mpki3 = (BP3_miss/total_branches) * 100
mpki4 = (BP4_miss/total_branches) * 100
mpki5 = (BP4_miss/total_branches) * 100
mpki6 = (BP4_miss/total_branches) * 100

print("MPKI for MarkerBP with default taken branch:", mpki1)
print("MPKI for MarkerBP with default not taken branch:", mpki2)
print("MPKI for MarkerBP with last branch predictor:", mpki3)
print("MPKI for MarkerBP with 2 bit hysteresis:", mpki4)
print("MPKI for Last branch predictor:", mpki5)
print("MPKI for 2 bit hysteresis predictor:", mpki6)
