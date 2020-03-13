# statisticsios.py
#
# Script for extracting statistics of session data
# from .json file to DataFrames
# for iOS devices
#
# Iason Ofeidis 2019

import json
import pandas as pd 
# import numpy as np 
# import sys
import os
import csv
# import matplotlib.pyplot as plt
# import math

# Function for extracting typing session data
# from .json file to .csv file


def keystrokes(jsonFile):
    # Data Acquisition from JSON files
    with open(jsonFile) as json_file:
        datasession = json.load(json_file)

    # Length of Characters
    keystrokes = datasession['sumOfCharacters']

    # Duration
    # duration = datasession['keyboardDownTime'] - datasession['keyboardDownTime'] 

    stat = {'Keystrokes': keystrokes}

    return stat


def emotion(jsonFile):
    # Data Acquisition from JSON files
    with open(jsonFile) as json_file:
        datasession = json.load(json_file)


    # ?Mood and Physical State?
    # Current Mood
    mood = datasession['currentMood']
    # print(mood)
    # Current Physical State
    physicalstate = datasession['currentPhysicalState']
    # print(physicalstate)

    stat = {'Mood': mood, 'Physical_State': physicalstate}

    return stat


def info(jsonFile):
    # Data Acquisition from JSON files
    with open(jsonFile) as json_file:
        datasession = json.load(json_file)

    # UserID
    userid = datasession['userDeviceID']
    # UserAge
    userage = datasession['userAge']
    # UserGender
    usergender = datasession['userGender']
    # UserPHQ9
    # userphq9 = datasession['userPhq9Score']
    # UserDeficiency
    # userdeficiency = datasession['userDeficiency']
    # UserMedication
    # usermedication = datasession['userMedication']


    stat = {'UserID': userid, 'User_Age': userage,
            'User_Gender': usergender}

    # df = pd.read_json(jsonFile, orient = 'index')
    df = pd.DataFrame.from_dict([stat])

    return df

# Function for looping across all files in a directory


def filesextract(dirname):
    # os.chdir("d:\\tmp")
    os.chdir(dirname)

    # Remove existing .csv files
    for root, dirs, files in os.walk(dirname, topdown=False):
        for filename in files:
            # print(os.path.join(root, filename))
            os.chdir(os.path.abspath(root))
            if filename.endswith('.csv'):
                os.remove(filename)

    # Loop across all files and create output.csv and statistics.csv
    # containing typingdata of all sessions in a day                
    os.chdir(os.path.abspath(dirname))
    for root, dirs, files in os.walk(os.getcwd(), topdown=False):
        for filename in files:
            os.chdir(os.path.abspath(root))
            # Session-Keystrokes file 'timestamp.json'
            if filename.startswith('Emotion') and\
               filename.endswith('.json'):
                statistics = emotion(filename)
                # Open .csv  file and append statistics 
                file_exists = os.path.isfile('./emotion.csv')
                with open('emotion.csv', 'a', newline='') as csvfile:
                    fieldnames = statistics.keys()        
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    if not file_exists:
                        writer.writeheader()
                    writer.writerow(statistics)
            # print(os.path.join(root, filename))
            os.chdir(os.path.abspath(root))
            # Session-Keystrokes file 'timestamp.json'
            if (not filename.startswith('Emotion')) and \
               (not filename.startswith('RawData')) and\
               (not filename.startswith('Info')) and\
               filename.endswith('.json'):
                statistics = keystrokes(filename)

                # Open .csv file and append statistics 
                file_exists = os.path.isfile('./statistics.csv')
                
                with open('statistics.csv', 'a', newline='') as csvfile:
                    fieldnames = statistics.keys()        
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    if not file_exists:
                        writer.writeheader()
                    writer.writerow(statistics)
            
    # Create statistics.csv by merging all .csv in folders below
    os.chdir(dirname)
    flagstat = flagemotion = False
    pathstat = os.path.abspath('/home')
    pathemotion = os.path.abspath('/home/jason')
    for root, dirs, files in os.walk(dirname, topdown=False):
        os.chdir(dirname)
        for filename in files:
            # print(os.path.join(root, filename))
            os.chdir(os.path.abspath(root))
            if filename.endswith('statistics.csv'):
                data = pd.read_csv(filename)
                fieldnames = ['Keystrokes']
                dfstat = pd.DataFrame(data)
                pathstat = os.path.abspath(root)
                flagstat = True
                # print('pathstat is ' + os.path.join(root, filename))
            elif filename.endswith('emotion.csv'):
                data = pd.read_csv(filename)
                fieldnames = ['Mood', 'Physical_State']
                dfemotion = pd.DataFrame(data)
                pathemotion = os.path.abspath(root)
                flagemotion = True
                # print('pathemotion is ' + os.path.join(root, filename))
            if pathstat == pathemotion and filename.endswith('.csv'):
                # print('pathstat == pathemotion')
                if flagstat and flagemotion:
                    # print('flagstat == flagemotion')
               
                    os.chdir(dirname)

                    df = pd.concat([dfstat, dfemotion], axis=1)
                    # Propagation to fill empty emotions
                    df = df.fillna(method='ffill')

                    # Open .csv file and append statistics
                    # Needed for header 
                    file_exists = os.path.isfile('./statistics_user.csv')
                
                    with open('statistics_user.csv', 'a', newline='') as csvfile:
                        fieldnames = ['Keystrokes', 'Mood', 'Physical_State']
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        if not file_exists:
                            writer.writeheader()

                    df.to_csv('statistics_user.csv', mode='a', index=False,
                              header=False)

                    flagemotion = False
                    flagstat = False
                    # pathstat = os.path.abspath('/home')
                    # pathinfo = os.path.abspath('/home/jason')
            elif pathstat != pathemotion and filename.endswith('.csv'):
                # print('pathstat != pathemotion')
                # print('pathstat is ' + pathstat)
                # print('pathemotion is ' + pathemotion)
                flagstat = False
                # flagemotion = False
        

# Function for looping across all users


def users(dirname):
    os.chdir(dirname)


    # Remove existing .csv files
    for root, dirs, files in os.walk(dirname, topdown=False):
        for filename in files:
            # print(os.path.join(root, filename))
            os.chdir(os.path.abspath(root))
            if filename.endswith('.csv'):
                os.remove(filename)

    os.chdir(dirname)
    for root, dirs, files in os.walk(dirname, topdown=False):
        for dir in dirs:
            # Only user files
            if ('2020' not in dir) and ('2019' not in dir):
                # print(os.path.join(root, filename))
                os.chdir(os.path.join(root, dir))
                # print(os.path.join(root,dir))
                # print(dir)
                filesextract(os.path.join(root, dir))

    os.chdir(dirname)
    # Some variables need to be initialized
    flagstat = flaginfo = False
    pathstat = os.path.abspath('/home')
    pathinfo = os.path.abspath('/home/jason')
    for root, dirs, files in os.walk(dirname, topdown=False):
        for filename in files:
            os.chdir(os.path.abspath(root))
            if filename.endswith('user.csv'):
                dfstat = process(filename)
                # print(dfstat)
                pathstat = os.path.abspath(root)
                flagstat = True

            elif filename.endswith('Info.json'):
                dfinfo = info(filename)
                # dfinfo = dfinfo.transpose()
                pathinfo = os.path.abspath(root)
                flaginfo = True

            if pathstat == pathinfo:
                if flagstat and flaginfo:
                    os.chdir(dirname)
                    # Open .csv file and append total statistics
                    # Needed for header 
                    file_exists = os.path.isfile('./statistics_total.csv')
                    df = pd.concat([dfinfo, dfstat], axis=1)
                    # Propagation to fill empty emotions
                    df = df.fillna(method='ffill')
                    # print(df)

                    with open('statistics_total.csv', 'a', newline='') as csvfile:
                        fieldnames = ['UserID', 'User_Age', 'User_Gender',
                                      'Keystrokes_Mean', 'Happy',
                                      'Sad', 'Neutral', 'Postponing', 'undefined',
                                      'Sessions_Number']        
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        if not file_exists:
                            writer.writeheader()

                    df.to_csv('statistics_total.csv', mode='a', index=False,
                              header=False)

                    flagstat = False
                    flaginfo = False    
            elif pathstat != pathinfo: 
                # info.json is first accessed in every folder
                flaginfo = False
            
# Function for processing DataFrame of typing data


def process(csvfile):
    data = pd.read_csv(csvfile)
    df = pd.DataFrame(data)
    sessionsnumber = len(df)
    # kf = df.head(1)
    # userid = kf.squeeze('rows')['UserID']
    # userage = kf.squeeze('rows')['User_Age']
    # usergender = kf.squeeze('rows')['User_Gender']
    keystrokesmean = round(df['Keystrokes'].mean(), 2)
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
                  'Sad': sad, 'Neutral': neutral, 'Postponing': postponing,
                  'Undefined': undefined, 'Sessions_Number': sessionsnumber}

    # fieldnames = ['Keystrokes_Mean', 'Happy',\
    #              'Sad', 'Neutral', 'Postponing', 'undefined',
    #             'Sessions_Number']
    df = pd.DataFrame.from_dict([statistics])
    return df


