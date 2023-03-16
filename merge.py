import subprocess

import graphviz
from graph import *

g = graphviz.Digraph('G', filename='dot.gv')

def help(graph):
    
    # for node in graph.nodeHT.keys():
    #     node = graph.nodeHT[node]
    #     print(f"{node.sid} - {node.level}")

    rootnode = graph.rootNode

    def helper(node):
        for child in node.children.keys():
            g.edge(node.sid, child.sid)
            helper(child)

    helper(rootnode)

    # g.view()

    subprocess.run(["dot", "-T", "pdf" , "./dot.gv" ,"-o", "./dot.pdf"])
    subprocess.run(["dot", "-T", "png" , "./dot.gv" ,"-o", "./dot.png"])
    g.save()



def merge_graphs(list_of_graphs):
    final_graph = list_of_graphs[0]

    to_visit = []
    node = final_graph.rootNode
    to_visit.append(node)
  
    node_serviceName = final_graph.processName[node.pid]
    while(len(to_visit) !=0):
        children = list(node.children.keys())
        for graph in  list_of_graphs[1:]:
            for new_node in graph.nodeHT.values():
                new_nodeserviceName = graph.processName[new_node.pid]
                if node_serviceName == new_nodeserviceName and node.opName == new_node.opName and node.level == new_node.level:
                    for key in children:
                        child1 = key
                        child1_sName = final_graph.processName[child1.pid]
                        for child2 in new_node.children:
                            child2_sName = graph.processName[child2.pid]
                            if child1.opName == child2.opName and child1_sName == child2_sName and child1.level == child2.level:
                                print("+")
                                print(child1)
                                print(child2)
                                continue
                                
                            else:
                                print ("-")
                                node.children[child2] = True

                                final_graph.processName[child2.pid] = child2_sName
                                # final_graph.nodeHT[]
                
        to_visit.pop(0)
    help(final_graph)
    print(final_graph.rootNode.children)
