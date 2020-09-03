import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plots
    

# os.chdir('/home/jason/Documents/Thesis/azuretry2/Android')
# p = 0
# for root, dirs, files in os.walk(os.getcwd(), topdown=False):
#     for d in dirs:
#         os.chdir(os.path.abspath(root))
#         if not d.startswith('2020') and \
#            not d.startswith('2019') and \
#            not d.startswith('2018'): 
#             # print(os.path.abspath(os.path.join(root, d)))
#             os.chdir(os.path.abspath(os.path.join(root, d)))
#             for rootb, dirsb, filesb in os.walk(os.getcwd(), topdown=True):
#                 # print(filesb)
#                 os.chdir(os.path.abspath(rootb))
#                 for f in filesb:
#                     if f.startswith('statistics_user.csv'):
#                         data = pd.read_csv(f)
#                         df = pd.DataFrame(data)
#                         if df.Date.max() > '2020-03-02':
#                             p += 1
#                             userid = \
#                                 str(os.path.abspath(os.path.join(os.getcwd(), "./.")))\
#                                 .split('/')[-1]
#                             print(userid)
#                 break
# print(p)


# def windows(date):
#     windows = [
#         '2020-01-14:2020-01-19', '2020-01-20:2020-01-25',
#         '2020-01-26:2020-01-31', '2020-02-01:2020-02-06',
#         '2020-02-07:2020-02-12', '2020-02-13:2020-02-18',
#         '2020-02-19:2020-02-24', '2020-02-25:2020-03-01',
#         '2020-03-02:2020-03-07', '2020-03-08:2020-03-13',
#         '2020-03-14:2020-03-19', '2020-03-20:2020-03-25',
#         '2020-03-26:2020-03-31', '2020-04-01:2020-04-06',
#         '2020-04-07:2020-04-12', '2020-04-13:2020-04-18'
#     ]
#     for w in windows:
#         start = w.split(':')[0] 
#         end = w.split(':')[1]
#         if (date >= start) and (date <= end):
#             return windows.index(w)

# os.chdir('/home/jason/Documents/Thesis/azuretry2/iOS')
# for root, dirs, files in os.walk(os.getcwd(), topdown=True):
#     for f in files:
#         os.chdir(os.path.abspath(root))
#         if f.startswith('distributions.csv'):
#             data = pd.read_csv(f)
#             df = pd.DataFrame(data)
#             df['period'] = df.Date.apply(lambda x: 0 if x < '2020-02-28'  
#                 else (1 if (x >= '2020-02-28') and (x < '2020-03-14') else 2))
#             df['window'] = df.Date.apply(windows)
#             df.to_csv(f, mode='w', header=True, index=False)


# os.chdir('/home/jason/Documents/Thesis/azuretry2/Android')
# for root, dirs, files in os.walk(os.getcwd(), topdown=True):
#     for f in files:
#         os.chdir(os.path.abspath(root))
#         if f.startswith('output_user.csv'):
#             data = pd.read_csv(f)
#             df = pd.DataFrame(data)
#             df = plots.clean(df)
#             df = df.round(4)
#             df.to_csv(f, mode='w', header=True, index=False)

# os.chdir('/home/jason/Documents/Thesis/azuretry3/iOS')
# for root, dirs, files in os.walk(os.getcwd(), topdown=True):
#     for f in files:
#         os.chdir(os.path.abspath(root))
#         if f.startswith('output_total.csv'):
#             data = pd.read_csv(f)
#             df = pd.DataFrame(data)
#             df.User_PHQ9 = df.User_PHQ9.fillna(method='ffill')
#             df.to_csv(f, mode='w', header=True, index=False)

