# test infos

import os
import patientsfind
import pandas as pd

os.chdir('/home/jason/Documents/Thesis/azuretry2/iOS')
stat = {}
dfall = pd.DataFrame([])
for root, dirs, files in os.walk(os.getcwd(), topdown=True):
    for f in files:
        os.chdir(os.path.abspath(root))
        if f.startswith('Info.json'):
            dfall = pd.concat([dfall, pd.DataFrame([patientsfind.info(f)])])
dfall1 = dfall.drop(columns=['User_Age', 'User_Gender'])
# print(dfall.sort_values('User_PHQ9', ascending=False))

os.chdir('/home/jason/Documents/Thesis/TypingData/iOS_old')
stat = {}
dfall = pd.DataFrame([])
for root, dirs, files in os.walk(os.getcwd(), topdown=True):
    for f in files:
        os.chdir(os.path.abspath(root))
        if f.startswith('Info.json'):
            dfall = pd.concat([dfall, pd.DataFrame([patientsfind.info(f)])])
dfall2 = dfall.drop(columns=['User_Age', 'User_Gender'])
# print(dfall.sort_values('User_PHQ9', ascending=False))

print(pd.merge(dfall1, dfall2, how='inner', on='UserID').head(50))
