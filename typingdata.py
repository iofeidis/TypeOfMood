# typingdata.py
#
# Script for extracting typing session data
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

# jsonFile = sys.argv[0]

# Function for extracting typing session data
# from .json file to .csv file
#


def extract(jsonFile):
    # Data Acquisition from JSON files
    with open(jsonFile) as json_file:
        data = json.load(json_file)
    # print(data.keys())
    # Keeping only SESSION_DATA from json file
    datasession = json.loads(data['SESSION_DATA'])
    # print(datasession.keys())

    # Current Mood
    mood = datasession['CurrentMood']
    # print(mood)
    # Current Physical State
    physicalstate = datasession['CurrentPhysicalState']
    # print(mood)

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

    # UserID
    userid = data['USER_ID']
    # # UserAge
    # userage = data['USER_AGE']
    # # UserGender
    # usergender = data['USER_GENDER']
    # UserPhq9
    userphq9 = data['USER_PHQ9']

    # ht: HoldTime, ft: FlightTime
    # sp: Speed, pfr: Press-Flight-Rate
    # pv: Pressure Values
    ht = []
    ft = []
    sp = []
    pfr = []
    # pv = []

    length = len(datadown)

    # TO DO:
    #     - 0 < flight time < 3000 ms (3 sec)
    #     - 0 < hold time < 300 ms (0.3 sec)
    #     - sumOfCharacters > 5
    # Sessions > 10

    # FEATURES (19)
    #   (statistical characteristics)
    #   Median, Std. Deviation, Skewness, Kurtosis
    #     1) Hold Time
    #     2) Flight Time
    #     3) Speed
    #     4) Pressure-Flight Rate
    #   (plain values)
    #   probably not useful for ML
    #     5) Duration
    #     6) Length
    #     7) Delete Rate

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

    for p in range(length - 1):
        sp.append(distance[p] / ft[p])
        pfr.append(ht[p] / ft[p])
        
    # dr: Delete Rate
    if length > 0:
        dr = (datasession['NumDels']) / length
    else:
        dr = 0
    # Duration of Session (in msec)
    # duration = datasession['StopDateTime'] - datasession['StartDateTime']

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
    htmedian = htseries.median()
    ftmedian = ftseries.median()
    spmedian = spseries.median()
    pfrmedian = pfrseries.median()
    # pvmean = pvseries.mean()

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
    # Plot data
    # htseries.plot.box()
    # plt.show()
    # print(htstd)
    # print(htskew)
    # print(htkurtosis)
    # Insert Characteristics into Variables Dictionary
    variables = {'UserID': userid, 'User_PHQ9': userphq9,
                 'HT_Mean': htmean, 'HT_Median': htmedian, 'HT_STD': htstd,
                 'HT_Skewness': htskew, 'HT_Kurtosis': htkurtosis,
                 'FT_Mean': ftmean, 'FT_Median': ftmedian, 'FT_STD': ftstd,
                 'FT_Skewness': ftskew, 'FT_Kurtosis': ftkurtosis,
                 'SP_Mean': spmean, 'SP_Median': spmedian, 'SP_STD': spstd,
                 'SP_Skewness': spskew, 'SP_Kurtosis': spkurtosis,
                 'PFR_Mean': pfrmean, 'PFR_Median': pfrmedian, 'PFR_STD': pfrstd,
                 'PFR_Skewness': pfrskew, 'PFR_Kurtosis': pfrkurtosis,
                 # 'PV_Mean': pvmean, 'PV_Median': pvmedian, 'PV_STD': pvstd,
                 # 'PV_Skewness': pvskew, 'PV_Kurtosis': pvkurtosis,
                 # 'Duration': duration,
                 'Delete_Rate': dr,
                 'Length': length,
                 'Mood': mood, 'Physical_State': physicalstate}

    # Open .csv file and append variables
    file_exists = os.path.isfile('./output.csv')

    with open('output.csv', 'a', newline='') as csvfile:
        fieldnames = variables.keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(variables)

    return

# Function for looping across all files in a directory


def filesextract(dirname):
    # os.chdir("d:\\tmp")
    os.chdir(dirname)

    # Remove existing .csv files
    for root, dirs, files in os.walk(dirname, topdown=False):
        for filename in files:
            # print(os.path.join(root, filename))
            os.chdir(os.path.abspath(root))
            if filename.endswith('output.csv') or \
               filename.endswith('output_user.csv'):
                os.remove(filename)


    # Loop across all files and create output.csv and output.csv
    # containing typingdata of all sessions in a day
    os.chdir(dirname)
    for root, dirs, files in os.walk(dirname, topdown=False):
        for filename in files:
            # print(os.path.join(root, filename))
            os.chdir(os.path.abspath(root))
            if filename.endswith('.json'):
                # print(filename)
                extract(filename)

    # Create output.csv by merging all .csv in folders below
    os.chdir(dirname)
    for root, dirs, files in os.walk(dirname, topdown=False):
        os.chdir(dirname)
        for filename in files:
            # print(os.path.join(root, filename))
            os.chdir(os.path.abspath(root))
            if filename.endswith('output.csv'):
                data = pd.read_csv(filename)
                df = pd.DataFrame(data)
                # print(output)
                os.chdir(dirname)

                # os.chdir(os.path.join(root,dir))
                os.chdir(dirname)
                # Open .csv file and append output
                # Needed for header
                file_exists = os.path.isfile('./output_user.csv')
                with open('output_user.csv', 'a', newline='') as csvfile:
                    fieldnames = ['UserID', 'User_PHQ9', 
                                  'HT_Mean', 'HT_Median', 'HT_STD', 'HT_Skewness',
                                  'HT_Kurtosis', 'FT_Mean', 'FT_Median', 'FT_STD',
                                  'FT_Skewness', 'FT_Kurtosis', 'SP_Mean',
                                  'SP_Median', 'SP_STD', 'SP_Skewness',
                                  'SP_Kurtosis', 'PFR_Mean', 'PFR_Median',
                                  'PFR_STD', 'PFR_Skewness', 'PFR_Kurtosis',
                                  # 'PV_Mean', 'PV_Median', 'PV_STD', 'PV_Skewness',
                                  # 'PV_Kurtosis',
                                  # 'Duration',
                                  'Delete_Rate',
                                  'Length',
                                  'Mood', 'Physical_State']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    if not file_exists:
                        writer.writeheader()

                df.to_csv('output_user.csv', mode='a', index=False,
                          header=False)
    return

# Function for looping across all users


def users(dirname):
    os.chdir(dirname)

    # Remove existing .csv files
    for root, dirs, files in os.walk(dirname, topdown=False):
        for filename in files:
            # print(os.path.join(root, filename))
            os.chdir(os.path.abspath(root))
            if filename.endswith('output.csv') or\
               filename.endswith('output_user.csv') or\
               filename.endswith('output_total.csv'):
                os.remove(filename)

    os.chdir(dirname)
    for root, dirs, files in os.walk(dirname, topdown=False):
        for dir in dirs:
            if ('2020' not in dir) and ('2019' not in dir):
                # print(os.path.join(root, filename))
                os.chdir(os.path.join(root, dir))
                # print(os.path.join(root,dir))
                # print(dir)
                filesextract(os.path.join(root, dir))

    os.chdir(dirname)
    for root, dirs, files in os.walk(dirname, topdown=False):
        for filename in files:
            os.chdir(os.path.abspath(root))
            if filename.endswith('output_user.csv'):
                df = process(filename)
                os.chdir(dirname)
                # Open .csv file and append total output
                # Needed for header
                file_exists = os.path.isfile('./output_total.csv')            
                with open('output_total.csv', 'a', newline='') as csvfile:
                    fieldnames = ['UserID', 'User_PHQ9', 
                                  'HT_Mean', 'HT_Median', 'HT_STD', 'HT_Skewness',
                                  'HT_Kurtosis', 'FT_Mean', 'FT_Median', 'FT_STD',
                                  'FT_Skewness', 'FT_Kurtosis', 'SP_Mean',
                                  'SP_Median', 'SP_STD', 'SP_Skewness',
                                  'SP_Kurtosis', 'PFR_Mean', 'PFR_Median',
                                  'PFR_STD', 'PFR_Skewness', 'PFR_Kurtosis',
                                  # 'PV_Mean', 'PV_Median', 'PV_STD', 'PV_Skewness',
                                  # 'PV_Kurtosis',
                                  # 'Duration',
                                  'Delete_Rate',
                                  'Length',
                                  'Mood', 'Physical_State']        
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    if not file_exists:
                        writer.writeheader()

                df.to_csv('output_total.csv', mode='a', index=False,
                          header=False)
    return

# ?Preprocessing?
# Remove duplicates

# Function for processing DataFrame of typing data
# Opens 'output_user.csv' and saves it to df


def process(csvfile):
    data = pd.read_csv(csvfile)
    df = pd.DataFrame(data)
    # Keep only sessions with NumberOfCharacters > 5
    df = df[df['Length'] > 5].reset_index(drop=True)
    # Keep only sessios with label (mood != undefined)
    # and (mood != Postponing)
    df = df[(df['Mood'] != 'undefined') & 
            (df['Mood'] != 'undefined TIMEOUT') &
            (df['Mood'] != 'Postponing') & 
            (df['Mood'] != 'Postponing TIMEOUT')].reset_index(drop=True)
    df = df.round(4)
    # Keep only users with number of sessions > 10
    if len(df) < 10:
        df = pd.DataFrame(columns=df.columns)
    return df
