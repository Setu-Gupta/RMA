import sys

def match_pattern(trace, index, pattern):
    pattern_length = len(pattern)
    
    # Collect pattern_length number of markers
    marker_history = []
    for i in range(index-1, 0, -1):
        if trace[i][0] != 'B':
            marker_history.append(trace[i])
        if len(marker_history) == pattern_length:
            break;
    marker_history.reverse()
    
    if(len(marker_history) != pattern_length):
        return False

    for i, j in zip(pattern, marker_history):
        if i != j:
            return False

    return True

if(len(sys.argv) < 5):
    print("Usage: The first argument is the path to the trace file")
    print("       The second argument is the start of the trace")
    print("       The third argument is the end of the trace")
    print("       The following arguments are the markers of interest")
    exit(-1)

trace = []

start = int(sys.argv[2])
end = int(sys.argv[3])
current_step = 0
with open(sys.argv[1], 'r') as tracefile:
    for line in tracefile.readlines():
        if start <= current_step and current_step <= end:
            trace.append(line.split()[0])
        current_step += 1

pattern = sys.argv[4:]
taken = 0
not_taken = 0
total_branches = 0
tracked_branches = 0
for idx in range(len(trace)):
    if trace[idx][0] == 'B':
        total_branches += 1
    if match_pattern(trace, idx, pattern):
        tracked_branches += 1
    
    if trace[idx] == 'B1' and match_pattern(trace, idx, pattern):
        taken += 1
    elif trace[idx] == 'B0' and match_pattern(trace, idx, pattern):
        not_taken += 1

if(taken == 0 and not_taken == 0):
    taken_ratio = -1
else:
    taken_ratio = taken / (taken + not_taken)

if total_branches == 0:
    track_ratio = -1
else:
    track_ratio = tracked_branches / total_branches

print("Taken ratio:", taken_ratio)
print("Track ratio:", track_ratio)
