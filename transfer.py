# Move directories from azurecontainer to iOS and 
# Android directories respectively

import os 
import shutil

path = '/home/jason/Documents/Thesis/azuretry2/typingdata/'
os.chdir(path)
for root, dirs, files in os.walk(os.getcwd(), topdown=True):
    for name in dirs:
        if name.isupper() and len(name) > 14 \
           and not name.startswith('2020') and not name.startswith('2019') \
           and not name.endswith('2020') and not name.endswith('2019'):
            source = path + name
            destination = path + 'iOS'
            dest = shutil.move(source, destination)
        elif name.islower() and len(name) > 14 \
                and not name.startswith('2020') and not name.startswith('2019') \
                and not name.endswith('2020') and not name.endswith('2019'):
            source = path + name
            destination = path + 'Android'
            dest = shutil.move(source, destination)
        else:
            source = path + name
            destination = path + 'etc'
            dest = shutil.move(source, destination)
