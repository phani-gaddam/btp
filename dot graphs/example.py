import subprocess
import graphviz


g = graphviz.Digraph('G', filename='example.dot', format="svg")



# g.edge("A","B",dir="both",color="red:blue")
# g.node("C",style="filled",fillcolor="blue",shape="circle")
g.node(name="""a dummy""",label="""This is label""")

g.node(name="4" ,tooltip="""<
    <table BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4"> 
        <tr>
            <td bgcolor="red" port="L">1</td>
            <td bgcolor="blue" port="R"></td>
        </tr>   
     </table>         >""")
g.node("C",shape="none", label="""<
    <table BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4"> 
        <tr>
            <td bgcolor="red" port="L">1</td>
            <td bgcolor="blue" port="R"></td>
        </tr>   
     </table>         >""")

g.node('b',label="""<
<table cellpadding="0" cellborder="0" cellspacing="0" border="0">
<tr>
<td bgcolor="orange">abc</td>
<td bgcolor="yellow">def</td>
</tr>
</table>
>""")

g.node('A', label="""<
<table cellpadding="0" cellborder="0" cellspacing="0" border="0" >
<tr>
<td bgcolor="orange" >abc</td>
<td bgcolor="yellow">def</td>
</tr>
</table>
>""")

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
    # print([h/100.0,s/100.0,v/100.0])
    return [h, s, v]

def gradient(err_prcnt,color="red"):
    h,s,v = rgb_to_hsv(255 - err_prcnt * 255.0/100.0, 255, 255)
    print (f"{h/100.0} {s/100.0} {v/100.0}")
    return f"{h/100.0} {s/100.0} {v/100.0}"

def gradient2(err_prcnt,color="red"):
    h,s,v = rgb_to_hsv(255 - 0 * 255.0/100.0,0,0)
    print (f"{h/100.0} {s/100.0} {v/100.0}")
    return f"{h/100.0} {s/100.0} {v/100.0}"


g.node("0",fillcolor=gradient(0), style="filled")
g.node("10",fillcolor=gradient(10), style="filled")
g.node("20",fillcolor=gradient(20), style="filled")
g.node("30",fillcolor=gradient(30), style="filled")
g.node("40",fillcolor=gradient(40), style="filled")
g.node("50",fillcolor=gradient(50), style="filled")
g.node("60",fillcolor=gradient(60), style="filled")
g.node("70",fillcolor=gradient(70), style="filled")
g.node("80",fillcolor=gradient(80), style="filled")
g.node("90",fillcolor=gradient(90), style="filled")
g.node("100",fillcolor=gradient(100), style="filled")
g.node("101",fillcolor=gradient2(100), style="filled")

# g.edge("B","C", penwidth="2.55")
# g.edge("C","D",weight="3")
# g.node('C')



# g.render(filename="example.dot")
# subprocess.run(["dot", "-Tsvg", "png" , "./dot.gv" ,"-o", "./dot.svg"])
g.render(outfile="example.svg")
