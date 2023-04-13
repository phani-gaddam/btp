import json
import graphviz
import graph
from graph import GraphNode

g = graphviz.Digraph('G', filename='final.gv', format="svg")


path = r"/home/rohith/code/btp/dot graphs/dict2.json"

data = json.load(open(path))

print(data)

for k,v in data.items():
    g.node(name=k,label=k)

for k,v in data.items():
    for n,val in v[4].items():
        g.edge(k,n,weight=str(val),penwidth=str(val))



g.render(outfile="final.svg")