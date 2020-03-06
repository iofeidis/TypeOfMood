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

def extract(jsonFile):
    #Data Acquisition from JSON files
    with open(jsonFile) as json_file:
        datasession = json.loads(json_file)
    
    #?Mood and Physical State?
    #Current Mood
    #mood = datasession['CurrentMood']
    # print(mood)
    #Current Physical State
    #physicalstate = datasession['CurrentPhysicalState']
    # print(physicalstate)

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

    #ht: HoldTime, ft: FlightTime
    #am: AccelerometerMagnitude, aa: AccelerometerAngle,
    #gm: GyroscopeMagnitude, pv: Pressure Values
    ht = []
    ft = []
    am = []
    aa = []
    gm = []
    pv = []

    length = datasession['sumOfCharacters']

    for p in range(length):
        if p<length-1:
            #FlightTime < 0 are omitted from the sequences
            #HoldTime > 300 are excluded from the sequences
            # map function
            if ((datadown[p+1] - dataup[p]) > 0) and (islongpress[p]== 0):
                ft.append(datadown[p+1] - dataup[p])
                ht.append(dataup[p] - datadown[p])
                pv.append(pressure[p])
        else: break

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

    length = len(rawValues['accelerometerX'])

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
    dr = (datasession['NumDels'])/length

    #Length of Characters
    length = datasession['sumOfCharacters']

    #Duration
    duration = datasession['keyboardDownTime'] - datasession['keyboardDownTime'] 