# Ref: https://networkx.org/documentation/stable/tutorial.html
# Ref: https://networkx.org/documentation/stable/reference/generated/networkx.relabel.relabel_nodes.html
# Ref: https://networkx.org/documentation/stable/reference/generated/networkx.drawing.nx_pydot.read_dot.html
# Ref: https://networkx.org/documentation/stable/reference/classes/generated/networkx.DiGraph.nodes.html#networkx.DiGraph.nodes
# Ref: https://www.geeksforgeeks.org/minimization-of-dfa/

import sys
import networkx as nx
import itertools

if len(sys.argv) < 3:
    print("Please specify the name of the input dot file as the first argument and the output file as the second argument")
    exit(-1)

print("Reading traces from", sys.argv[1], "and dumping graph to", sys.argv[2])

# Read the dot file
G = nx.DiGraph(nx.drawing.nx_pydot.read_dot(sys.argv[1]))

# Get the nodes and edges of the graph
nodes = nx.get_node_attributes(G, 'label')
edges = nx.get_edge_attributes(G, 'label')

# Extract out the alphabet set
alphabets = set()
for edge in edges:
    alphabets.add(int(edge[0]))
    alphabets.add(int(edge[1]))

# Extract out the states of the DFA 
states = set()
terminal_states = set()
non_terminal_states = set()
for node in nodes:
    states.add(int(node))
    if nodes[node] == "End":
        terminal_states.add(int(node))
    else:
        non_terminal_states.add(int(node))

# Create the transition function
trans = {}

# Populate the transition function by adding all the edges
for edge, alph in edges.items():
    src_state = int(edge[0])
    dst_state = int(edge[1])
    if (src_state, alph) not in trans:
        trans[(src_state, alph)] = set()
    trans[(src_state, alph)].add(dst_state)

# Create self transitions for the remaining alphabets
for state in states:
    for alph in alphabets:
        if (state, alph) not in trans:
            trans[(state, alph)] = set([state])

# Start the minimization
partition = [terminal_states, non_terminal_states]
while(True):
    # Allocate the new partitions
    new_partition = []
    
    for S in partition:
        for (s1, s2) in itertools.combinations(S, 2):
            
            # Check if s1 and s2 are same
            same = True
            for alph in alphabets:
                if trans[(s1, alph)] == trans[(s2, alph)]:
                    same = False
                    break
            
    # Break if parition didn't change
    if partition[0] == new_partition[0] and partition[1] == new_partition[1]:
        break
    if partition[0] == new_partition[1] and partition[1] == new_partition[0]:
        break
