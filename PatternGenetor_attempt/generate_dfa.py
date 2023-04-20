# Ref: https://networkx.org/documentation/stable/tutorial.html
# Ref: https://networkx.org/documentation/stable/reference/generated/networkx.relabel.relabel_nodes.html

import sys
import networkx as nx

def generate_graph(traces):
    G = nx.DiGraph()
    node_id = 1
    start_node_id = 0
    terminal_node_ids = []
    for t in traces:
        # Always start DFAs with the same start node
        prev_node = start_node_id
        
        # Add nodes to this DFA
        for edge_label in t.split():
            
            # Check if last node is reached
            if edge_label in ("A", "R"):
                terminal_node_ids.append(prev_node)
            else:
                node_to_add = node_id
                node_id += 1
                
                # Add an edge between node and prev_node
                G.add_edge(prev_node, node_to_add, label=edge_label)
                prev_node = node_to_add 

    # Remove node labels
    label_map = {}
    for ni in range(node_id):
        label_map[ni] = ""
    label_map[start_node_id] = "Start"
    for n in terminal_node_ids:
        label_map[n] = "End"
    nx.set_node_attributes(G, label_map, "label")
    return G


if len(sys.argv) < 3:
    print("Please specify the name of the input split trace file as the first argument, the output file for accept DFA as the second argument and the output file foe reject DFA as the third argument")
    exit(-1)

print("Reading traces from", sys.argv[1], "dumping accept graph to", sys.argv[2], "and reject graph to", sys.argv[3])

# Read the trace file
accept_traces = []
reject_traces = []
with open(sys.argv[1], 'r') as trace:
    for line in trace.readlines():
        line = line.strip()
        if line[-1] == "A":
            accept_traces.append(line)
        elif line[-1] == "R":
            reject_traces.append(line)

GA = generate_graph(accept_traces)
GR = generate_graph(reject_traces)

# Dump the graph
nx.drawing.nx_pydot.write_dot(GA, sys.argv[2])
nx.drawing.nx_pydot.write_dot(GR, sys.argv[3])
