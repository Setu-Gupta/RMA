import matplotlib.pyplot as plt
import sys

if(len(sys.argv) < 4):
    print("Usage: The first argument is the path to the trace file")
    print("       The second argument is the start of the trace")
    print("       The last argument is the end of the trace")

trace_points = []
trace_steps = []

taken_branch_points = []
taken_branch_steps = []

not_taken_branch_points = []
not_taken_branch_steps = []

start = int(sys.argv[2])
end = int(sys.argv[3])
current_step = 0
with open(sys.argv[1], 'r') as tracefile:
    for line in tracefile.readlines():
        if start <= current_step and current_step <= end:
            if line[0] == 'B':  # Branch line
                if line[1] == '1':  # Taken branch
                    taken_branch_points.append(-3)
                    taken_branch_steps.append(current_step)
                else:   # Not taken branch
                    not_taken_branch_points.append(-3)
                    not_taken_branch_steps.append(current_step)
            else:   # Regular marker
                tracer = int(line)
                trace_points.append(tracer)
                trace_steps.append(current_step)
        current_step += 1

plt.title("Traces")
plt.scatter(trace_steps, trace_points, marker='.', c='k', label="Trace markers")
plt.scatter(not_taken_branch_steps, not_taken_branch_points, marker='o', c='r', label="Not Taken branches")
plt.scatter(taken_branch_steps, taken_branch_points, marker='.', c='b', label="Taken branches")
plt.xlabel("Time steps")
plt.ylabel("Marker ID")
plt.legend()
plt.grid()
plt.autoscale(enable=True, axis='x', tight=True)
plt.show()
