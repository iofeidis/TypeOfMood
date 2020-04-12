# statisticsall.py
# Script for creating all kinds of statistics.csv
# Iason Ofeidis 2020

import os
import pandas as pd
# import matplotlib.pyplot as plt 
import csv
import json
import patientsfind



def stat_without_emotion(dirname):
    """ Function for creating 'statistics_user_without_emotion.csv'
        by merging all keystrokes sessions"""
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


def stat_without_keystrokes(dirname):
    """ Function for creating 'statistics_user_without_keystrokes.csv'
        by merging all 'emotion.csv'"""
    os.chdir(dirname)
    for root, dirs, files in os.walk(os.getcwd(), topdown=False):
        for filename in files:
            os.chdir(os.path.abspath(root))
            if filename.endswith('statistics_user_without_keystrokes.csv') or \
               filename.endswith('statistics_user_info_emotion.csv'):
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
    
    os.chdir(dirname)
    for root, dirs, files in os.walk(os.getcwd(), topdown=False):
        for filename in files:
            os.chdir(os.path.abspath(root))
            if filename.endswith('Info.json'):
                data = patientsfind.info(filename)
                df = pd.DataFrame([data])
                dfinfo = df.User_PHQ9
                # df = df.replace('.', '/')
                # Open .csv file and append statistics
                # Needed for header 
                # os.chdir(os.path.abspath(os.path.join(os.getcwd(), "./..")))
                file_exists = \
                    os.path.isfile('./statistics_user_without_keystrokes.csv')
                if file_exists:
                    data = pd.read_csv('statistics_user_without_keystrokes.csv')
                    dfstat = pd.DataFrame(data)

                    df = pd.concat([dfinfo, dfstat], ignore_index=True, axis=1)
                    df = df.fillna(method='ffill')
                    file_exists = \
                        os.path.isfile('./statistics_user_info_emotion.csv')
                    with open('statistics_user_info_emotion.csv',
                              'w', newline='') as csvfile:
                        fieldnames = ['User_PHQ9', 'Mood', 'Physical_State', 'Date']
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        if not file_exists:
                            writer.writeheader()
                    df.to_csv('statistics_user_info_emotion.csv', mode='a', index=False,
                              header=False)
                
    os.chdir(dirname)
    for root, dirs, files in os.walk(os.getcwd(), topdown=False):
        for filename in files:
            os.chdir(os.path.abspath(root))
            if filename.endswith('statistics_user_without_keystrokes.csv'):
                os.remove(filename)
            


def sessions_total_ios(dirname):
    """ Function for creating 'statistics_total_sessions.csv' in iOS files
        by merging all 'statistics_user_without_emotions.csv'"""
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


def sessions_total_android(dirname):
    """ Function for creating 'statistics_total_sessions.csv' in Android files
        by merging all 'statistics_user.csv'"""
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


def emotions_total_ios(dirname):
    """ Function for creating 'statistics_total_emotions.csv' in iOS files
        by merging all 'statistics_user_without_keystrokes.csv'"""
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


def emotions_total_android(dirname):
    """ Function for creating 'statistics_total_emotions.csv' in Android files
        by merging all 'statistics_user.csv'"""
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


def statistics_add(dirname):
    """ Just add all 'statistics_user.csv' to a single .csv file"""
    os.chdir(dirname)
    for root, dirs, files in os.walk(os.getcwd(), topdown=False):
        for filename in files:
            os.chdir(os.path.abspath(root))
            # change filename depending on plots
            if filename.endswith('statistics_user_info_emotion.csv'):
                data = pd.read_csv(filename)
                df = pd.DataFrame(data)
                df = df[['User_PHQ9', 'Mood', 'Physical_State', 'Date']]
                os.chdir(dirname)
                # Open .csv file and append total statistics
                # Needed for header 
                file_exists = os.path.isfile('./statistics_total_added_info.csv')
                with open('statistics_total_added_info.csv',
                          'a', newline='') as csvfile:
                    fieldnames = ['User_PHQ9', 
                                  'Mood', 'Physical_State', 'Date']        
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    if not file_exists:
                        writer.writeheader()
                df.to_csv('statistics_total_added_info.csv', mode='a', index=False,
                          header=False)


def dynamics(jsonFile, device):
    """Gather all keystroke dynamics of user in a single .csv"""
    if device == 'Android':
        # Data Acquisition from JSON files
        with open(jsonFile) as json_file:
            data = json.load(json_file)
        # Keeping only SESSION_DATA from json file
        datasession = json.loads(data['SESSION_DATA'])
        # Date of Session
        date = data['DATE_DATA']
        # Format: Y-M-d
        date = date.split(',')[0]
        
        # DownTime
        datadown = (datasession['DownTime'])
        # Uptime
        dataup = (datasession['UpTime'])
        # Euclidean Distance
        distance = datasession['Distance']
        # Deliberately Long Pressed Button
        islongpress = datasession['IsLongPress']
        # PressureValues
        # pressure = datasession['PressureValue']
        # print(islongpress)
    elif device == 'iOS':
        # Data Acquisition from JSON files
        with open(jsonFile) as json_file:
            datasession = json.load(json_file)

        # DownTime
        datadown = (datasession['startTimeOfKeyPressed'])
        # Uptime
        dataup = (datasession['stopTimeOfKeyPressed'])
        # Euclidean Distance
        distance = datasession['distanceBetweenKeys']
        # Deliberately Long Pressed Button
        islongpress = datasession['longPressed']
        # PressureValues
        # pressure = datasession['pressureMax']
        # print(islongpress)
        # Date
        tmp = str((os.path.basename(os.getcwd())))
        try1 = tmp.split('.')
        date = try1[2] + '-' + try1[1] + '-' + try1[0]

    # ht: HoldTime, ft: FlightTime
    # sp: Speed, pfr: Press-Flight-Rate
    # pv: Pressure Values
    ht = []
    ft = []
    sp = []
    pfr = []
    # pv = []

    length = len(datadown)

    for p in range(length - 1):
        # 0 < flight time < 3000 ms (3 sec)
        # 0 < hold time < 300 ms (0.3 sec)
        tempft = datadown[p + 1] - dataup[p]
        tempht = dataup[p] - datadown[p]
        if tempft > 0 and tempft < 3000 and\
           tempht > 0 and tempht < 300 and\
           (islongpress[p] == 0):
            ft.append(tempft)
            ht.append(tempht)
            # pv.append(pressure[p])
        
    # Total Number of Characters
    length = len(ht)
    lengthht = len(ht)
    lengthft = len(ft)
    lengthdis = len(distance)
    minlength = min(lengthht, lengthft, lengthdis)


    for p in range(minlength - 1):
        sp.append(distance[p] / ft[p])
        pfr.append(ht[p] / ft[p])
        
    # dr: Delete Rate
    # if length > 0:
    #     dr = (datasession['NumDels']) / length
    # else:
    #     dr = 0
    # # Duration of Session (in msec)
    # duration = datasession['StopDateTime'] - datasession['StartDateTime']

    # Convert data lists to Panda.Series
    htseries = pd.Series(ht)
    ftseries = pd.Series(ft)
    spseries = pd.Series(sp)
    pfrseries = pd.Series(pfr)
    # pvseries = pd.Series(pv)

    # Insert Characteristics into Variables Dictionary
    variables = {'Hold_Time': htseries, 'Flight_Time': ftseries,
                 'Speed': spseries, 'Press_Flight_Rate': pfrseries,
                 'Date': date}

    df = pd.DataFrame({key: pd.Series(value) for key, value in variables.items()})
    df.Date = df.Date.fillna(method='ffill')

    # Open .csv file and append statistics
    # Needed for header
    file_exists = os.path.isfile('./dynamics.csv')
    with open('dynamics.csv', 'a', newline='') as csvfile:
        fieldnames = ['Hold_Time', 'Flight_Time', 'Speed',
                      'Press_Flight_Rate', 'Date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
    
    df.to_csv('dynamics.csv', mode='a', index=False,
              header=False)
    return


def dynamics_add(dirname, device):
    """ Just add all 'dynamics.csv' to a single 'dynamics_user.csv' file"""
    # Remove existing statistics related .csv files
    for root, dirs, files in os.walk(dirname, topdown=False):
        for filename in files:
            # print(os.path.join(root, filename))
            os.chdir(os.path.abspath(root))
            if filename.endswith('dynamics.csv') or \
               filename.endswith('dynamics_user.csv'):
                os.remove(filename)

    if device == 'Android':
        # Loop across all files and create dynamics.csv
        # containing typingdata of all sessions in a day
        os.chdir(dirname)
        for root, dirs, files in os.walk(dirname, topdown=False):
            for filename in files:
                os.chdir(os.path.abspath(root))
                if filename.endswith('.json'):
                    dynamics(filename, device)
                    

        # Create dynamics_user.csv
        os.chdir(dirname)
        for root, dirs, files in os.walk(os.getcwd(), topdown=False):
            for filename in files:
                os.chdir(os.path.abspath(root))
                if filename.endswith('dynamics.csv'):
                    data = pd.read_csv(filename)
                    df = pd.DataFrame(data)
                    os.chdir(dirname)
                    # Open .csv file and append total statistics
                    # Needed for header 
                    file_exists = os.path.isfile('./dynamics_user.csv')
                    with open('dynamics_user.csv',
                              'a', newline='') as csvfile:
                        fieldnames = ['Hold_Time', 'Flight_Time', 'Speed',
                                      'Press_Flight_Rate', 'Date']      
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        if not file_exists:
                            writer.writeheader()
                    df.to_csv('dynamics_user.csv', mode='a', index=False,
                              header=False)
    elif device == 'iOS':
        # Loop across all files and create dynamics.csv
        # containing typingdata of all sessions in a day
        os.chdir(dirname)
        for root, dirs, files in os.walk(dirname, topdown=False):
            for filename in files:
                os.chdir(os.path.abspath(root))
                if (not filename.startswith('Emotion')) and \
                   (not filename.startswith('RawData')) and\
                   (not filename.startswith('Info')) and\
                   filename.endswith('.json'):
                    # print(filename)
                    dynamics(filename, device)
                    

        # Create dynamics_user.csv
        os.chdir(dirname)
        for root, dirs, files in os.walk(os.getcwd(), topdown=False):
            for filename in files:
                os.chdir(os.path.abspath(root))
                if filename.endswith('dynamics.csv'):
                    data = pd.read_csv(filename)
                    df = pd.DataFrame(data)
                    os.chdir(dirname)
                    # Open .csv file and append total statistics
                    # Needed for header 
                    file_exists = os.path.isfile('./dynamics_user.csv')
                    with open('dynamics_user.csv',
                              'a', newline='') as csvfile:
                        fieldnames = ['Hold_Time', 'Flight_Time', 'Speed',
                                      'Press_Flight_Rate', 'Date']      
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        if not file_exists:
                            writer.writeheader()
                    df.to_csv('dynamics_user.csv', mode='a', index=False,
                              header=False)
    
    return


def dynamics_users(dirname, device):
    """Loop across all users for dynamics_user.csv"""

    if device == 'Android':
        os.chdir(dirname)
        for root, dirs, files in os.walk(dirname, topdown=False):
            for dir in dirs:
                # If directory refers to user and not a day of sessions
                if ('2020' not in dir) and ('2019' not in dir):
                    os.chdir(os.path.join(root, dir))
                    dynamics_add(os.path.join(root, dir), device)
    elif device == 'iOS':
        os.chdir(dirname)
        for root, dirs, files in os.walk(dirname, topdown=False):
            for dir in dirs:
                # If directory refers to user and not a day of sessions
                if ('2020' not in dir) and ('2019' not in dir):
                    os.chdir(os.path.join(root, dir))
                    dynamics_add(os.path.join(root, dir), device)


def stat_info_emotion(dirname):
    os.chdir(dirname)
    for root, dirs, files in os.walk(os.getcwd(), topdown=False):
        for filename in files:
            os.chdir(os.path.abspath(root))
            if filename.endswith('statistics_user_info_emotion.csv'):
                os.remove(filename)

    os.chdir(dirname)
    for root, dirs, files in os.walk(os.getcwd(), topdown=False):
        for filename in files:
            os.chdir(os.path.abspath(root))
            if filename.endswith('statistics_user_without_keystrokes.csv'):
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


def dynamics_total(dirname, device):
    """ Merge all dynamics_user.csv into a single dynamics_total.csv"""
    peakdate = '2020-02-28'
    if device == 'Android':
        print('DO STH')
    elif device == 'iOS':
        os.chdir(dirname)
        dfall = pd.DataFrame([])
        for root, dirs, files in os.walk(os.getcwd(), topdown=True):
            for filename in files:
                os.chdir(os.path.abspath(root))
                if filename.endswith('dynamics_user.csv'):
                    data = pd.read_csv(filename)
                    dfstat = pd.DataFrame(data)
                    userphq9 = -1
                    userid = \
                        str(os.path.abspath(os.path.join(os.getcwd(), "./.")))\
                        .split('/')[-1]
                    for rootb, dirsb, filesb in os.walk(os.getcwd(), topdown=True):
                        for filenameb in filesb:
                            if filenameb.endswith('Info.json'):
                                userphq9 = patientsfind.info(filenameb)['User_PHQ9']
                    dfstat = dfstat[dfstat['Date'] > '2019-12-25']
                    dfstat.loc[(dfstat.Date < peakdate), 'Date'] = 'period1'
                    dfstat.loc[(dfstat.Date >= peakdate) & 
                               (dfstat.Date != 'period1'), 'Date'] = 'period2'
                    if 'period1' in dfstat.Date.values and \
                       'period2' in dfstat.Date.values:
                        for value, dfdate in dfstat.groupby('Date'):
                            stat = {'UserID': userid, 'User_PHQ9': userphq9,
                                    'HT_Mean': dfdate.Hold_Time.mean(), 
                                    'Date': value}
                            df1 = pd.DataFrame([stat])
                            dfall = pd.concat([dfall, df1])
        dfall = dfall.reset_index(drop=True)
        print(dfall.head(40))
                    


# Workflow

# stat_without_keystrokes(os.path.abspath(dirname))
# emotion(os.getcwd())
# emotions_total_android(os.getcwd())
# emotions_total_ios(os.getcwd())

# stat_without_emotion(os.path.abspath(dirname))
# sessions(os.getcwd())
# sessions_total_android(os.getcwd())
# sessions_total_ios(os.getcwd())


