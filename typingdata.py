# typingdata.py
#
# Script for extracting typing session data
# from .json file to DataFrames
#
# Iason Ofeidis 2019

import json
import pandas as pd 
import numpy as np 
import sys
import os
import csv
import matplotlib.pyplot as plt

# jsonFile = sys.argv[0]

# Function for extracting typing session data
# from .json file to .csv file
#
def extract(jsonFile):
    #Data Acquisition from JSON files
    with open(jsonFile) as json_file:
        data = json.load(json_file)
    # print(data.keys())
    #Keeping only SESSION_DATA from json file
    datasession = json.loads(data['SESSION_DATA'])
    # print(datasession.keys())

    #Current Mood
    mood = datasession['CurrentMood']
    # print(mood)
    #Current Mood
    physicalstate = datasession['CurrentPhysicalState']
    # print(mood)
    #DownTime
    datadown =(datasession['DownTime'])
    #Uptime
    dataup = (datasession['UpTime'])
    #Euclidean Distance
    distance = datasession['Distance']
    #Deliberately Long Pressed Button
    islongpress = datasession['IsLongPress']
    #PressureValues
    # pressure = datasession['PressureValue']
    # print(islongpress)

    #ht: HoldTime, ft: FlightTime
    #sp: Speed, pfr: Press-Flight-Rate
    #pv: Pressure Values
    ht = []
    ft = []
    sp = []
    pfr = []
    # pv = []

    length = len(datadown)
    for p in range(length):
        if p<length-1:
            #FlightTime < 0 are omitted from the sequences
            #HoldTime > 300 are excluded from the sequences
            if ((datadown[p+1] - dataup[p]) > 0) and (islongpress[p]== 0):
                ft.append(datadown[p+1] - dataup[p])
                ht.append(dataup[p] - datadown[p])
                # pv.append(pressure[p])
        else: break

    #Total Number of Characters 
    length = len(ht)

    for p in range(length-1):
        sp.append(distance[p]/ft[p])
        pfr.append(ht[p]/ft[p])
    
    #dr: Delete Rate
    dr = (datasession['NumDels'])/length

    #Duration of Session (in msec)
    # duration = datasession['StopDateTime']-datasession['StartDateTime']

    #Convert data lists to Panda.Series
    htseries = pd.Series(ht)
    ftseries = pd.Series(ft)
    spseries = pd.Series(sp)
    pfrseries = pd.Series(pfr)
    # pvseries = pd.Series(pv)

    #Mean of each Series
    htmean = htseries.mean()
    ftmean = ftseries.mean()
    spmean = spseries.mean()
    pfrmean = pfrseries.mean()
    # pvmean = pvseries.mean()

    #Median of each Series
    htmedian = htseries.median()
    ftmedian = ftseries.median()
    spmedian = spseries.median()
    pfrmedian = pfrseries.median()
    # pvmedian = pvseries.median()

    #Standard Deviation of each Series
    htstd = htseries.std()
    ftstd = ftseries.std()
    spstd = spseries.std()
    pfrstd = pfrseries.std()
    # pvstd = pvseries.std()

    #Skewness of each Series
    htskew = htseries.skew()
    ftskew = ftseries.skew()
    spskew = spseries.skew()
    pfrskew = pfrseries.skew()
    # pvskew = pvseries.skew()

    #Mean of each Series
    htkurtosis = htseries.kurtosis()
    ftkurtosis = ftseries.kurtosis()
    spkurtosis = spseries.kurtosis()
    pfrkurtosis = pfrseries.kurtosis()
    # pvkurtosis = pvseries.kurtosis()
    
    
    #Plot data
    # htseries.plot.box()
    # plt.show()
    
    # print(htstd)
    # print(htskew)
    # print(htkurtosis)
    
    #Insert Characteristics into Variables Dictionary
    variables = {'HT_Mean':htmean, 'HT_Median':htmedian, 'HT_STD':htstd,
        'HT_Skewness':htskew, 'HT_Kurtosis':htkurtosis,
        'FT_Mean':ftmean, 'FT_Median':ftmedian, 'FT_STD':ftstd,
        'FT_Skewness':ftskew, 'FT_Kurtosis':ftkurtosis,
        'SP_Mean':spmean, 'SP_Median':spmedian, 'SP_STD':spstd,
        'SP_Skewness':spskew, 'SP_Kurtosis':spkurtosis,
        'PFR_Mean':pfrmean, 'PFR_Median':pfrmedian, 'PFR_STD':pfrstd,
        'PFR_Skewness':pfrskew, 'PFR_Kurtosis':pfrkurtosis,
        # 'PV_Mean':pvmean, 'PV_Median':pvmedian, 'PV_STD':pvstd,
        # 'PV_Skewness':pvskew, 'PV_Kurtosis':pvkurtosis,
        # 'Duration':duration,
        'Delete_Rate':dr, 'Length':length,
        'Mood':mood, 'Physical_State':physicalstate
    }

    # distance = df.loc['Distance'][0]

    #Open .csv file and append variables
    file_exists = os.path.isfile('./output.csv')

    with open('output.csv', 'a', newline='') as csvfile:
        fieldnames = variables.keys()    
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(variables)
    
    return 

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

    #Loop across all files and create output.csv
    #containing typingdata of each session                
    os.chdir(dirname)
    for root, dirs, files in os.walk(dirname, topdown = False):
        for filename in files:
            # print(os.path.join(root, filename))
            os.chdir(os.path.abspath(root))
            if filename.endswith('.json'):
                # print(filename)
                extract(filename)


#?Preprocessing?
# Remove duplicates

#Function for processing DataFrame of typing data
def process(csvfile):
    data = pd.read_csv(csvfile)
    df = pd.DataFrame(data)
    return df