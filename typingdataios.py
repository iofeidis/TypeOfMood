# typingdataios.py
#
# Script for extracting typing session data
# from .json file to DataFrames
# for iOS devices
#
# Iason Ofeidis 2019

# TO DO:
#     - 0 < flight time < 3000 ms (3 sec)
#     - 0 < hold time < 300 ms (0.3 sec)
#     - sumOfCharacters > 5 
#  Sessions > 10

# FEATURES (33)
#   (statistical characteristics)
#   Mean, Median, Std. Deviation, Skewness, Kurtosis
#     1) Hold Time 
#     2) Flight Time 
#     3) Pressure (No Values?)
#     4) Accelerometer Magnitude
#     5) Accelerometer Angle
#     6) Gyroscope Magnitude
#   (plain values)
#   probably not useful for ML
#     7) Duration
#     8) Length
#     9) Delete Rate

import json
import pandas as pd 
import numpy as np 
import sys
import os
import csv
import matplotlib.pyplot as plt
import math

# Function for extracting typing session data
# from .json file to .csv file

def keystrokes(jsonFile):
    #Data Acquisition from JSON files
    with open(jsonFile) as json_file:
        datasession = json.load(json_file)

    #DownTime
    datadown =(datasession['startTimeOfKeyPressed'])
    #Uptime
    dataup = (datasession['stopTimeOfKeyPressed'])
    #Euclidean Distance
    distance = datasession['distanceBetweenKeys']
    #Deliberately Long Pressed Button
    islongpress = datasession['longPressed']
    #PressureValues
    pressure = datasession['pressureMax']
    # print(islongpress)



    # #ht: HoldTime, ft: FlightTime
    # #am: AccelerometerMagnitude, aa: AccelerometerAngle,
    # #gm: GyroscopeMagnitude, pv: Pressure Values
    # ht = []
    # ft = []
    # am = []
    # aa = []
    # gm = []
    # pv = []

    # length = datasession['sumOfCharacters']

    # for p in range(length):
    #     if p<length-1:
    #         #FlightTime < 0 are omitted from the sequences
    #         #HoldTime > 300 are excluded from the sequences
    #         # map function
    #         if ((datadown[p+1] - dataup[p]) > 0) and (islongpress[p]== 0):
    #             ft.append(datadown[p+1] - dataup[p])
    #             ht.append(dataup[p] - datadown[p])
    #             pv.append(pressure[p])
    #     else: break

    #Total Number of Characters
    #?is length(ht) == sumOfCharacters?
    # length = len(ht)

    # for p in range(length-1):
    #     sp.append(distance[p]/ft[p])
    #     pfr.append(ht[p]/ft[p])
    
    # dr: Delete Rate
    # dr = (datasession['NumDels'])/length

    #Duration of Session (in msec)
    # duration = datasession['StopDateTime']-datasession['StartDateTime']

    # length = len(rawValues['accelerometerX'])

    #Not needed right now
    # for p in range(length):
    #     if p<length-1:
    #         #AccelerometerMagnitude
    #         x = np.array([rawValues['accelerometerX'],\
    #             rawValues['accelerometerY'],rawValues['accelerometerZ']])
    #         am.append(np.linarg.norm(x))
    #         #AccelerometerAngle in degrees
    #         x = np.array([rawValues['accelerometerX'],\
    #             rawValues['accelerometerY'])
    #         denum = np.linarg.norm(x)
    #         y = rawValues['accelerometerZ']/denum
    #         aa.append(np.arctan(y*(180/np.pi)))
    #         #GyroscopeMagnitude
    #         x = np.array([rawValues['gyroscopeX'],\
    #             rawValues['gyroscopeY'],rawValues['gyroscopeZ']])
    #         gm.append(np.linarg.norm(x))
    #     else: break
    
    #dr: Delete Rate
    # dr = (datasession['NumDels'])/length

    #Length of Characters
    keystrokes = datasession['sumOfCharacters']

    #Duration
    # duration = datasession['keyboardDownTime'] - datasession['keyboardDownTime'] 

    s = pd.Series([keystrokes], \
        index = ['Keystrokes'])

    stat = {'Keystrokes':keystrokes}

    return stat


def emotion(jsonFile):
    #Data Acquisition from JSON files
    with open(jsonFile) as json_file:
        datasession = json.load(json_file)


    #?Mood and Physical State?
    #Current Mood
    mood = datasession['currentMood']
    # print(mood)
    #Current Physical State
    physicalstate = datasession['currentPhysicalState']
    # print(physicalstate)

    s = pd.Series([mood, physicalstate], \
        index = ['Mood', 'Physical_State'])

    stat = {'Mood':mood, 'Physical_State':physicalstate}

    return stat

def info(jsonFile):
    # #Data Acquisition from JSON files
    with open(jsonFile) as json_file:
        datasession = json.load(json_file)

    #UserID
    userid = datasession['userDeviceID']
    #UserAge
    userage = datasession['userAge']
    #UserGender
    usergender = datasession['userGender']
    #UserPHQ9
    # userphq9 = datasession['userPhq9Score']
    #UserDeficiency
    # userdeficiency = datasession['userDeficiency']
    #UserMedication
    # usermedication = datasession['userMedication']

    s = pd.Series([userid, userage, usergender], \
        index = ['UserID', 'User_Age', 'User_Gender'])

    stat = {'UserID':userid, 'User_Age':userage,\
         'User_Gender':usergender}

    # df = pd.read_json(jsonFile, orient = 'index')
    df = pd.DataFrame.from_dict([stat])

    return df

#Function for looping across all files in a directory
def filesextract(dirname):
    # os.chdir("d:\\tmp")
    os.chdir(dirname)

    #Remove existing .csv files
    for root, dirs, files in os.walk(dirname, topdown = False):
        for filename in files:
            # print(os.path.join(root, filename))
            os.chdir(os.path.abspath(root))
            if filename.endswith('.csv'):
                os.remove(filename)

    #Loop across all files and create output.csv and statistics.csv
    #containing typingdata of all sessions in a day                
    os.chdir(os.path.abspath(dirname))
    for root, dirs, files in os.walk(os.getcwd(), topdown = False):
        for filename in files:
            os.chdir(os.path.abspath(root))
            # Session-Keystrokes file 'timestamp.json'
            if filename.startswith('Emotion') and\
                filename.endswith('.json'):
                
                statistics = emotion(filename)
                #Open .csv  file and append statistics 
                file_exists = os.path.isfile('./emotion.csv')
                
                with open('emotion.csv', 'a', newline='') as csvfile:
                    fieldnames = statistics.keys()        
                    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
                    if not file_exists:
                        writer.writeheader()
                    writer.writerow(statistics)
            
        
            #print(os.path.join(root, filename))
            os.chdir(os.path.abspath(root))
            #Session-Keystrokes file 'timestamp.json'
            if (not filename.startswith('Emotion')) and \
                (not filename.startswith('RawData')) and\
                (not filename.startswith('Info')) and\
                    filename.endswith('.json'):
                statistics = keystrokes(filename)

                #Open .csv file and append statistics 
                file_exists = os.path.isfile('./statistics.csv')
                
                with open('statistics.csv', 'a', newline='') as csvfile:
                    fieldnames = statistics.keys()        
                    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
                    if not file_exists:
                        writer.writeheader()
                    writer.writerow(statistics)
            
        
            


    #Create statistics.csv by merging all .csv in folders below
    os.chdir(dirname)
    flagstat = flagemotion = False
    for root, dirs, files in os.walk(dirname, topdown = False):
        os.chdir(dirname)
        for filename in files:
            # print(os.path.join(root, filename))
            os.chdir(os.path.abspath(root))
            if filename.endswith('statistics.csv'):
                data = pd.read_csv(filename)
                fieldnames = ['Keystrokes']
                dfstat = pd.DataFrame(data)
                flagstat = True
            elif filename.endswith('emotion.csv'):
                data = pd.read_csv(filename)
                fieldnames = ['Mood', 'Physical_State']
                dfemotion = pd.DataFrame(data)
                flagemotion = True
            if flagstat and flagemotion:
                os.chdir(dirname)

                df = pd.concat([dfstat,dfemotion], axis = 1)
                #Propagation to fill empty emotions
                df = df.fillna(method = 'ffill')

                #Open .csv file and append statistics
                #Needed for header 
                file_exists = os.path.isfile('./statistics_user.csv')
            
                with open('statistics_user.csv', 'a', newline='') as csvfile:
                    fieldnames = ['Keystrokes', 'Mood', 'Physical_State']
                    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
                    if not file_exists:
                        writer.writeheader()

                df.to_csv('statistics_user.csv', mode = 'a', index = False,\
                            header = False)

                flagemotion = False
                flagstat = False
        

#Function for looping across all users
def users(dirname):

    #Remove existing .csv files
    for root, dirs, files in os.walk(dirname, topdown = False):
        for filename in files:
            # print(os.path.join(root, filename))
            os.chdir(os.path.abspath(root))
            if filename.endswith('.csv'):
                os.remove(filename)

    os.chdir(dirname)
    for root, dirs, files in os.walk(dirname, topdown = False):
        for dir in dirs:
            if ('2020' not in dir) and ('2019' not in dir):
                # print(os.path.join(root, filename))
                os.chdir(os.path.join(root,dir))
                # print(os.path.join(root,dir))
                # print(dir)
                filesextract(os.path.join(root,dir))

    os.chdir(dirname)
    flagstat = flaginfo = False
    for root, dirs, files in os.walk(dirname, topdown = False):
        for filename in files:
            os.chdir(os.path.abspath(root))
            if filename.endswith('user.csv'):
                dfstat = process(filename)
                flagstat = True
            elif filename.endswith('Info.json'):
                dfinfo = info(filename)
                # dfinfo = dfinfo.transpose()
                flaginfo = True
            if flagstat and flaginfo:
                os.chdir(dirname)
                #Open .csv file and append total statistics
                #Needed for header 
                file_exists = os.path.isfile('./statistics_total.csv')
                
                df = pd.concat([dfinfo,dfstat], axis = 1)
                #Propagation to fill empty emotions
                df = df.fillna(method = 'ffill')
                print(df)

                with open('statistics_total.csv', 'a', newline='') as csvfile:
                    fieldnames = ['UserID','User_Age', 'User_Gender',\
                            'Keystrokes_Mean', 'Happy',\
                        'Sad', 'Neutral', 'Postponing', 'undefined']        
                    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
                    if not file_exists:
                        writer.writeheader()

                df.to_csv('statistics_total.csv', mode = 'a', index = False,\
                            header = False)

                flagstat = False
                flaginfo = False
        
          
#Function for processing DataFrame of typing data
def process(csvfile):
    data = pd.read_csv(csvfile)
    df = pd.DataFrame(data)
    # kf = df.head(1)
    # userid = kf.squeeze('rows')['UserID']
    # userage = kf.squeeze('rows')['User_Age']
    # usergender = kf.squeeze('rows')['User_Gender']
    keystrokesmean = df['Keystrokes'].mean()
    happy = len(df[df['Mood'] == 'Happy']) + \
            len(df[df['Mood'] == 'Happy TIMEOUT'])
    sad = len(df[df['Mood'] == 'Sad']) + \
            len(df[df['Mood'] == 'Sad TIMEOUT'])
    neutral = len(df[df['Mood'] == 'Neutral']) + \
        len(df[df['Mood'] == 'Neutral TIMEOUT'])
    postponing = len(df[df['Mood'] == 'Postponing']) + \
            len(df[df['Mood'] == 'Postponing TIMEOUT'])
    undefined = len(df[df['Mood'] == 'undefined']) + \
            len(df[df['Mood'] == 'undefined TIMEOUT'])
            
    statistics = {'Keystrokes_Mean': keystrokesmean, 'Happy': happy,
            'Sad': sad,'Neutral':neutral, 'Postponing': postponing,
             'Undefined':undefined}

    fieldnames = ['Keystrokes_Mean', 'Happy',\
                 'Sad', 'Neutral', 'Postponing', 'undefined']
    df = pd.DataFrame.from_dict([statistics])
    return df


