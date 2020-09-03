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
#     Probably will not use these ones: 
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

    # DownTime
    datadown = (datasession['startTimeOfKeyPressed'])
    # Uptime
    dataup = (datasession['stopTimeOfKeyPressed'])
    # Euclidean Distance
    distance = datasession['distanceBetweenKeys']
    # Deliberately Long Pressed Button
    islongpress = datasession['longPressed']
    # PressureValues
    pressure = datasession['pressureMax']
    # print(islongpress)



    # #ht: HoldTime, ft: FlightTime
    # #am: AccelerometerMagnitude, aa: AccelerometerAngle,
    # #gm: GyroscopeMagnitude, pv: Pressure Values (Normalized)
    ht = []
    ft = []
    sp = []
    pfr = []
    # am = []
    # aa = []
    # gm = []
    pv = []

    length = datasession['sumOfCharacters']
    for p in range(length - 1):
        # 0 < flight time < 3000 ms (3 sec)
        # 0 < hold time < 300 ms (0.3 sec)
        tempft = datadown[p + 1] - dataup[p]
        tempht = dataup[p] - datadown[p]
        if tempft > 0 and tempft < 3 and\
           tempht > 0 and tempht < .3 and\
           (not islongpress[p]):
            ft.append(tempft)
            ht.append(tempht)
            if p < len(pressure):
                pv.append(pressure[p])
    
    # Pressure Values Issue
    if not pv:
        pv.append(0)
    
    # Total Number of Characters
    # ?is length(ht) == sumOfCharacters?
    lengthht = len(ht)
    lengthft = len(ft)
    lengthdis = len(distance)
    minlength = min(lengthht, lengthft, lengthdis)

    for p in range(minlength - 1):
        sp.append(distance[p] / ft[p])
        pfr.append(ht[p] / ft[p])
    
    # dr: Delete Rate
    # if length > 0:
    #     dr = (datasession['backSpaceCounter']) / length
    # else:
    #     dr = 0
    # Duration of Session (in sec)
    # duration = datasession['sessionTime']

    # length = len(rawValues['accelerometerX'])

    # Not needed right now
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


    # Convert data lists to Panda.Series
    htseries = pd.Series(ht)
    ftseries = pd.Series(ft)
    spseries = pd.Series(sp)
    pfrseries = pd.Series(pfr)
    # pvseries = pd.Series(pv)

    # Is not used in analysis
    # Mean of each Series
    htmean = htseries.mean()
    ftmean = ftseries.mean()
    spmean = spseries.mean()
    pfrmean = pfrseries.mean()
    # pvmean = pvseries.mean()

    # Median of each Series
    # htmedian = htseries.median()
    # ftmedian = ftseries.median()
    # spmedian = spseries.median()
    # pfrmedian = pfrseries.median()
    # pvmedian = pvseries.median()

    # Standard Deviation of each Series
    htstd = htseries.std()
    ftstd = ftseries.std()
    spstd = spseries.std()
    pfrstd = pfrseries.std()
    # pvstd = pvseries.std()

    # Skewness of each Series
    htskew = htseries.skew()
    ftskew = ftseries.skew()
    spskew = spseries.skew()
    pfrskew = pfrseries.skew()
    # pvskew = pvseries.skew()

    # Kurtosis of each Series
    htkurtosis = htseries.kurtosis()
    ftkurtosis = ftseries.kurtosis()
    spkurtosis = spseries.kurtosis()
    pfrkurtosis = pfrseries.kurtosis()
    # pvkurtosis = pvseries.kurtosis()

    # Date
    tmp = str((os.path.basename(os.getcwd())))
    try1 = tmp.split('.')
    date = try1[2] + '-' + try1[1] + '-' + try1[0]
    
    stat = {'HT_Mean': htmean, 'HT_STD': htstd,
            'HT_Skewness': htskew, 'HT_Kurtosis': htkurtosis,
            'FT_Mean': ftmean, 'FT_STD': ftstd,
            'FT_Skewness': ftskew, 'FT_Kurtosis': ftkurtosis,
            'SP_Mean': spmean, 'SP_STD': spstd,
            'SP_Skewness': spskew, 'SP_Kurtosis': spkurtosis,
            'PFR_Mean': pfrmean, 'PFR_STD': pfrstd,
            'PFR_Skewness': pfrskew, 'PFR_Kurtosis': pfrkurtosis,
            # 'PV_Mean': pvmean, 'PV_Median': pvmedian, 'PV_STD': pvstd,
            # 'PV_Skewness': pvskew, 'PV_Kurtosis': pvkurtosis,
            # 'Duration': duration,
            # 'Delete_Rate': dr, 
            'Length': length,
            'Date': date}

    return stat


def emotion(jsonFile):
    # Data Acquisition from JSON files
    with open(jsonFile) as json_file:
        datasession = json.load(json_file)

    # ?Mood and Physical State?
    # Current Mood
    mood = datasession['currentMood']
    # Current Physical State
    physicalstate = datasession['currentPhysicalState']

    stat = {'Mood': mood, 'Physical_State': physicalstate}

    return stat


def info(jsonFile):
    # Data Acquisition from JSON files
    with open(jsonFile) as json_file:
        datasession = json.load(json_file)

    # UserID
    userid = datasession['userDeviceID']
    # UserAge
    # userage = datasession['userAge']
    # UserGender
    # usergender = datasession['userGender']
    # UserPHQ9
    userphq9 = datasession['userPhq9Score']
    # UserDeficiency
    # userdeficiency = datasession['userDeficiency']
    # UserMedication
    # usermedication = datasession['userMedication']

    stat = {'UserID': userid,
            # 'User_Age': userage, 'User_Gender': usergender,
            'User_PHQ9': userphq9}

    # df = pd.read_json(jsonFile, orient = 'index')
    df = pd.DataFrame.from_dict([stat])

    return df

# Function for looping across all files in a directory


def filesextract(dirname):
    os.chdir(dirname)

    # Remove existing .csv files
    for root, dirs, files in os.walk(dirname, topdown=False):
        for filename in files:
            os.chdir(os.path.abspath(root))
            if filename.endswith('output.csv') or\
               filename.endswith('output_user.csv') or\
               filename.endswith('emotion.csv'):
                os.remove(filename)

    # Loop across all files and create output.csv and output.csv
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
            os.chdir(os.path.abspath(root))
            # Session-Keystrokes file 'timestamp.json'
            if (not filename.startswith('Emotion')) and \
               (not filename.startswith('RawData')) and\
               (not filename.startswith('Info')) and\
               filename.endswith('.json'):
                statistics = keystrokes(filename)

                # Open .csv file and append statistics 
                file_exists = os.path.isfile('./output.csv')
                
                with open('output.csv', 'a', newline='') as csvfile:
                    fieldnames = statistics.keys()        
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    if not file_exists:
                        writer.writeheader()
                    writer.writerow(statistics)
            
    # Create output_user.csv by merging all .csv in folders below
    os.chdir(dirname)
    # Some variables need to be initialized
    flagstat = flagemotion = False
    pathstat = os.path.abspath('/home')
    pathemotion = os.path.abspath('/home/jason')
    for root, dirs, files in os.walk(dirname, topdown=False):
        os.chdir(dirname)
        for filename in files:
            os.chdir(os.path.abspath(root))
            if filename.endswith('output.csv'):
                data = pd.read_csv(filename)
                fieldnames = ['HT_Mean', 'HT_STD', 'HT_Skewness',
                              'HT_Kurtosis', 'FT_Mean', 'FT_STD',
                              'FT_Skewness', 'FT_Kurtosis', 'SP_Mean',
                              'SP_STD', 'SP_Skewness',
                              'SP_Kurtosis', 'PFR_Mean',
                              'PFR_STD', 'PFR_Skewness', 'PFR_Kurtosis',
                              # 'PV_Mean', 'PV_Median', 'PV_STD', 'PV_Skewness',
                              # 'PV_Kurtosis',
                              # 'Duration',
                              # 'Delete_Rate', 
                              'Length',
                              'Date']
                dfstat = pd.DataFrame(data)
                pathstat = os.path.abspath(root)
                flagstat = True
            elif filename.endswith('emotion.csv'):
                data = pd.read_csv(filename)
                fieldnames = ['Mood', 'Physical_State']
                dfemotion = pd.DataFrame(data)
                pathemotion = os.path.abspath(root)
                flagemotion = True
            # 'output.csv' and 'emotion.csv' need to be from the
            # same folder 
            if pathstat == pathemotion and filename.endswith('.csv'):
                # one folder must have both 'emotion.csv' and
                # 'output.csv' to be considered for analysis
                if flagstat and flagemotion:
                    os.chdir(dirname)
                    df = pd.concat([dfstat, dfemotion], axis=1)
                    # Propagation to fill empty emotions
                    df.Mood = df.Mood.fillna(method='ffill')
                    df.Physical_State = df.Physical_State.fillna(method='ffill')
                    # Open .csv file and append statistics
                    # Needed for header 
                    file_exists = os.path.isfile('./output_user.csv')
                    with open('output_user.csv', 'a', newline='') as csvfile:
                        fieldnames = ['HT_Mean', 'HT_STD',
                                      'HT_Skewness', 'HT_Kurtosis', 'FT_Mean',
                                      'FT_STD',
                                      'FT_Skewness', 'FT_Kurtosis', 'SP_Mean',
                                      'SP_STD', 'SP_Skewness',
                                      'SP_Kurtosis', 'PFR_Mean',
                                      'PFR_STD', 'PFR_Skewness', 'PFR_Kurtosis',
                                      # 'PV_Mean', 'PV_Median', 'PV_STD',
                                      # 'PV_Skewness', 'PV_Kurtosis',
                                      # 'Duration',
                                      # 'Delete_Rate', 
                                      'Length', 
                                      'Date',
                                      'Mood', 'Physical_State']
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        if not file_exists:
                            writer.writeheader()
                    df = df[df['Length'] > 5].reset_index(drop=True)    
                    df.to_csv('output_user.csv', mode='a', index=False,
                              header=False)

                    flagemotion = False
                    flagstat = False
            elif pathstat != pathemotion and filename.endswith('.csv'):
                # 'output.csv' is first accessed in every folder
                flagstat = False

# Function for looping across all users


def users(dirname):
    os.chdir(dirname)
    # Remove existing .csv files
    for root, dirs, files in os.walk(dirname, topdown=False):
        for filename in files:
            os.chdir(os.path.abspath(root))
            if filename.endswith('output.csv') or\
               filename.endswith('output_user.csv') or\
               filename.endswith('emotion.csv') or\
               filename.endswith('output_total.csv'):
                os.remove(filename)

    os.chdir(dirname)
    for root, dirs, files in os.walk(dirname, topdown=False):
        for dir in dirs:
            # Only user files
            if ('2020' not in dir) and ('2019' not in dir):
                os.chdir(os.path.join(root, dir))
                filesextract(os.path.join(root, dir))

    os.chdir(dirname)
    # Some variables need to be initialized
    flagstat = flaginfo = False
    pathstat = os.path.abspath('/home')
    pathinfo = os.path.abspath('/home/jason')
    for root, dirs, files in os.walk(dirname, topdown=False):
        for filename in files:
            os.chdir(os.path.abspath(root))
            if filename.endswith('output_user.csv'):
                dfstat = process(filename)
                pathstat = os.path.abspath(root)
                flagstat = True
            elif filename.endswith('Info.json'):
                dfinfo = info(filename)
                pathinfo = os.path.abspath(root)
                flaginfo = True
            # 'output_user.csv' and 'Info.json' need to be from the
            # same folder
            if pathstat == pathinfo:
                # one folder must have both 'Info.csv' and
                # 'output_user.csv' to be considered for analysis
                if flagstat and flaginfo:
                    os.chdir(dirname)
                    # Open .csv file and append total statistics
                    # Needed for header 
                    file_exists = os.path.isfile('./output_total.csv')
                    df = pd.concat([dfinfo, dfstat], axis=1)
                    # Propagation to fill empty emotions
                    df.UserID = df.UserID.fillna(method='ffill')
                    with open('output_total.csv', 'a', newline='') as csvfile:
                        fieldnames = ['UserID', 'User_PHQ9',
                                      # 'User_Age', 'User_Gender',
                                      'HT_Mean', 'HT_STD',
                                      'HT_Skewness',
                                      'HT_Kurtosis', 'FT_Mean',
                                      'FT_STD',
                                      'FT_Skewness', 'FT_Kurtosis', 'SP_Mean',
                                      'SP_STD', 'SP_Skewness',
                                      'SP_Kurtosis', 'PFR_Mean',
                                      'PFR_STD', 'PFR_Skewness', 'PFR_Kurtosis',
                                      # 'PV_Mean', 'PV_Median', 'PV_STD',
                                      # 'PV_Skewness',
                                      # 'PV_Kurtosis',
                                      # 'Duration',
                                      # 'Delete_Rate', 
                                      'Length', 
                                      'Date',
                                      'Mood', 'Physical_State']        
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        if not file_exists:
                            writer.writeheader()

                    df.to_csv('output_total.csv', mode='a', index=False,
                              header=False)

                    flagstat = False
                    flaginfo = False    
            elif pathstat != pathinfo:
                # info.json is first accessed in every folder
                # flaginfo = False
                flagstat = False

# Function for processing DataFrame of typing data


def process(csvfile):
    data = pd.read_csv(csvfile)
    df = pd.DataFrame(data)
    # Keep only sessions with NumberOfCharacters > 5
    df = df[df['Length'] > 5].reset_index(drop=True)
    # Keep only sessions with label (mood != undefined)
    df = df[(df['Mood'] != 'undefined') & 
            (df['Mood'] != 'undefined TIMEOUT')].reset_index(drop=True)
    df = df.round(4)
    # Keep only users with number of sessions > 10
    if len(df) < 10:
        # It's an empty df with just columns
        df = pd.DataFrame(columns=df.columns)
    # print(df)
    return df
