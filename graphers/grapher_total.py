import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
# import sys
# reading the data from the file
# with open('../out/dict.txt') as f:
#     data = f.read()
  
# data = data.splitlines()

# args = sys.argv
# percent = int(args[1])/100

# negative_data = []
# positive_data = []
# positive_value = []
# negative_value = []
# names = []
# pairs = {}
# for pair in data:
#     pair = pair.split(':')
#     values = list(map(int,pair[1].split()[0:4]))
#     key = tuple(pair[0].split())
#     pairs[key] = values
#     recovered = values[1]
#     passed = values[2]
#     summ = values[0]
#     if summ==0:
#         continue
#     recovered_percent = recovered/summ
#     passed_percent = passed/summ
#     names.append(f'{key}')
#     positive_data.append(100*recovered_percent)
#     positive_value.append(recovered)

#     negative_data.append(-100*passed_percent)
#     negative_value.append(-1*passed)
    
# print(pairs)

# names = names[:10]
# positive_data = positive_data[:10]
# negative_data = negative_data[:10]
#positive-negative bar graph using matplotlib?

def plot_total(pairs,percent):
    negative_data = []
    positive_data = []
    positive_value = []
    negative_value = []
    names = []

    pairs = dict(sorted(pairs.items(), key = lambda x:x[1][1],reverse=True))
    for key,values in pairs.items():
        recovered = values[1]
        passed = values[2]
        summ = values[0]
        if summ==0:
            continue
        names.append(f'{key}')
        positive_data.append(values[4])
        positive_value.append(recovered)

        negative_data.append(values[5])
        negative_value.append(-1*passed)

    x = int(len(positive_data)*percent)

    names = names[0:x]
    positive_data = positive_data[0:x]
    positive_value = positive_value[0:x]
    negative_data = negative_data[0:x]
    negative_value = negative_value[0:x]

    fig, (ax,plt1) = plt.subplots(2,1,sharex=True)
    # ax.bar(x, negative_data, width=0.1, color='tomato')
    # ax.bar(x, positive_data, width=0.1, color='b')
    ax.bar(names,positive_data,color='mediumseagreen')
    ax.bar(names,negative_data,color='tomato')
    ax.set_title("Sorted based on total errors received",pad=20)
    plt.xticks(rotation=90)
    ax.set_ylabel("Percentage")

    # ax.set_ylabel("passed on percentage",fontdict={'color':'tomato'})




    plt1.bar(names,positive_value,color='mediumseagreen')
    plt1.bar(names,negative_value,color='tomato')
    plt1.set_ylabel("Magnitude")

    plt.xticks(rotation=90)
    plt.tick_params(axis = 'x',labelsize=5*(1/(percent+1)*(percent+1)))

    # plt.autoscale()

    red_patch = mpatches.Patch(facecolor='tomato', edgecolor='#000000') # This will create a red bar with black borders, you can leave out edgecolor if you do not want the borders
    green_patch = mpatches.Patch(facecolor='mediumseagreen', edgecolor='#000000')
    fig.legend(handles = [green_patch,red_patch], labels=['fail-safe','fail-open'],
        loc="lower left",
        borderaxespad=0.1)

    plt.tight_layout()
    fig.set_figwidth(20)
    plt.savefig('bar_total.png')
    plt.savefig('bar_total.svg')



    #Source: https://stackoverflow.com/questions/25550308


