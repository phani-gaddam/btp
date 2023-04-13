import json
import graphviz

g = graphviz.Digraph('G', filename='final.gv', format="svg")


path = r"/home/rohith/code/btp/out/dict.json"

data = json.load(open(path))

print(data)

for k,v in data.items():
    g.node(name=k,label=k)

for k,v in data.items():
    for n,val in v[4].items():
        g.edge(k,n,weight=str(val),penwidth=str(val),label=str(val))



g.render(outfile="final.svg")
g.render(outfile="final.png")
g.render(outfile="final.pdf")