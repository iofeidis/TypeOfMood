# statistics.py
#
# Script for extracting statistics of session data
# from .json file to DataFrames
# for Android devices
#
# Iason Ofeidis 2019

import json
import pandas as pd 
import numpy as np 
import sys
import os
import csv
import matplotlib.pyplot as plt

#Function for extracting statistics of session
def session_statistics(jsonFile):
    #Data Acquisition from JSON files
    with open(jsonFile) as json_file:
        data = json.load(json_file)
    # print(data.keys())
    #Keeping only SESSION_DATA from json file
    datasession = json.loads(data['SESSION_DATA'])
    # print(datasession.keys())
1
    #Current Mood
    mood = datasession['CurrentMood']
    # print(mood)
    #Current Physical State
    physicalstate = datasession['CurrentPhysicalState']
    # print(physicalstate)

    

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
    
    #Insert session statistics into Statistics Dictionary
    statistics = {'Keystrokes':length, 'Mood':mood,
        'Physical_State':physicalstate
    }

    return statistics

#Function for looping across all files in a directory
def files_statistics(dirname):
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