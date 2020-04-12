import os
import json
import datetime


def info(jsonFile):
    # Data Acquisition from JSON files
    with open(jsonFile) as json_file:
        datasession = json.load(json_file)

    # UserID
    userid = datasession['userDeviceID']
    # UserAge
    userage = datasession['userAge']
    # UserGender
    usergender = datasession['userGender']
    # UserPHQ9
    userphq9 = datasession['userPhq9Score']
    # UserDeficiency
    # userdeficiency = datasession['userDeficiency']
    # UserMedication
    # usermedication = datasession['userMedication']

    stat = {'UserID': userid, 'User_Age': userage,
            'User_Gender': usergender, 'User_PHQ9': userphq9}

    # df = pd.read_json(jsonFile, orient = 'index')
    # df = pd.DataFrame.from_dict([stat])

    return stat


def patients(phq9, gender, age):
    dest = '/home/jason/Documents/Thesis/TypingData/iOS'
    os.chdir(dest)
    for root, dirs, files in os.walk(os.getcwd(), topdown=False):
        for filename in files:
            os.chdir(os.path.abspath(root))
            if filename.startswith('Info.json'):
                stat = info(filename)
                userid = str(os.path.abspath(os.path.join(os.getcwd(), "./."))).split('/')[-1]
                os.chdir(dest + '/userid')
                dates = []
                for root, dirs, files in os.walk(os.getcwd(), topdown=True):
                    for name in dirs:
                        format_str = '%d.%m.%Y'
                        date_obj = datetime.datetime.strptime(name, format_str)
                        dates.append(date_obj)


                if stat['User_PHQ9'] == phq9 and stat['User_Gender'] == gender \
                   and stat['User_Age'] == age:
                    userid = str(os.path.abspath(os.path.join(os.getcwd(), "./."))).split('/')[-1]
                    print('userid: ' + userid + ', phq9:' + str(stat['User_PHQ9']) + 
                          ', age:' + str(stat['User_Age']))


def patientsloop(gender, age, userdate):
    dest = '/home/jason/Documents/Thesis/TypingData/iOS'
    os.chdir(dest)
    for root, dirs, files in os.walk(os.getcwd(), topdown=False):
        for filename in files:
            os.chdir(os.path.abspath(root))
            if filename.startswith('Info.json'):
                stat = info(filename)
                userid = str(os.path.abspath(os.path.join(os.getcwd(), "./."))).split('/')[-1]
                os.chdir(dest + '/' + userid)
                dates = []
                for root, dirs, files in os.walk(os.getcwd(), topdown=True):
                    for name in dirs:
                        format_str = '%d.%m.%Y'
                        date_obj = datetime.datetime.strptime(name, format_str)
                        dates.append(date_obj)
                    if dates:
                        # print('User: ' + str(userid) + ', first date: ' + str(min(dates)))
                        firstdate = min(dates).strftime('%Y-%m-%d')
                    else:
                        # print('User: ' + str(userid) + ', first date is empty')
                        firstdate = 'EMPTY'
                    # print(firstdate)
                if stat['User_Gender'] == gender \
                   and stat['User_Age'] == age and firstdate == userdate:
                    print('userid: ' + userid + ', phq9:' + str(stat['User_PHQ9']) + 
                          ', age:' + str(stat['User_Age']) + ', date: ' + firstdate)