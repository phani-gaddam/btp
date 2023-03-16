import json
import graphviz
import graph
import subprocess


g = graphviz.Digraph('G', filename='dot.gv')

# path = r"/home/rohith/code/btp/test_cases/demo.json"

path = r"/home/rohith/code/btp/1ktrace/f1.json"

data = json.load(open(path))

# serviceName, operationName, filename, rootTrace = "S1", "O1", "1.json", "A"

serviceName, operationName, filename, rootTrace = "Service43", "Operation159", "f1.json", "A"

graph = graph.Graph(data, serviceName, operationName, filename, rootTrace)

graph.assignLevels()

for node in graph.nodeHT.keys():
    node = graph.nodeHT[node]
    print(f"{node.sid} - {node.level}")

rootnode = graph.rootNode

def helper(node):
    for child in node.children.keys():
        g.edge(node.sid, child.sid)
        helper(child)

helper(rootnode)

# g.view()

subprocess.run(["dot", "-T", "pdf" , "dot.gv" ,"-o", "dot.pdf"])
subprocess.run(["dot", "-T", "png" , "dot.gv" ,"-o", "dot.png"])
g.save()

