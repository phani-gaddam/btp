import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import sys
from graphers import grapher_total
from graphers import grapher_open
from graphers import grapher_safe
from graphers import grapher_percent_safe
from graphers import grapher_percent_open
# reading the data from the file
# with open('../out/dict.txt') as f:
#     data = f.read()

# args = sys.argv
# percent = int(args[1])/100

# data = data.splitlines()


# pairs = {}
# for pair in data:
#     pair = pair.split(':')
#     values = list(map(int,pair[1].split()[0:4]))
#     key = tuple(pair[0].split())
#     if values[0] != 0:
#         pairs[key] = values

def plot_all(sorted_d,percent):
    pairs = {}
    for key,values in sorted_d.items():
        pairs[key] = values[0:4]

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

    grapher_total.plot_total(pairs,percent)
    grapher_safe.plot_safe(pairs,percent)
    grapher_open.plot_open(pairs,percent)
    grapher_percent_safe.plot_safe_percent(pairs,percent)
    grapher_percent_open.plot_open_percent(pairs,percent)