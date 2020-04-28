# Correlation and Mutual Information

import pandas as pd
import os

from sklearn.feature_selection import mutual_info_regression


def combine(peakdate):
    """ Combine labels and dynamics .csv into a single DF"""
    os.chdir('/home/jason/Documents/Thesis/azuretry2/iOS/DF')
    dfall = pd.DataFrame([])
    dflabels = pd.DataFrame([])
    dfdynamics = pd.DataFrame([])

    for root, dirs, files in os.walk(os.getcwd(), topdown=True):
        for filename in files:
            if filename.startswith('labels') and \
               filename.endswith(peakdate + '.csv'):
                data = pd.read_csv(filename)
                df = pd.DataFrame(data)
                dflabels = df[['UserID', 'User_PHQ9']]
                break
        for filename in files:
            if filename.startswith('labels') and \
               filename.endswith(peakdate + '.csv'):
                data = pd.read_csv(filename)
                df = pd.DataFrame(data)
                df = df.drop(columns=['UserID', 'User_PHQ9', 'Total'])
                dflabels = pd.concat([dflabels, df], axis=1)
        
        for filename in files:
            if filename.startswith('dynamics') and \
               filename.endswith(peakdate + '.csv'):
                data = pd.read_csv(filename)
                df = pd.DataFrame(data)
                dfdynamics = df[['UserID', 'User_PHQ9']]
                break
        for filename in files:
            if filename.startswith('dynamics') and \
               filename.endswith(peakdate + '.csv'):
                data = pd.read_csv(filename)
                df = pd.DataFrame(data)
                df = df.drop(columns=['UserID', 'User_PHQ9', 'Total'])
                dfdynamics = pd.concat([dfdynamics, df], axis=1)
    # print(dflabels.head(30))
    # print(dfdynamics.head(30))
    dfall = pd.merge(dfdynamics, dflabels, how='inner', on=['UserID', 'User_PHQ9'])
    os.chdir('/home/jason/Documents/Thesis/azuretry2/iOS/DF')
    dfall.dropna().sort_values('User_PHQ9').to_csv('dfall_' + peakdate + '.csv',
                                                   mode='w',
                                                   index=False, header=True)


def cleanratios(currdirectory):
    for root, dirs, files in os.walk(currdirectory, topdown=True):
        for f in files:
            if f.startswith('dfall'):
                print(f)
                data = pd.read_csv(f)
                df = pd.DataFrame(data)
                df['Ratio Mood'] = round((df['Ratio Stressed+Sad'] + 1) / 
                                         (df['Ratio Happy'] + 1), 3)
                df['Ratio Physical_State'] = \
                    round((df['Ratio Tired+Sick'] + 1) / 
                          (df['Ratio Relaxed'] + 1), 3)
                df = df.drop(columns=['Ratio Happy', 'Ratio Stressed+Sad',
                                      'Ratio Tired+Sick', 'Ratio Relaxed'])
                df.to_csv(f, mode='w', header=True,
                          index=False)


def windows(dfdynamics, dflabels):
    """ Store features of user in time windows 
        by using dynamics_user.csv 
                    &&&
        labels of user in time windows
        by using statistics_user.csv
        creating windows_user.csv 
        """
    windows = [
        '2020-01-14:2020-01-19', '2020-01-20:2020-01-25',
        '2020-01-26:2020-01-31', '2020-02-01:2020-02-06',
        '2020-02-07:2020-02-12', '2020-02-13:2020-02-18',
        '2020-02-19:2020-02-24', '2020-02-25:2020-03-01',
        '2020-03-02:2020-03-07', '2020-03-08:2020-03-13',
        '2020-03-14:2020-03-19', '2020-03-20:2020-03-25',
        '2020-03-26:2020-03-31', '2020-04-01:2020-04-06',
        '2020-04-07:2020-04-12', '2020-04-13:2020-04-18'
    ]
    dfuser = pd.DataFrame([])
    dflabels = dflabels.drop_duplicates()
    for w in windows:
        df1 = pd.DataFrame([])
        start = w.split(':')[0] 
        end = w.split(':')[1]
        df1 = dfdynamics[(dfdynamics.Date >= start) & (dfdynamics.Date <= end)]
        df2 = dflabels[(dflabels.Date >= start) & (dflabels.Date <= end)]
        mood = (len(df2[(df2.Mood == 'Stressed') | 
                        (df2.Mood == 'Sad')]) + 5) / \
            (len(df2[df2.Mood == 'Happy']) + 5)
        physical_state = (len(df2[(df2['Physical_State'] == 'Tired') | 
                                  (df2['Physical_State'] == 'Sick')]) + 5) / \
            (len(df2[df2.Mood == 'Relaxed']) + 5)
        
        stat = {
            # 'UserID': userid, 'User_PHQ9': userphq9,

            'HT_Mean': df1.Hold_Time.mean(),
            'HT_STD': df1.Hold_Time.std(),
            'HT_Skewness': df1.Hold_Time.skew(),
            'HT_Kurtosis': df1.Hold_Time.kurtosis(), 
            
            'FT_Mean': df1.Flight_Time.mean(),
            'FT_STD': df1.Flight_Time.std(),
            'FT_Skewness': df1.Flight_Time.skew(),
            'FT_Kurtosis': df1.Flight_Time.kurtosis(), 
            
            'SP_Mean': df1.Speed.mean(),
            'SP_STD': df1.Speed.std(),
            'SP_Skewness': df1.Speed.skew(),
            'SP_Kurtosis': df1.Speed.kurtosis(), 
            
            'PFR_Mean': df1.Press_Flight_Rate.mean(),
            'PFR_STD': df1.Press_Flight_Rate.std(),
            'PFR_Skewness': df1.Press_Flight_Rate.skew(),
            'PFR_Kurtosis': df1.Press_Flight_Rate.kurtosis(), 
            
            'Characters': len(df1),
            'Mood': mood,
            'Physical_State': physical_state,
            'Window': w
        }
        df1 = pd.DataFrame([stat])
        dfuser = pd.concat([dfuser, df1])
    dfuser.set_index('Window').round(3).to_csv('windows_user.csv', mode='w',
                                               header=True, index=True)


def windows_users(dirname):
    """ Loop across users for creating windows_user.csv """
    os.chdir(dirname)
    for root, dirs, files in os.walk(os.getcwd(), topdown=False):
        for d in dirs:
            os.chdir(os.path.abspath(root))
            # Select only user folders
            if not d.endswith('2020') and \
               not d.endswith('2019'):
                os.chdir(os.path.abspath(os.path.join(root, d)))
                for rootb, dirsb, filesb in os.walk(os.getcwd(), topdown=True):
                    if 'dynamics_user.csv' in filesb and \
                       'statistics_user.csv' in filesb:
                        data = pd.read_csv('dynamics_user.csv')
                        dfdynamics = pd.DataFrame(data)
                        data = pd.read_csv('statistics_user.csv')
                        dflabels = pd.DataFrame(data)
                        windows(dfdynamics, dflabels)
                    else:
                        break


def mutual_info():
    """ Compute mutual info between variables and target variable"""
    os.chdir('/home/jason/Documents/Thesis/azuretry2/iOS/DF')
    data = pd.read_csv('dfall.csv')
    df = pd.DataFrame(data)
    features = df.loc[:, 'Ratio FT_Mean':'Ratio FT_STD']
    # target = df.loc[:, 'Ratio Happy':'Ratio Tired+Sick']
    target = df[['Ratio Happy', 'Ratio Stressed+Sad']]
    # print(target)
    targets = target.columns
    dfall = pd.DataFrame([])
    for t in targets:
        mi = mutual_info_regression(features, target[t], discrete_features=False)
        # print()
        dfall[t] = mi
    dfall = dfall.set_index(features.columns)
    # datac = pd.read_csv('correlation.csv')
    # dfc = pd.DataFrame(datac)
    # print(dfc)
    # print(dfc.loc[:, 'Ratio.Happy':'Ratio.Tired.Sick'].head(16).set_index(features.columns))
    print(dfall)

