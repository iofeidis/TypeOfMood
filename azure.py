# workflow after downloading azure container
# last sync: 17-04-2020

import statisticsall
import os
# import transfer
import statisticsios
import statistics

# TRANSFER BASH

# Now files are inside iOS, Android, etc
# Maybe typingdata directory missing
dirname = '/home/jason/Documents/Thesis/azuretry2/iOS'
os.chdir(dirname)
for root, dirs, files in os.walk(os.getcwd()):
    for f in files:
        os.chdir(os.path.abspath(root))
        if f.endswith('.csv'):
            os.remove(f) 
os.chdir(dirname)
statisticsios.users(os.getcwd())
os.chdir(dirname)
statisticsall.stat_without_emotion(os.getcwd())
os.chdir(dirname)
statisticsall.stat_without_keystrokes(os.getcwd())
os.chdir(dirname)
statisticsall.sessions_total_ios(os.getcwd())
os.chdir(dirname)
statisticsall.emotions_total_ios(os.getcwd())
os.chdir(dirname)
statisticsall.statistics_add(os.getcwd())
os.chdir(dirname)
statisticsall.dynamics_users(os.getcwd(), 'iOS')
# os.chdir(dirname)
# statisticsall.stat_info_emotion(os.getcwd())
os.chdir(dirname)
statisticsall.dynamics_total(os.getcwd(), 'iOS')








