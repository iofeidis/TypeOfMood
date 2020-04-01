import os

# os.chdir('/home/jason/Documents/Thesis/TypingData/test')

# STATISTICS
# import statistics
# # statistics.filesextract(os.getcwd())
# statistics.users(os.getcwd())

# import typingdata
# # typingdata.filesextract(os.getcwd())
# typingdata.users(os.getcwd())

# os.chdir('/home/jason/Documents/Thesis/TypingData/iOS')

# import statisticsios
# # statisticsios.filesextract(os.getcwd())
# statisticsios.users(os.getcwd())

# TYPINGDATAFILES
# import typingdataios
# typingdataios.users(os.getcwd())

# ANALYSIS
# import analysis
# import pandas as pd
# os.chdir('/home/jason/Documents/Thesis/outputs/PHQ9')
# data = pd.read_csv('output_total_android.csv')
# # data = pd.read_csv('output_total_android.csv')
# df = pd.DataFrame(data)

# analysis.regression(df)

# PLOTS
import plots
os.chdir('/home/jason/Documents/Thesis/TypingData/iOS')
# plots.multiline(os.getcwd(), 'Android', 'Physical_State')
plots.multiline(os.getcwd(), 'iOS', 'label')

