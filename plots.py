# plots.py
# Script for generating statistics plots
# Iason Ofeidis 2020

import os
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
# import numpy as np
from matplotlib.figure import figaspect
# import csv
# import patientsfind


def clean(df):
    """ Clean one dataframe from 'Postponing, undefined, TIMEOUT' values"""
    df = df.replace('Happy TIMEOUT', 'Happy')
    df = df.replace('Neutral TIMEOUT', 'Neutral')
    df = df.replace('Sad TIMEOUT', 'Sad')
    df = df.replace('Stressed TIMEOUT', 'Stressed')
    df = df.replace('Relaxation TIMEOUT', 'Relaxation')
    df = df.replace('Tiredness TIMEOUT', 'Tiredness')
    df = df.replace('Sickness TIMEOUT', 'Sickness')
    df = df.replace('undefined TIMEOUT', 'undefined')
    df = df.replace('Postponing TIMEOUT', 'Postponing')
    df = df[(df['Mood'] != 'undefined') &
            (df['Mood'] != 'Postponing') &
            (df['Physical_State'] != 'Postponing') & 
            (df['Physical_State'] != 'undefined')].reset_index(drop=True)

    return df


def evol(df, name, device, label):
    """ Plotting the evolution of Mood labels in time
        Just change label and device variables"""
    # label = 'Mood'
    # device = 'iOS'
    # Clean df from undefined, Postponing, TIMEOUT values
    df = clean(df)
    # Keep only sessions with NumberOfKeystrokes > 5
    # df = df[df['Keystrokes'] > 5]
    # Keep only label and Date columns
    df = df[[label, 'Date']]
    # str(Date) to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    # Keep only recent sessions
    df = df[df['Date'] > '2019-11-01']
    df = df.drop_duplicates()
    # Count labels for each specific Date
    df = df.groupby(df.columns.tolist()).size().reset_index().\
        rename(columns={0: 'records'})
    # Pivot necessary for plotting
    df = df.pivot(index='Date', columns=label, values='records')    
    df = df.fillna(0)
    userid = str(os.path.abspath(os.path.join(os.getcwd(), "./."))).split('/')[-1]
    title = 'UserID: ' + userid + ', Device: ' + device
    if not df.empty:
        if len(df.columns) > 1:
            df.plot(linewidth=4, title=title)
            plt.axvline(x='2020-01-25', linewidth=2, color='r')
            plt.axvline(x='2020-02-28', linewidth=2, color='g')
            plt.show()
        else:
            if len(df) == 1:
                df.plot.bar(title=title)
            else:
                df.plot(linewidth=4, title=title)
                plt.axvline(x='2020-01-25', linewidth=2, color='r')
                plt.axvline(x='2020-02-28', linewidth=2, color='g')
        # plt.gcf()
        # os.chdir('/home/jason/Documents/Thesis/TypingData/' + device + '/Plots')
        # plt.savefig(os.getcwd() + '/' + name + '.png')
        # plt.show()
        plt.close()


def label_distribution(df, name, device, label):
    """ Plotting the distribution of Mood or Physical_State labels 
        in time periods"""
    # Clean df from undefined, Postponing, TIMEOUT values
    df = clean(df)
    # Keep only sessions with NumberOfKeystrokes > 5
    # df = df[df['Keystrokes'] > 5]
    # Keep only label and Date columns 
    df = df[['User_PHQ9', label, 'Date']]
    if not df.empty:
        userphq9 = df['User_PHQ9'][0]
    else:
        userphq9 = 'empty'
    # print(df)
    peakdate = '2020-02-28'
    # Keep only recent sessions
    df = df[df['Date'] > '2019-12-25']
    df = df.drop_duplicates()
    df.loc[(df.Date < peakdate), 'Date'] = 'period1'
    df.loc[(df.Date >= peakdate) & 
           (df.Date != 'period1'), 'Date'] = 'period2'
    df = df.sort_values(by=['Date'])

    # if device == 'iOS':
    #     for root, dirs, files in os.walk(os.getcwd(), topdown=True):
    #         for filename in files:
    #             if filename.startswith('Info.json'):
    #                 info = patientsfind.info(filename)
    #                 userphq9 = str(info['User_PHQ9'])
    #                 break
    #         break
        

    userid = str(os.path.abspath(os.path.join(os.getcwd(), "./.")))\
        .split('/')[-1]
    title = 'UserID: ' + userid + ',\n User_PHQ9: ' + str(userphq9) + \
            ', Device: ' + device
    if not df.empty:
        if (df.Date.nunique() > 1):
            # print(len(df))
            df.groupby(label).Date.value_counts().unstack(1).plot.barh(title=title)
            # plt.set_xlim(0, 10)
            plt.gcf()
            # os.chdir('/home/jason/Documents/Thesis/TypingData/' + device + '/Plots')
            # plt.savefig(os.getcwd() + '/' + name + label + '.png')
            plt.show()
            plt.close()


def dynamics_distribution(df, name, device, dynamics_variable):
    """ Plot the distribution of keystroke dynamics in 2 periods
        Violin Plots """
    df = df.dropna()
    # Keep only recent sessions
    peakdate = '2020-02-28'
    df = df[df['Date'] > '2019-12-25']
    df.loc[(df.Date < peakdate), 'Date'] = 'period1'
    df.loc[(df.Date >= peakdate) & 
           (df.Date != 'period1'), 'Date'] = 'period2'
    df = df.sort_values(by=['Date'])
    userid = str(os.path.abspath(os.path.join(os.getcwd(), "./.")))\
        .split('/')[-1]
    title = 'UserID: ' + userid + ', Device: ' + device
    # Cut extreme values
    if device == 'iOS':
        df = df[df.Hold_Time < 0.3]
        df = df[df.Speed < 5000]
        df = df[df.Flight_Time < 3]
    elif device == 'Android':
        df = df[df.Speed < 5]
        df = df[df.Press_Flight_Rate < 10]
    df = df[[dynamics_variable, 'Date']]
    
    # Keep only users with all 3 periods
    if not df.empty and ('period1' in df.Date.values) and \
                        ('period2' in df.Date.values):
        # fig, axs = plt.subplots(2, 1)
        sns.set() 
        # df.Hold_Time.hist(by=df.Date)
        os.chdir('/home/jason/Documents/Thesis/TypingData/' + device + '/Plots')
        if dynamics_variable == 'Hold_Time':
            sns.violinplot(y=df.Date, x=df.Hold_Time, bw=.2).set_title(title)
            # plt.savefig(os.getcwd() + '/' + name + '_ht.png')
            plt.show()
            plt.close()
        elif dynamics_variable == 'Flight_Time':
            sns.violinplot(y=df.Date, x=df.Flight_Time, bw=.2).set_title(title)
            # plt.savefig(os.getcwd() + '/' + name + '_ft.png')
            plt.show()
            plt.close()
        elif dynamics_variable == 'Speed':
            sns.violinplot(y=df.Date, x=df.Speed, bw=.2).set_title(title)
            # plt.savefig(os.getcwd() + '/' + name + '_sp.png')
            plt.show()
            plt.close()
        elif dynamics_variable == 'Press_Flight_Rate':
            sns.violinplot(y=df.Date, x=df.Press_Flight_Rate, bw=.2).set_title(title)
            # plt.savefig(os.getcwd() + '/' + name + '_pfr.png')
            plt.show()
            plt.close()
        else:
            print('wrong dynamics input')

    return


def ratio(df, label, labelvalue, periods):
    """ Compute percentage and total of a label in a given time period """
    s = 0
    percentages = []
    labels = labelvalue.split('+')
    # print(labels)
    for p in periods:
        # Total
        totals = [len(df[(df[label] == lab) & (df.Date == p)]) 
                  for lab in labels]
        # print(totals)
        s += sum(totals)
        # Percentage
        if len(df[df.Date == p]) != 0:
            percentages.append(sum(totals) / len(df[df.Date == p]))
        else: 
            percentages.append(0)
    if percentages[0] == 0 and percentages[1] == 0:
        ratio = 0
    elif percentages[0] == 0:
        # Big value
        ratio = 5
    else:
        ratio = percentages[1] / percentages[0]
    
    return ratio, s


def label_distribution_sorted(df, label, labelvalue, device):
    """ Plot label distribution for all users sorted 
        using 'statistics_total_added_info.csv' 
        For multiple labels, separate with '+' """
    peakdate = '2020-02-28'
    df = df.drop_duplicates()
    df = df[df['Date'] > '2019-12-25']
    nusers = df.User_PHQ9.nunique()
    df.loc[(df.Date < peakdate), 'Date'] = 'period1'
    df.loc[(df.Date >= peakdate) & 
           (df.Date != 'period1'), 'Date'] = 'period2'
    periods = ['period1', 'period2']
    dfall = pd.DataFrame(columns=['Ratio', 'Total'])
    for value, data in df.groupby('User_PHQ9'):
        dfuser = data
        # All periods inside Date values
        if 'period1' in dfuser.Date.values and \
           'period2' in dfuser.Date.values:
            r = round(ratio(dfuser, label, labelvalue, periods)[0], 3)
            totals = ratio(dfuser, label, labelvalue, periods)[1]
            dfratios = pd.DataFrame({'Ratio': r, 'Total': totals},
                                    index=[value])
            dfall = pd.concat([dfall, dfratios])
    dfall.index.rename('User_PHQ9', inplace=True)
    sns.set()
    # print(dfall)
    title = labelvalue + ' ' + label + \
        ' Ratios for all users in 2 time periods\n' + 'Device: ' + device + \
        ', Number of Users: ' + str(nusers) + '\n' + \
        'On the left: Total Number of ' + labelvalue + ' ' + label + \
        ' occurences.'
    # Aspect ratio of figure png
    w, h = figaspect(3 / 2)
    plt.figure(figsize=(w, h))    
    ax = plt.gca()
    dfall.Ratio.plot.barh(title=title, ax=ax)
    plt.axvline(x=1, linewidth=2, color='r')
    for i, v in enumerate(dfall.Total):
        # print(round(i, 1), round(v, 1))
        ax.text(-0.7, round(i, 1), str(v), color='blue', fontweight='bold')
    for i, v in enumerate(dfall.Ratio):
        ax.text(v + 0.1, round(i, 1), str(round(v, 2)), color='blue', fontweight='bold')
    plt.show()
    plt.close()


def multiline(dirname, device, label, plot, dynamics_variable):
    """ Different kind of plots """
    # Delete previous versions of .png files in directory
    os.chdir(dirname)
    for root, dirs, files in os.walk(os.getcwd(), topdown=False):
        for filename in files:
            os.chdir(os.path.abspath(root))
            if filename.endswith('.png'):
                os.remove(filename)

    os.chdir(dirname)
    for root, dirs, files in os.walk(os.getcwd(), topdown=False):
        for filename in files:
            os.chdir(os.path.abspath(root))
            # UserID is the name of parent directory of file
            userid = str(os.path.abspath(os.path.join(os.getcwd(), "./.")))\
                .split('/')[-1]
            if device == 'Android':
                if plot == 'evolution':
                    if filename.endswith('statistics_user.csv'):
                        data = pd.read_csv(filename)
                        df = pd.DataFrame(data)
                        if not df.empty:
                            evol(df, userid, device, label)
                elif plot == 'distribution':
                    if filename.endswith('statistics_user.csv'):
                        data = pd.read_csv(filename)
                        df = pd.DataFrame(data)
                        if not df.empty:
                            label_distribution(df, userid, device, label)
                elif plot == 'dynamics':
                    if filename.endswith('dynamics_user.csv'):
                        data = pd.read_csv(filename)
                        df = pd.DataFrame(data)
                        if not df.empty:
                            dynamics_distribution(df, userid, device, dynamics_variable)

            if device == 'iOS':
                if plot == 'evolution':
                    if filename.endswith('statistics_user_info_emotion.csv'):
                        data = pd.read_csv(filename)
                        df = pd.DataFrame(data)
                        if not df.empty:
                            evol(df, userid, device, label)
                elif plot == 'distribution':
                    if filename.endswith('statistics_user_info_emotion.csv'):
                        data = pd.read_csv(filename)
                        df = pd.DataFrame(data)
                        if not df.empty:
                            label_distribution(df, userid, device, label)
                elif plot == 'dynamics':
                    if filename.endswith('dynamics_user.csv'):
                        data = pd.read_csv(filename)
                        df = pd.DataFrame(data)
                        if not df.empty:
                            dynamics_distribution(df, userid, device, dynamics_variable)
                            
# Workflow

# os.chdir('/home/jason/Documents/Thesis/TypingData/iOS')
# os.chdir('/home/jason/Documents/Thesis/TypingData/Android')
# dirname = os.getcwd()
# os.chdir(dirname)

# multiline(os.getcwd(), 'Android', 'Mood')

# stat_without_keystrokes(os.path.abspath(dirname))
# emotion(os.getcwd())
# emotions_total_android(os.getcwd())
# emotions_total_ios(os.getcwd())

# stat_without_emotion(os.path.abspath(dirname))
# sessions(os.getcwd())
# sessions_total_android(os.getcwd())
# sessions_total_ios(os.getcwd())
