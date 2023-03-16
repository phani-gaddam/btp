from graph import *


def merge_graphs(list_of_graphs):
    final_graph = list_of_graphs[0]

    to_visit = []
    node = final_graph.rootNode
    to_visit.append(node)
  
    node_serviceName = final_graph.processName[node.pid]
    while(len(to_visit) !=0):
        for graph in  list_of_graphs[1:]:
            for new_node in graph.nodeHT.values():
                new_nodeserviceName = graph.processName[new_node.pid]
                if node_serviceName == new_nodeserviceName and node.opName == new_node.opName and node.level == new_node.level:
                    for child1 in node.children:
                        child1_sName = final_graph.processName[child1.pid]
                        for child2 in new_node.children:
                            child2_sName = graph.processName[child2.pid]
                            if child1.opName == child2.opName and child1_sName == child2_sName and child1.level == child2.level:
                                continue
                            else:
                                node.children.append(child2)
                                final_graph.processName[child2.pid] = child2_sName
                
        to_visit.pop(0)