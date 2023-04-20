import matplotlib.pyplot as plt
import sys

if(len(sys.argv) < 4):
    print("Usage: The first argument is the path to the trace file")
    print("       The second argument is the start of the trace")
    print("       The last argument is the end of the trace")

taken_stream_points = []
taken_stream_steps = []

not_taken_stream_points = []
not_taken_stream_steps = []

last_branch_status = 'x'

start = int(sys.argv[2])
end = int(sys.argv[3])
current_step = 0
with open(sys.argv[1], 'r') as tracefile:
    for line in tracefile.readlines():
        if start <= current_step and current_step <= end:
            if line[0] == 'B':  # Branch line
                if last_branch_status == line[1]:  # Same stream
                    if last_branch_status == '1':
                        taken_stream_points[-1] += 1
                    else:
                        not_taken_stream_points[-1] += 1
                else:   # New stream
                    if line[1] == '1':
                        taken_stream_points.append(1)
                        taken_stream_steps.append(current_step)
                    elif line[1] == '0':
                        not_taken_stream_points.append(1)
                        not_taken_stream_steps.append(current_step)
                    last_branch_status = line[1]
        current_step += 1

plt.title("Branch streams")
plt.scatter(not_taken_stream_steps, not_taken_stream_points, marker='.', c='r', label="Not Taken branches")
plt.scatter(taken_stream_steps, taken_stream_points, marker='.', c='b', label="Taken branches")
plt.legend()
plt.xlabel("Time steps")
plt.ylabel("Length of streams")
plt.grid()
plt.autoscale(enable=True, axis='x', tight=True)
plt.show()
