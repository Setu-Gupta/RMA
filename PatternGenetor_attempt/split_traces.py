# Ref: https://networkx.org/documentation/stable/tutorial.html

import sys
import networkx as nx

if len(sys.argv) < 3:
    print("Please specify the name of the input trace file as the first argument and the output dump file as the second argument")
    exit(-1)

print("Reading traces from", sys.argv[1], "and dumping split traces to", sys.argv[2])

# Read the trace file
traces = []
with open(sys.argv[1], 'r') as trace:
    traces.extend(trace.readlines())

# Split all the traces one by one
with open(sys.argv[2], 'w') as of:
    for trace in traces:
        split_trace = ""
        for marker in trace.split():
            if marker != "-2" and marker[0] != "B" and marker != "-1": # Parsing a regular marker
                split_trace += " " + marker
            elif marker[0] == "B":  # Reached a branch marker
                history = split_trace   # Old value of split_trace
                split_trace += " " + ("A" if marker[-1] == "1" else "R")
                of.write(split_trace + "\n")
                split_trace = history
            elif marker == "-2" or marker == "-1":  # Reached the end or the start of the trace
                split_trace = ""
