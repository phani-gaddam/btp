import json
import graphviz
import sys

g = graphviz.Digraph('G', filename='tmp_gh.gv', format="svg")


# give dict.json as argument
path = sys.argv[1]

data = json.load(open(path))

for k,v in data.items():
    g.node(name=k,label=k)

for k,v in data.items():
    for n,val in v[4].items():
        g.edge(n,k,weight=str(val),label=str(val))

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