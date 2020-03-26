import os
import pandas as pd
import matplotlib.pyplot as plt 
import csv

# data = pd.read_csv('output_user.csv')
# df = pd.DataFrame(data)
# df = df.dropna()
# dftemp = df.group_by('Mood')

# boxplot = df.boxplot(column=['HT_Mean'], by='Mood')
# plt.show(boxplot)

# Function for creating 'statistics_user_without_emotion.csv'
# by merging all keystrokes sessions


def stat_without_emotion(dirname):
    os.chdir(dirname)
    for root, dirs, files in os.walk(os.getcwd(), topdown=False):
        for filename in files:
            os.chdir(os.path.abspath(root))
            if filename.endswith('statistics_user_without_emotion.csv'):
                os.remove(filename)

    os.chdir(dirname)
    for root, dirs, files in os.walk(os.getcwd(), topdown=False):
        for filename in files:
            os.chdir(os.path.abspath(root))
            if filename.endswith('statistics.csv'):
                data = pd.read_csv(filename)
                df = pd.DataFrame(data)
                # df = df.replace('.', '/')
                # Open .csv file and append statistics
                # Needed for header 
                os.chdir(os.path.abspath(os.path.join(os.getcwd(), "./..")))
                file_exists = os.path.isfile('./statistics_user_without_emotion.csv')
                with open('statistics_user_without_emotion.csv', 'a', newline='') \
                        as csvfile:
                    fieldnames = ['Keystrokes', 'Date']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    if not file_exists:
                        writer.writeheader()
                df.to_csv('statistics_user_without_emotion.csv', mode='a', index=False,
                          header=False)    
            
# Function for creating 'statistics_user_without_keystrokes.csv'
# by merging all 'emotion.csv'


def stat_without_keystrokes(dirname):
    os.chdir(dirname)
    for root, dirs, files in os.walk(os.getcwd(), topdown=False):
        for filename in files:
            os.chdir(os.path.abspath(root))
            if filename.endswith('statistics_user_without_keystrokes.csv'):
                os.remove(filename)

    os.chdir(dirname)
    for root, dirs, files in os.walk(os.getcwd(), topdown=False):
        for filename in files:
            os.chdir(os.path.abspath(root))
            if filename.endswith('emotion.csv'):
                data = pd.read_csv(filename)
                df = pd.DataFrame(data)
                # df = df.replace('.', '/')
                # Open .csv file and append statistics
                # Needed for header 
                os.chdir(os.path.abspath(os.path.join(os.getcwd(), "./..")))
                file_exists = \
                    os.path.isfile('./statistics_user_without_keystrokes.csv')
                with open('statistics_user_without_keystrokes.csv',
                          'a', newline='') as csvfile:
                    fieldnames = ['Mood', 'Physical_State', 'Date']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    if not file_exists:
                        writer.writeheader()
                df.to_csv('statistics_user_without_keystrokes.csv', mode='a', index=False,
                          header=False)    
        
# Function for looping across all users and plotting for each one
# their rate of sessions in time


def sessions(dirname):
    os.chdir(dirname)
    for root, dirs, files in os.walk(os.getcwd(), topdown=False):
        for filename in files:
            os.chdir(os.path.abspath(root))
            if filename.endswith('statistics_user_without_emotion.csv'):
                os.remove(filename)  

    os.chdir(dirname)
    for root, dirs, files in os.walk(os.getcwd(), topdown=False):
        for filename in files:
            os.chdir(os.path.abspath(root))
            if filename.endswith('statistics_user_without_emotion.csv'):          
                data = pd.read_csv('statistics_user_without_emotion.csv')
                df = pd.DataFrame(data)
                df = df[df['Keystrokes'] > 5]
                # print(len(df['Date'].value_counts()))
                if len(df['Date'].value_counts()) > 1:
                    id = str(os.path.abspath(os.path.join(os.getcwd(), "./.")))
                    id = id.split('/')[-1]
                    df['Date'].value_counts().sort_index().plot.line(title=id)
                    # plt.tight_layout()
                    plt.show()
                    # plt.gcf()
                    # print(os.getcwd())
                    # plt.savefig(os.getcwd() + '/figure.png')

# Function for looping across all users and plotting for each one
# their rate of emotions in time (incomplete!)


def emotion(dirname):
    os.chdir(dirname)
    for root, dirs, files in os.walk(os.getcwd(), topdown=False):
        for filename in files:
            os.chdir(os.path.abspath(root))
            if filename.endswith('figure.png'):
                os.remove(filename)  

    os.chdir(dirname)
    for root, dirs, files in os.walk(os.getcwd(), topdown=False):
        for filename in files:
            os.chdir(os.path.abspath(root))
            if filename.endswith('statistics_user_without_keystrokes.csv'):          
                data = pd.read_csv('statistics_user_without_keystrokes.csv')
                df = pd.DataFrame(data)
                df = df[df['Mood'] == 'Happy']
                # df = df[df['Keystrokes'] > 5]
                # print(len(df['Date'].value_counts()))
                if len(df['Date'].value_counts()) > 1:
                    id = str(os.path.abspath(os.path.join(os.getcwd(), "./.")))
                    id = id.split('/')[-1]
                    df['Date'].value_counts().sort_index().plot.line(title=id)
                    # plt.tight_layout()
                    plt.show()
                    # plt.gcf()
                    # print(os.getcwd())
                    # plt.savefig(os.getcwd() + '/figure.png')

# Function for creating 'statistics_total_sessions.csv' in iOS files
# by merging all 'statistics_user_without_emotions.csv'


def sessions_total_ios(dirname):
    os.chdir(dirname)
    for root, dirs, files in os.walk(os.getcwd(), topdown=False):
        for filename in files:
            os.chdir(os.path.abspath(root))
            if filename.endswith('statistics_user_without_emotion.csv'):
                data = pd.read_csv(filename)
                df = pd.DataFrame(data)
                os.chdir(dirname)
                # Open .csv file and append total statistics
                # Needed for header 
                file_exists = os.path.isfile('./statistics_total_sessions.csv')
                with open('statistics_total_sessions.csv',
                          'a', newline='') as csvfile:
                    fieldnames = ['Keystrokes', 'Date']        
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    if not file_exists:
                        writer.writeheader()
                df.to_csv('statistics_total_sessions.csv', mode='a', index=False,
                          header=False)

# Function for creating 'statistics_total_sessions.csv' in Android files
# by merging all 'statistics_user.csv'


def sessions_total_android(dirname):
    os.chdir(dirname)
    for root, dirs, files in os.walk(os.getcwd(), topdown=False):
        for filename in files:
            os.chdir(os.path.abspath(root))
            if filename.endswith('statistics_user.csv'):
                data = pd.read_csv(filename)
                df = pd.DataFrame(data)
                df = df[['Keystrokes', 'Date']]
                os.chdir(dirname)
                # Open .csv file and append total statistics
                # Needed for header 
                file_exists = os.path.isfile('./statistics_total_sessions.csv')
                with open('statistics_total_sessions.csv',
                          'a', newline='') as csvfile:
                    fieldnames = ['Keystrokes', 'Date']        
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    if not file_exists:
                        writer.writeheader()
                df.to_csv('statistics_total_sessions.csv', mode='a', index=False,
                          header=False)

# Function for creating 'statistics_total_emotions.csv' in iOS files
# by merging all 'statistics_user_without_keystrokes.csv'


def emotions_total_ios(dirname):
    os.chdir(dirname)
    for root, dirs, files in os.walk(os.getcwd(), topdown=False):
        for filename in files:
            os.chdir(os.path.abspath(root))
            if filename.endswith('statistics_user_without_keystrokes.csv'):
                data = pd.read_csv(filename)
                df = pd.DataFrame(data)
                os.chdir(dirname)
                # Open .csv file and append total statistics
                # Needed for header 
                file_exists = os.path.isfile('./statistics_total_emotions.csv')
                with open('statistics_total_emotions.csv',
                          'a', newline='') as csvfile:
                    fieldnames = ['Mood', 'Physical_State', 'Date']        
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    if not file_exists:
                        writer.writeheader()
                df.to_csv('statistics_total_emotions.csv', mode='a', index=False,
                          header=False)

# Function for creating 'statistics_total_emotions.csv' in Android files
# by merging all 'statistics_user.csv'


def emotions_total_android(dirname):
    os.chdir(dirname)
    for root, dirs, files in os.walk(os.getcwd(), topdown=False):
        for filename in files:
            os.chdir(os.path.abspath(root))
            if filename.endswith('statistics_user.csv'):
                data = pd.read_csv(filename)
                df = pd.DataFrame(data)
                df = df[['Mood', 'Physical_State', 'Date']]
                os.chdir(dirname)
                # Open .csv file and append total statistics
                # Needed for header 
                file_exists = os.path.isfile('./statistics_total_emotions.csv')
                with open('statistics_total_emotions.csv',
                          'a', newline='') as csvfile:
                    fieldnames = ['Mood', 'Physical_State', 'Date']        
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    if not file_exists:
                        writer.writeheader()
                df.to_csv('statistics_total_emotions.csv', mode='a', index=False,
                          header=False)

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


def evol(df, name):
    df = clean(df)
    # Keep only Mood and Date columns
    df = df[['Mood', 'Date']]
    df['Date'] = pd.to_datetime(df['Date'])
    df = df[df['Date'] > '2019.09.01']
    df = df.groupby(df.columns.tolist()).size().reset_index().\
        rename(columns={0: 'records'})
    df = df.pivot(index='Date', columns='Mood', values='records')
    df = df.fillna(0)
    userid = str(os.path.abspath(os.path.join(os.getcwd(), "./.")))
    userid = userid.split('/')[-1]
    title = 'UserID: ' + userid + ', Device: iOS'
    if not df.empty:
        if len(df.columns) > 1:
            df.plot(linewidth=4, title=title)
        else:
            if len(df) == 1:
                df.plot.bar(title=title)
        plt.gcf()
        # print(os.getcwd())
        os.chdir('/home/jason/Documents/Thesis/TypingData/iOS/Plots')
        plt.savefig(os.getcwd() + '/' + name + '.png')
        # plt.show()
    else:
        print('DF is empty')
# Loop across files in directory


def multiline(dirname):
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
            userid = str(os.path.abspath(os.path.join(os.getcwd(), "./.")))
            userid = userid.split('/')[-1]
            # Android
            # if filename.endswith('statistics_user.csv'):
            # iOS
            if filename.endswith('statistics_user_without_keystrokes.csv'):
                data = pd.read_csv(filename)
                df = pd.DataFrame(data)
                df = clean(df)
                if not df.empty:
                    evol(df, userid)
        

# Workflow


os.chdir('/home/jason/Documents/Thesis/TypingData/iOS')
dirname = os.getcwd()
os.chdir(dirname)
multiline(os.getcwd())

# stat_without_keystrokes(os.path.abspath(dirname))
# emotion(os.getcwd())
# emotions_total_android(os.getcwd())
# emotions_total_ios(os.getcwd())

# stat_without_emotion(os.path.abspath(dirname))
# sessions(os.getcwd())
# sessions_total_android(os.getcwd())
# sessions_total_ios(os.getcwd())