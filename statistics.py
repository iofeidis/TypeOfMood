# statistics.py
#
# Script for extracting statistics of session data
# from .json file to DataFrames
# for Android devices
#
# Iason Ofeidis 2019

import json
import pandas as pd 
# import numpy as np 
# import sys
import os
import csv
# import matplotlib.pyplot as plt

# Function for extracting typing session data
# from .json file to .csv file
#


def extract(jsonFile):
    # Data Acquisition from JSON files
    with open(jsonFile) as json_file:
        data = json.load(json_file)
    # Keeping only SESSION_DATA from json file
    datasession = json.loads(data['SESSION_DATA'])

    # Current Mood
    mood = datasession['CurrentMood']
    # Current Physical State
    physicalstate = datasession['CurrentPhysicalState']
    # DownTime
    datadown = (datasession['DownTime'])
    
    # UserID
    userid = data['USER_ID']
    # UserAge
    userage = data['USER_AGE']
    # UserGender
    usergender = data['USER_GENDER']

    # Total Number of Characters
    length = len(datadown)

    # dr: Delete Rate
    # dr = (datasession['NumDels']) / length

    # Duration of Session (in msec)
    # duration = datasession['StopDateTime'] - datasession['StartDateTime']
    # Insert session statistics into Statistics Dictionary
    statistics = {'UserID': userid, 'User_Age': userage,
                  'User_Gender': usergender, 'Keystrokes': length,
                  'Mood': mood, 'Physical_State': physicalstate}

    # Open statistics.csv file and append statistics
    file_exists = os.path.isfile('./statistics.csv')
    with open('statistics.csv', 'a', newline='') as csvfile:
        fieldnames = statistics.keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(statistics)

    return

# Function for looping across all files in a directory


def filesextract(dirname):
    os.chdir(dirname)

    # Remove existing statistics related .csv files
    for root, dirs, files in os.walk(dirname, topdown=False):
        for filename in files:
            # print(os.path.join(root, filename))
            os.chdir(os.path.abspath(root))
            if filename.endswith('statistics.csv') or \
               filename.endswith('statistics_user.csv'):
                os.remove(filename)

    # Loop across all files and create output.csv and statistics.csv
    # containing typingdata of all sessions in a day
    os.chdir(dirname)
    for root, dirs, files in os.walk(dirname, topdown=False):
        for filename in files:
            os.chdir(os.path.abspath(root))
            if filename.endswith('.json'):
                extract(filename)

    # Create statistics.csv by merging all .csv in folders below
    os.chdir(dirname)
    for root, dirs, files in os.walk(dirname, topdown=False):
        os.chdir(dirname)
        for filename in files:
            os.chdir(os.path.abspath(root))
            if filename.endswith('statistics.csv'):
                data = pd.read_csv(filename)
                fieldnames = ['UserID', 'User_Age', 'User_Gender',
                              'Keystrokes', 'Mood', 'Physical_State']
                df = pd.DataFrame(data)
                os.chdir(dirname)
                # Open .csv file and append statistics
                # Needed for header
                file_exists = os.path.isfile('./statistics_user.csv')
                with open('statistics_user.csv', 'a', newline='') as csvfile:
                    fieldnames = ['UserID', 'User_Age', 'User_Gender',
                                  'Keystrokes', 'Mood', 'Physical_State']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    if not file_exists:
                        writer.writeheader()
                df.to_csv('statistics_user.csv', mode='a', index=False,
                          header=False)
    return

# Function for looping across all users


def users(dirname):
    os.chdir(dirname)
    # Remove existing .csv files
    for root, dirs, files in os.walk(dirname, topdown=False):
        for filename in files:
            os.chdir(os.path.abspath(root))
            if filename.endswith('statistics.csv') or\
               filename.endswith('statistics_user.csv') or\
               filename.endswith('statistics_total.csv'):
                os.remove(filename)

    os.chdir(dirname)
    for root, dirs, files in os.walk(dirname, topdown=False):
        for dir in dirs:
            # If directory refers to user and not a day of sessions
            if ('2020' not in dir) and ('2019' not in dir):
                os.chdir(os.path.join(root, dir))
                filesextract(os.path.join(root, dir))

    os.chdir(dirname)
    for root, dirs, files in os.walk(dirname, topdown=False):
        for filename in files:
            os.chdir(os.path.abspath(root))
            if filename.endswith('statistics_user.csv'):
                df = process(filename)
                os.chdir(dirname)
                # Open .csv file and append total statistics
                # Needed for header
                file_exists = os.path.isfile('./statistics_total.csv')            
                with open('statistics_total.csv', 'a', newline='') as csvfile:
                    fieldnames = ['UserID', 'User_Age', 'User_Gender',
                                  'Keystrokes_Mean', 'Happy',
                                  'Sad', 'Neutral', 'Stressed',
                                  'Postponing', 'undefined',
                                  'Session_Number']        
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    if not file_exists:
                        writer.writeheader()

                df.to_csv('statistics_total.csv', mode='a', index=False,
                          header=False)
    return

# ?Preprocessing?
# Remove duplicates

# Function for processing DataFrame of typing data
# Opens 'statistics_user.csv' and saves it to DataFrame


def process(csvfile):
    data = pd.read_csv(csvfile)
    df = pd.DataFrame(data)
    kf = df.head(1)
    sessionsnumber = len(df)
    userid = kf.squeeze('rows')['UserID']
    userage = kf.squeeze('rows')['User_Age']
    usergender = kf.squeeze('rows')['User_Gender']
    keystrokesmean = round(df['Keystrokes'].mean(), 2)
    happy = len(df[df['Mood'] == 'Happy']) + \
        len(df[df['Mood'] == 'Happy TIMEOUT'])
    sad = len(df[df['Mood'] == 'Sad']) + \
        len(df[df['Mood'] == 'Sad TIMEOUT'])
    neutral = len(df[df['Mood'] == 'Neutral']) + \
        len(df[df['Mood'] == 'Neutral TIMEOUT'])
    stressed = len(df[df['Mood'] == 'Stressed']) + \
        len(df[df['Mood'] == 'Stressed TIMEOUT'])
    postponing = len(df[df['Mood'] == 'Postponing']) + \
        len(df[df['Mood'] == 'Postponing TIMEOUT'])
    undefined = len(df[df['Mood'] == 'undefined']) + \
        len(df[df['Mood'] == 'undefined TIMEOUT'])            
    statistics = {'UserID': userid, 'User_Age': userage,
                  'User_Gender': usergender,
                  'Keystrokes_Mean': keystrokesmean, 'Happy': happy,
                  'Sad': sad, 'Neutral': neutral, 'Stressed': stressed,
                  'Postponing': postponing,
                  'Undefined': undefined, 'Sessions_Number': sessionsnumber}

    df = pd.DataFrame.from_dict([statistics])
    return df
