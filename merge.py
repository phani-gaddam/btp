import subprocess
from graphers import plotall
import graphviz
from graph import *


def compute_metrics(metrics,outputdir):
    d = {}
    for trace in metrics:
        # nodes.extend(nodelist.nodeHT)
        rootNode:GraphNode = trace.rootNode
        
        helper(rootNode,d,trace)

    sorted_d = dict(sorted(d.items(), key = lambda x:x[1][0],reverse=True))
    
    plotall.plot_all(sorted_d,0.2,outputdir)
    generatehtml(sorted_d,outputdir)

    # with open('./out/dict.txt', 'w+') as f:
    #     for key, value in sorted_d.items(): 
    #         f.write('%s:%s\n' % (f'{key[0]} {key[1]}', f'{value[0]} {value[1]} {value[2]} {value[3]} {value[4]}'))
    # with open('./out/dict.json','w+') as file:
    #     file.write(str(sorted_d))

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

def gradient(err_prcnt,color="red"):
    h,s,v = rgb_to_hsv(255 - err_prcnt * 255.0/100.0, 255, 255)
    return f"{h/100.0} {s/100.0} {v/100.0}"
    
def rgb_to_hsv(r, g, b):
  
    # R, G, B values are divided by 255
    # to change the range from 0..255 to 0..1:
    r, g, b = r / 255.0, g / 255.0, b / 255.0
  
    # h, s, v = hue, saturation, value
    cmax = max(r, g, b)    # maximum of r, g, b
    cmin = min(r, g, b)    # minimum of r, g, b
    diff = cmax-cmin       # diff of cmax and cmin.
  
    # if cmax and cmax are equal then h = 0
    if cmax == cmin: 
        h = 0
      
    # if cmax equal r then compute h
    elif cmax == r: 
        h = (60 * ((g - b) / diff) + 360) % 360
  
    # if cmax equal g then compute h
    elif cmax == g:
        h = (60 * ((b - r) / diff) + 120) % 360
  
    # if cmax equal b then compute h
    elif cmax == b:
        h = (60 * ((r - g) / diff) + 240) % 360
  
    # if cmax equal zero
    if cmax == 0:
        s = 0
    else:
        s = (diff / cmax) * 100
  
    # compute v
    v = cmax * 100
    return h, s, v

def generatehtml(data,outputdir):
    g = graphviz.Digraph('G', filename='tmp_gh.gv', format="svg")

    max_errs = 0
    for k,v in data.items():
        max_errs = max(v[0],max_errs)
    
    print(max_errs)

    for k,v in data.items():
        # g.node(name=str(k),label=str(k))
        if v[0] != 0: # comtains errors
            g.node(name=f"{k[0]} {k[1]}",label=f"{k[0]} {k[1]}",fillcolor=gradient(v[0]/max_errs*100),style="filled")

    for k,v in data.items():
        for n,val in v[4].items():
            g.edge(f"{n[0]} {n[1]}",f"{k[0]} {k[1]}",weight=str(val),label=str(val))

    g.render(outfile=f"{outputdir}/tmp_gh.svg")
    g.render(outfile=f"{outputdir}/tmp_gh.png")
    g.render(outfile=f"{outputdir}/tmp_gh.pdf")


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
                width: 800px;
                height: 800px;
                display: flex;
                align-items: center;
                justify-content: center;
                background: #FFF;

                position: fixed;
                top: 50vh;
                left: 50vw;
                transform: translate(-50%, -50%);
            }

            .popup .contents2 {
                position: fixed;
                background: #FFF;
                min-height: 60vh;
                min-width: 60vw;
                /* top: 0px;
                left: 0px;
                transform: translate(25%, 50%); */
                top: 50vh;
                left: 50vw;
                transform: translate(-50%, -50%);
                /* right: 0px */
            }


            .grid-container {
                display: grid;
                grid-template-columns: 1fr 1fr;
                grid-gap: 20px;
            }

            #piechart {
                /* display: relative; */
                /* display: none; */
                /* width: 400px; */
                background: aqua;
            }

            /* .canvasjs-chart-canvas {
                position: relative !important;
            } */

            #data {
                padding: 1rem;
            }
        </style>
        <script src="https://d3js.org/d3.v5.min.js"></script>
        <script src="https://unpkg.com/@hpcc-js/wasm@0.3.11/dist/index.min.js"></script>
        <script src="https://unpkg.com/d3-graphviz@3.0.5/build/d3-graphviz.js"></script>
        <!-- <script src="https://canvasjs.com/assets/script/canvasjs.min.js"></script> -->
        <script src='https://cdn.plot.ly/plotly-2.20.0.min.js'></script>
        <title>Document</title>
    </head>

    <body>
        <div id="graph" style="text-align: center;"></div>
        <div class="popup">
            <div class="blocker" onclick="hidePopup()"></div>
            <div class="contents2 grid-container" id="actualpopup">
                <div id="data" style="min-width: 100px;"></div>
                <div id="piechart"></div>
            </div>
        </div>
        <script>
            var dotSrc = `
    """ + \
        open("./out/tmp_gh.gv").read() + \
        """`;
        const DATA = """ + \
            str({f"'{k[0]} {k[1]}'":[v[0],v[1],v[2],v[3],{f"'{a[0]} {a[1]}'":b for a,b in v[4].items()}] for k,v in data.items()}) + \
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
                var err_results = DATA[`'${title}'`];
                var datadiv = document.getElementById('data');
                datadiv.innerHTML = `<p>Total Error instances:${err_results[0]}</p><p>Recovered error instances:${err_results[1]}</p><p>Passed on error instances:${err_results[2]}</p><p>Total self errors produced:${err_results[3]}</p>`;
                // var chart = new CanvasJS.Chart("piechart", {
                // 	animationEnabled: true,
                // 	data: [{
                // 		type: "pie",
                // 		startAngle: 240,

                // 		indexLabel: "{label} : {y}",
                // 		dataPoints: [
                // 			{ y: 6000, label: "fail-safe", color: "green" },
                // 			{ y: 3000, label: "fail-open", color: "red" }

                // 		]
                // 	}]
                // });
                // chart.render();
                var v1 = err_results[1];
                var v2 = err_results[2];

                var data = [{
                    values: [v1, v2],
                    labels: ['Fail safe', 'Fail open'],
                    type: 'pie',
                    marker: {
                        colors: ["mediumseagreen", "tomato"]
                    }
                }];


                var layout = {
                    // height: 400,
                    // width: 500

                };

                Plotly.newPlot('piechart', data, layout, { displaylogo: false });
                popup.classList.add('open');
            }
            function hidePopup() {
                popup.classList.remove('open');
            }



        </script>
    </body>

    </html>
        """

    f = open(f"{outputdir}/generated.html",'w+')
    f.write(html)
    f.close()