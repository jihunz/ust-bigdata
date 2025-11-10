import pandas as pd
import matplotlib
from matplotlib.patches import Patch
# matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

country = ['Korea', 'Japan', 'China country', 'Thailand', 'Hong Kong']
temp = [19, 15, 30, 34, 33]
bar_labels = ['red', 'blue']
threshold = 20

bar_colors = ['tab:blue' if t < threshold else 'tab:red' for t in temp]

ax.bar(country, temp, color=bar_colors)

ax.set_ylabel('temperature')
ax.set_title('Country temperature')
legend_elements = [
    Patch(facecolor='tab:blue', label=f'≤ {threshold}(blue)'),
    Patch(facecolor='tab:red', label=f'> {threshold}(red)')
]
ax.legend(handles=legend_elements, title='Temperature color')

plt.show()
