import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# os.chdir('/home/jason/Documents/Thesis/TypingData/iOS')
# p = 0
# for root, dirs, files in os.walk(os.getcwd(), topdown=False):
#     for d in dirs:
#         os.chdir(os.path.abspath(root))
#         if not d.endswith('2020') and \
#            not d.endswith('2019'): 
#             # print(os.path.abspath(os.path.join(root, d)))
#             os.chdir(os.path.abspath(os.path.join(root, d)))
#             for rootb, dirsb, filesb in os.walk(os.getcwd(), topdown=True):
#                 # print(filesb)    
#                 if 'statistics_user_info_emotion.csv' not in filesb or \
#                    'dynamics_user.csv' not in filesb:
#                     print(os.getcwd())  
#                     p += 1
#                 break
# print(p)
