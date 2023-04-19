import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import sys
from graphers import grapher_total
from graphers import grapher_open
from graphers import grapher_safe
from graphers import grapher_percent_safe
from graphers import grapher_percent_open

def plot_all(sorted_d,percent,outputdir):
    pairs = {}
    for key,values in sorted_d.items():
        pairs[key] = values[0:4]

    # appending the percentage information to the dictionary
    pairs = dict(sorted(pairs.items(), key = lambda x:x[1][1],reverse=True))
    for key,values in pairs.items():    
        recovered = values[1]
        passed = values[2]
        summ = values[0]
        if summ==0:
            pairs[key].append(100*0)
            pairs[key].append(-100*0)
            continue
        recovered_percent = recovered/summ

        pairs[key].append(100*recovered_percent)
        passed_percent = passed/summ
        pairs[key].append(-100*passed_percent)

    #calling all the graphing functions with the updated dictionary
    grapher_total.plot_total(pairs,percent,outputdir)
    grapher_safe.plot_safe(pairs,percent,outputdir)
    grapher_open.plot_open(pairs,percent,outputdir)
    grapher_percent_safe.plot_safe_percent(pairs,percent,outputdir)
    grapher_percent_open.plot_open_percent(pairs,percent,outputdir)