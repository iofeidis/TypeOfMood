# plots.py
# Script for generating statistics plots
# Iason Ofeidis 2020

import os
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
# import csv

# Clean one dataframe from 'Postponing, undefined, TIMEOUT' values


def clean(df):
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

# Plotting the evolution of Mood labels in time
# Just change label and device variables


def evol(df, name, device, label):
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
        plt.show()
        plt.close()

# Plotting the evolution of Mood labels in time
# Just change label and device variables


def label_distribution(df, name, device, label):
    # Clean df from undefined, Postponing, TIMEOUT values
    df = clean(df)
    # Keep only sessions with NumberOfKeystrokes > 5
    # df = df[df['Keystrokes'] > 5]
    # Keep only label and Date columns
    df = df[[label, 'Date']]
    # Keep only recent sessions
    df = df[df['Date'] > '2019-12-25']
    df = df.drop_duplicates()
    df.loc[(df.Date < '2020-01-25'), 'Date'] = 'period1'
    df.loc[(df.Date >= '2020-01-25') & 
           (df.Date < '2020-02-28') & 
           (df.Date != 'period1'), 'Date'] = 'period2'
    df.loc[(df.Date >= '2020-02-28') & 
           (df.Date != 'period1') &
           (df.Date != 'period2'), 'Date'] = 'period3'
    df = df.sort_values(by=['Date'])

    userid = str(os.path.abspath(os.path.join(os.getcwd(), "./.")))\
        .split('/')[-1]
    title = 'UserID: ' + userid + ', Device: ' + device
    if not df.empty:
        if (df.Date.nunique() > 1):
            # print(len(df))
            df.groupby(label).Date.value_counts().unstack(1).plot.barh(title=title)
            plt.gcf()
            # os.chdir('/home/jason/Documents/Thesis/TypingData/' + device + '/Plots')
            # plt.savefig(os.getcwd() + '/' + name + label + '.png')
            plt.show()
            plt.close()


def dynamics_distribution(df, name, device):
    """ Plot the distribution of keystroke dynamics in 3 periods"""
    df = df.dropna()
    # Keep only recent sessions
    df = df[df['Date'] > '2019-12-25']
    df.loc[(df.Date < '2020-01-25'), 'Date'] = 'period1'
    df.loc[(df.Date >= '2020-01-25') & 
           (df.Date < '2020-02-28') & 
           (df.Date != 'period1'), 'Date'] = 'period2'
    df.loc[(df.Date >= '2020-02-28') & 
           (df.Date != 'period1') &
           (df.Date != 'period2'), 'Date'] = 'period3'
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
    
    # Keep only users with all 3 periods
    if not df.empty and ('period1' in df.Date.values) and \
                        ('period3' in df.Date.values):
        # fig, axs = plt.subplots(2, 1)
        sns.set() 
        # df.Hold_Time.hist(by=df.Date)
        os.chdir('/home/jason/Documents/Thesis/TypingData/' + device + '/Plots')
        sns.violinplot(y=df.Date, x=df.Hold_Time, bw=.2).set_title(title)
        # plt.savefig(os.getcwd() + '/' + name + '_ht.png')
        plt.show()
        plt.close()
        sns.violinplot(y=df.Date, x=df.Flight_Time, bw=.2).set_title(title)
        # plt.savefig(os.getcwd() + '/' + name + '_ft.png')
        plt.show()
        plt.close()
        sns.violinplot(y=df.Date, x=df.Speed, bw=.2).set_title(title)
        # plt.savefig(os.getcwd() + '/' + name + '_sp.png')
        plt.show()
        plt.close()
        sns.violinplot(y=df.Date, x=df.Press_Flight_Rate, bw=.2).set_title(title)
        # plt.savefig(os.getcwd() + '/' + name + '_pfr.png')
        plt.show()
        plt.close()
        print('------------------------------------------------------------')

    return

# Loop across files in directory


def multiline(dirname, device, label, plot):
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
                            dynamics_distribution(df, userid, device)

            if device == 'iOS':
                if plot == 'evolution':
                    if filename.endswith('statistics_user_without_keystrokes.csv'):
                        data = pd.read_csv(filename)
                        df = pd.DataFrame(data)
                        if not df.empty:
                            evol(df, userid, device, label)
                elif plot == 'distribution':
                    if filename.endswith('statistics_user_without_keystrokes.csv'):
                        data = pd.read_csv(filename)
                        df = pd.DataFrame(data)
                        if not df.empty:
                            label_distribution(df, userid, device, label)
                elif plot == 'dynamics':
                    if filename.endswith('dynamics_user.csv'):
                        data = pd.read_csv(filename)
                        df = pd.DataFrame(data)
                        if not df.empty:
                            dynamics_distribution(df, userid, device)

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
