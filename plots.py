import os
import pandas as pd
import matplotlib.pyplot as plt 

os.chdir('/home/jason/Documents/Thesis/TypingData/iOS/D557D8F8-4507-4C85-9E72-73D8DA37D2EC')

data = pd.read_csv('output_user.csv')
df = pd.DataFrame(data)
df = df.dropna()
dftemp = df.group_by('Mood')

boxplot = df.boxplot(column=['HT_Mean'], by='Mood')
plt.show(boxplot)

