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


def compute_metrics(metrics):
    d = {}
    for trace in metrics:
        # nodes.extend(nodelist.nodeHT)
        rootNode:GraphNode = trace.rootNode
        
        helper(rootNode,d,trace)

    sorted_d = dict(sorted(d.items(), key = lambda x:x[1][0],reverse=True))

    with open('./out/dict.txt', 'w+') as f:
        for key, value in sorted_d.items(): 
            f.write('%s:%s\n' % (f'{key[0]} {key[1]}', f'{value[0]} {value[1]} {value[2]} {value[3]} {value[4]}'))

def getChildrenErrorDict(node:GraphNode,trace:Graph,di):
    for child in node.children.keys():
        serviceName = trace.processName[child.pid]
        key = (serviceName,child.opName)

        if child.errorFlag == True:
            if di.get(key) is None:
                di[key] = 1
            else:
                di[key] += 1
        
    return di
    
def helper(node:GraphNode,d,trace:Graph):
    children = node.children.keys()
    # serviceName = self.processName[root.pid]
    serviceName = trace.processName[node.pid]
    key = (serviceName,node.opName)
    if d.get(key) is None:
        d[key] = [0,0,0,0,{}]
    if node.hasErrorChild == True and node.errorFlag == True:
        value = d[key] 
        value[0] += 1
        value[1] += 0
        value[2] += 1
        value[3] += 0
    if node.hasErrorChild == True and node.errorFlag == False:
        value = d[key] 
        value[0] += 1
        value[1] += 1
        value[2] += 0
        value[3] += 0
    if node.hasErrorChild == False and node.errorFlag == True:
        value = d[key] 
        value[0] += 0
        value[1] += 0
        value[2] += 0
        value[3] += 1
    if node.hasErrorChild == False and node.errorFlag == False:
        value = d[key] 
        value[0] += 0
        value[1] += 0
        value[2] += 0
        value[3] += 0
    
    d[key][4] = getChildrenErrorDict(node,trace,d[key][4])

    for node in children:
        helper(node,d,trace)






# def merge_graphs(list_of_graphs):
#     final_graph = list_of_graphs[0]

#     to_visit = []
#     node = final_graph.rootNode
#     to_visit.append(node)
  
#     node_serviceName = final_graph.processName[node.pid]
#     while(len(to_visit) !=0):
#         children = list(node.children.keys())
#         for graph in  list_of_graphs[1:]:
#             for new_node in graph.nodeHT.values():
#                 new_nodeserviceName = graph.processName[new_node.pid]
#                 if node_serviceName == new_nodeserviceName and node.opName == new_node.opName and node.level == new_node.level:
#                     for key in children:
#                         child1 = key
#                         child1_sName = final_graph.processName[child1.pid]
#                         for child2 in new_node.children:
#                             child2_sName = graph.processName[child2.pid]
#                             if child1.opName == child2.opName and child1_sName == child2_sName and child1.level == child2.level:
#                                 print("+")
#                                 print(child1)
#                                 print(child2)
#                                 continue
                                
#                             else:
#                                 print ("-")
#                                 node.children[child2] = True

#                                 final_graph.processName[child2.pid] = child2_sName
#                                 # final_graph.nodeHT[]
                
#         to_visit.pop(0)
#     help(final_graph)
#     print(final_graph.rootNode.children)
