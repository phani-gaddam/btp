import json
import graph
from graph import GraphNode



# path = r"/home/rohith/code/btp/test_cases/demo.json"

# path = r"/home/rohith/code/btp/1ktrace/f1.json"

path = r"/home/rohith/code/btp/new_test/1.json"

data = json.load(open(path))

serviceName, operationName, filename, rootTrace = "S1", "O1", "1.json", "A"

# serviceName, operationName, filename, rootTrace = "Service43", "Operation159", "f1.json", "A"

graph = graph.Graph(data, serviceName, operationName, filename, rootTrace)

graph.assignLevels()


def getChildrenErrorDict(node:GraphNode):
    di = {}
    for child in node.children.keys():
        serviceName = graph.processName[child.pid]
        key = (serviceName,child.opName)
        if child.errorFlag == True:
            di[key] = 1
        else:
            di[key] = 0
    return di
    
def helper(node:GraphNode,d):
    children = node.children.keys()
    # serviceName = self.processName[root.pid]
    serviceName = graph.processName[node.pid]
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
    
    d[key][4] = getChildrenErrorDict(node)

    for node in children:
        helper(node,d)


rootNode:GraphNode = graph.rootNode
d = {}
helper(rootNode,d)

sorted_d = dict(sorted(d.items(), key = lambda x:x[1][0],reverse=True))

with open('./dict.txt', 'w+') as f:
    for key, value in sorted_d.items(): 
        f.write('%s:%s\n' % (f'{key[0]} {key[1]}', f'{value[0]} {value[1]} {value[2]} {value[3]} {value[4]}'))



    
# key - [pid,opName]
# value = [err_child_count,recovery_count,passed_on,produced_itself]
# for node in nodes:
#     key = (node.serviceName,node.opName)
#     if d.get(key) is not None:
#         if node.hasErrorChild == True and node.errorFlag == True:
#             value = d[key] 
#             value[0] += 1
#             value[1] += 0
#             value[2] += 1
#             value[3] += 0
#         if node.hasErrorChild == True and node.errorFlag == False:
#             value = d[key] 
#             value[0] += 1
#             value[1] += 1
#             value[2] += 0
#             value[3] += 0
#         if node.hasErrorChild == False and node.errorFlag == True:
#             value = d[key] 
#             value[0] += 0
#             value[1] += 0
#             value[2] += 0
#             value[3] += 1
#         if node.hasErrorChild == False and node.errorFlag == False:
#             value = d[key] 
#             value[0] += 0
#             value[1] += 0
#             value[2] += 0
#             value[3] += 0
#     else:
#         d[key] = [0,0,0,0]


# sorted_d = dict(sorted(d.items(), key = lambda x:x[1][0],reverse=True))

# with open('./out/dict.txt', 'w') as f:
#     for key, value in sorted_d.items(): 
#         f.write('%s:%s\n' % (f'{key[0]} {key[1]}', f'{value[0]} {value[1]} {value[2]} {value[3]}'))


# for node in graph.nodeHT.keys():
#     node = graph.nodeHT[node]
#     print(f"{node.sid} - {node.level}")

# rootnode = graph.rootNode

# def helper(node):
#     for child in node.children.keys():
#         g.edge(node.sid, child.sid)
#         helper(child)

# helper(rootnode)

# # g.view()

# subprocess.run(["dot", "-T", "pdf" , "./dot.gv" ,"-o", "./dot.pdf"])
# subprocess.run(["dot", "-T", "png" , "./dot.gv" ,"-o", "./dot.png"])
# subprocess.run(["dot", "-Tsvg", "png" , "./dot.gv" ,"-o", "./dot.svg"])
# # dot -Tsvg graph.dot -o file
# g.save()

