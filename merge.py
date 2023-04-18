import subprocess
from graphers import plotall
import graphviz
from graph import *


def compute_metrics(metrics):
    d = {}
    for trace in metrics:
        # nodes.extend(nodelist.nodeHT)
        rootNode:GraphNode = trace.rootNode
        
        helper(rootNode,d,trace)

    sorted_d = dict(sorted(d.items(), key = lambda x:x[1][0],reverse=True))
    
    plotall.plot_all(sorted_d,0.2)

    with open('./out/dict.txt', 'w+') as f:
        for key, value in sorted_d.items(): 
            f.write('%s:%s\n' % (f'{key[0]} {key[1]}', f'{value[0]} {value[1]} {value[2]} {value[3]} {value[4]}'))
    with open('./out/dict.json','w+') as file:
        file.write(str(sorted_d))

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

