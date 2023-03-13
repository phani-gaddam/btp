import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
# reading the data from the file
with open('../out/dict.txt') as f:
    data = f.read()
  
data = data.splitlines()

negative_data = []
positive_data = []
positive_value = []
negative_value = []
names = []
pairs = {}
for pair in data:
    pair = pair.split(':')
    values = list(map(int,pair[1].split()))
    key = tuple(pair[0].split())
    pairs[key] = values
    recovered = values[1]
    passed = values[2]
    summ = values[0]
    if summ==0:
        continue
    recovered_percent = recovered/summ
    passed_percent = passed/summ
    names.append(f'{key}')
    positive_data.append(100*recovered_percent)
    positive_value.append(recovered)

    negative_data.append(-100*passed_percent)
    negative_value.append(-1*passed)
    
# print(pairs)

# names = names[:10]
# positive_data = positive_data[:10]
# negative_data = negative_data[:10]
#positive-negative bar graph using matplotlib?

x = len(positive_data)

print("positive +++++++++",len(positive_data))
# print(positive_data)
print("negative ---------",len(negative_data))
# print(negative_data)



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
plt.tick_params(axis = 'x',labelsize=5)

# plt.autoscale()

red_patch = mpatches.Patch(facecolor='tomato', edgecolor='#000000') # This will create a red bar with black borders, you can leave out edgecolor if you do not want the borders
green_patch = mpatches.Patch(facecolor='mediumseagreen', edgecolor='#000000')
fig.legend(handles = [green_patch,red_patch], labels=['fail-safe','fail-open'],
       loc="lower left",
       borderaxespad=0.1)

plt.tight_layout()
fig.set_figwidth(10)
plt.show()



#Source: https://stackoverflow.com/questions/25550308


