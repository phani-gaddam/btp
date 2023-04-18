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
    
    # plotall.plot_all(sorted_d,0.2)
    generatehtml(sorted_d)

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

def generatehtml(data):
    g = graphviz.Digraph('G', filename='tmp_gh.gv', format="svg")

    for k,v in data.items():
        g.node(name=str(k),label=str(k))

    print(data)
    for k,v in data.items():
        print("+++++++++++++++++++++++")
        for n,val in v[4].items():
            print("-----------------------------")
            g.edge(str(n),str(k),weight=str(val),label=str(val))

    g.render(outfile="tmp_gh.svg")
    g.render(outfile="tmp_gh.png")
    g.render(outfile="tmp_gh.pdf")


    html = """
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <style>
            .popup {
                display: none;
            }

            .popup.open {
                display: block;
            }

            .blocker {
                position: fixed;
                top: 0;
                left: 0;
                bottom: 0;
                right: 0;
                content: ' ';
                background: rgba(0, 0, 0, .5);
            }

            .popup .contents {
                border: 1px solid #ccc;
                border-radius: 5px;
                width: 200px;
                height: 100px;
                display: flex;
                align-items: center;
                justify-content: center;
                background: #FFF;

                position: fixed;
                top: 50vh;
                left: 50vw;
                transform: translate(-50%, -50%);
            }
        </style>
        <script src="https://d3js.org/d3.v5.min.js"></script>
        <script src="https://unpkg.com/@hpcc-js/wasm@0.3.11/dist/index.min.js"></script>
        <script src="https://unpkg.com/d3-graphviz@3.0.5/build/d3-graphviz.js"></script>
        <title>Document</title>
    </head>

    <body>
        <div id="graph" style="text-align: center;"></div>
        <div class="popup" id="myForm">
            <div class="blocker" onclick="hidePopup()"></div>
            <div class="contents" id="actualpopup">
                This is popup
            </div>
        </div>
        <script>
            var dotSrc = `
    """ + \
        open("./tmp_gh.gv").read() + \
        """`;
        const DATA = """ + \
            open("./dict.json").read() + \
        """
        var dotSrcLines;

            var graphviz = d3.select("#graph").graphviz();

            function render() {
                console.log('DOT source =', dotSrc);
                dotSrcLines = dotSrc.split('\\n');

                graphviz
                    .transition(function () {
                        return d3.transition()
                            .delay(100)
                            .duration(1000);
                    })
                    .renderDot(dotSrc)
                    .on("end", displayPopupOnClickingNodes);
            }



            function interactive() {

                nodes = d3.selectAll('.node,.edge');
                nodes
                    .on("click", function () {
                        alert(data);
                        var title = d3.select(this).selectAll('title').text().trim();
                        var text = d3.select(this).selectAll('text').text();
                        var id = d3.select(this).attr('id');
                        var class1 = d3.select(this).attr('class');
                        dotElement = title.replace('->', ' -> ');
                        console.log('Element id="%s" class="%s" title="%s" text="%s" dotElement="%s"', id, class1, title, text, dotElement);
                        console.log('Finding and deleting references to %s "%s" from the DOT source', class1, dotElement);
                        for (i = 0; i < dotSrcLines.length;) {
                            if (dotSrcLines[i].indexOf(dotElement) >= 0) {
                                console.log('Deleting line %d: %s', i, dotSrcLines[i]);
                                dotSrcLines.splice(i, 1);
                            } else {
                                i++;
                            }
                        }
                        dotSrc = dotSrcLines.join('\\n');
                        render();
                    });
            }

            function displayPopupOnClickingNodes() {
                nodes = d3.selectAll('.node');
                nodes.on("click", function () {
                    const title = d3.select(this).selectAll('title').text();
                    showPopup(title);
                })
            }

            render(dotSrc);

            const popup = document.querySelector('.popup');
            function showPopup(title) {
                var popup_contents = document.getElementById('actualpopup');
                popup_contents.innerHTML = [DATA[title][0], DATA[title][1], DATA[title][2], DATA[title][3]];
                popup.classList.add('open');
            }
            function hidePopup() {
                popup.classList.remove('open');
            }



        </script>
    </body>

    </html>
        """

    f = open('generated.html','w+')
    f.write(html)
    f.close()