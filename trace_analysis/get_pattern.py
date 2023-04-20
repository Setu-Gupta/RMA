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

def get_taken_tracked_ratio(trace, pattern):
    taken = 0
    total_matches = 0
    total_branches = 0
    tracked_branches = 0
    for idx in range(len(trace)):
        if trace[idx][0] == 'B':
            total_branches += 1
            if match_pattern(trace, idx, pattern):
                tracked_branches += 1
        
        if trace[idx] == 'B1' and match_pattern(trace, idx, pattern):
            taken += 1
            total_matches += 1
        elif trace[idx] == 'B0' and match_pattern(trace, idx, pattern):
            total_matches += 1

    if(total_matches == 0):
        taken_ratio = -1
    else:
        taken_ratio = taken / total_matches

    if total_branches == 0:
        track_ratio = -1
    else:
        track_ratio = tracked_branches / total_branches

    return taken_ratio, track_ratio

def get_patterns(patterns, prefix, markers, trace, tolerance, max_length):
    
    if max_length <= 0:
        return

    for m in markers:
        pattern = prefix + [m]
        taken, track = get_taken_tracked_ratio(trace, pattern)
        if(taken == -1 or track == -1):
            continue

        if abs(taken - 1.0) < tolerance:
            patterns[" ".join(pattern)] = ["T", track, taken]
        elif abs(taken - 0.0) < tolerance:
            patterns[" ".join(pattern)] = ["NT", track, 1 - taken]
        else:
            get_patterns(patterns, pattern, markers, trace, tolerance, max_length - 1)

def get_trace(start, end, path):
    trace = []
    start = int(sys.argv[2])
    end = int(sys.argv[3])
    current_step = 0
    with open(sys.argv[1], 'r') as tracefile:
        for line in tracefile.readlines():
            if start <= current_step and current_step <= end:
                trace.append(line.split()[0])
            current_step += 1
    return trace

def get_top_patterns(patterns, max_count, required_coverage, min_coverage):
    
    all_patterns = []
    for k in patterns:
        pattern = k + " " + patterns[k][0]
        coverage = patterns[k][1]
        confidence = patterns[k][2]
        all_patterns.append((pattern, coverage, confidence))

    sorted_patterns = sorted(all_patterns, key=lambda x: -x[1])
    
    count = 0
    coverage = 0
    confidence = 0
    filtered_patterns = {}
    for pattern in sorted_patterns:
        if count == max_count:
            break
        if coverage >= required_coverage:
            break
        
        action = pattern[0].split()[-1]
        match = " ".join(pattern[0].split()[:-1])
        cov = pattern[1]
        conf = pattern[2]

        if cov < min_coverage:
            break
        
        filtered_patterns[match] = action
        confidence += cov * conf
        coverage += cov
        
        count += 1

    return filtered_patterns, coverage, confidence

if(len(sys.argv) <= 8):
    print("Usage: The first argument is the path to the trace file")
    print("       The second argument is the start of the trace")
    print("       The third argument is the end of the trace")
    print("       The fourth argument is maximum tolerable error")
    print("       The fifth argument is the maximum pattern length")
    print("       The sixth argument is the required branch coverage")
    print("       The seventh argument is the maximum number of patterns")
    print("       The eighth argument is the minimum required coverage of patterns")
    exit(-1)


path = sys.argv[1]
start = int(sys.argv[2])
end = int(sys.argv[3])
trace = get_trace(start, end, path)

unique_markers = set()
for t in trace:
    if t[0] != 'B':
        unique_markers.add(t)

patterns = {}
tolerance = float(sys.argv[4])
max_length = int(sys.argv[5])
get_patterns(patterns, [], unique_markers, trace, tolerance, max_length)

coverage = float(sys.argv[6])
top_count = int(sys.argv[7])
min_coverage = float(sys.argv[8])
patterns, achieved_coverage, achieved_confidence = get_top_patterns(patterns, top_count, coverage, min_coverage)

print(f"Captured {achieved_coverage * 100}% branches and achieved overall accuracy of {achieved_confidence * 100}%")
for k in patterns:
    print(k, '->', patterns[k])
