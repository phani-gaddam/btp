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

# g.edge("B","C", penwidth="2.55")
# g.edge("C","D",weight="3")
# g.node('C')



# g.render(filename="example.dot")
# subprocess.run(["dot", "-Tsvg", "png" , "./dot.gv" ,"-o", "./dot.svg"])
g.render(outfile="example.svg")
