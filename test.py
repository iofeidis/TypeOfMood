# test.py

# import features
# import os
# import pandas as pd
# os.chdir('/home/jason/Documents/Thesis/azuretry2/iOS')
# data = pd.read_csv('dynamics_user.csv')
# dfd = pd.DataFrame(data)
# data = pd.read_csv('statistics_user.csv')
# dfl = pd.DataFrame(data)
# features.windows(dfd, dfl)
# features.windows_users(os.getcwd())

# import plots
# plots.cors_windows('scatterplot')

import os
# import statisticsall
import plots
# os.chdir('/home/jason/Documents/Thesis/azuretry2/iOS/D24B8716-810F-41AB-A905-197370EB08C6')
# os.chdir('/home/jason/Documents/Thesis/azuretry2/iOS')
# plots.sessions_feature_plot(os.getcwd(), 'FT_Mean', 'undefined')
# statisticsall.sessions_features(os.getcwd())
os.chdir('/home/jason/Documents/Thesis/azuretry2/iOS')
plots.feature_distributions(os.getcwd(), 'Hold_Time')

# import typingdataios
# os.chdir('/home/jason/Documents/Thesis/azuretry2/iOS')
# typingdataios.users(os.getcwd())
# import plots
# os.chdir('/home/jason/Documents/Thesis/azuretry3/iOS')
# plots.boxplots_users(os.getcwd(), 'median', 'Session')
# plots.facetgrid_boxplots(os.getcwd(), 'Neutral')

# import statistics
# statistics.windows_users()

# import statisticsall

# os.chdir('/home/jason/Documents/Thesis/azuretry2/iOS')
# statisticsall.distrib(os.getcwd())

# os.chdir('/home/jason/Documents/Thesis/azuretry2/iOS/D24B8716-810F-41AB-A905-197370EB08C6')
# import analysis
# import pandas as pd
# os.chdir('/home/jason/Documents/Thesis/azuretry3/iOS')
# data = pd.read_csv('output_total.csv')
# df = pd.DataFrame(data)
# analysis.classification_all(df, 'Happy')

# import analysis
# os.chdir('/home/jason/Documents/Thesis/azuretry3/iOS/')
# os.chdir('/home/jason/Documents/Thesis/azuretry2/Android')
# analysis.clasf_user(os.getcwd(), 'Stressed')
# analysis.logistic_regression_user(os.getcwd(), 'Sad')
# analysis.svm_clf_user(os.getcwd(), 'Sad')

# import statisticsall
# os.chdir('/home/jason/Documents/Thesis/azuretry2/iOS')
# statisticsall.statisticsdates(os.getcwd())

# import typingdataios
# os.chdir('/home/jason/Documents/Thesis/azuretry3/iOS')
# typingdataios.users(os.getcwd())