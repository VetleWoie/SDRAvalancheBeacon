from matplotlib import pyplot as plt
from matplotlib.patches import Patch
import pandas as pd
import numpy as np
import json
import datetime

# timeData = pd.read_csv("timeline.csv", parse_dates=["Start", "End"])
timeData = pd.read_json("timeline.json", convert_dates=["Start","End"])
print(timeData)
with open("legends.json",'r') as legends_file:
    colors = json.load(legends_file)


projectStartDate = timeData.Start.min()
# number of days from project start to task start
timeData['start_num'] = (timeData.Start-projectStartDate).dt.days
# number of days from project start to end of tasks
timeData['end_num'] = (timeData.End-projectStartDate).dt.days
# days between start and end of each task
timeData['days'] = timeData.end_num - timeData.start_num

legends = [Patch(facecolor=colors[legend], label=legend) for legend in colors]


print(projectStartDate)
print(timeData.start_num)
timeData = timeData.loc[::-1]
fig, ax = plt.subplots(1, figsize=(16,4))
bars = ax.barh(timeData.Work,timeData.days, left=timeData.start_num, color=timeData.Color)

##### TICKS #####
xticks = np.arange(0, timeData.end_num.max()+1, 10)
xticks_labels = pd.date_range(projectStartDate, end=timeData.End.max()).strftime("%m/%d")
xticks_minor = np.arange(0, timeData.end_num.max()+1, 1)
ax.set_xticks(xticks)
ax.set_xticks(xticks_minor, minor=True)
ax.set_xticklabels(xticks_labels[::10])
ax.legend(handles=legends)
plt.show()