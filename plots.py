# plots.py
# Script for generating statistics plots
# Iason Ofeidis 2020

import os
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
from matplotlib.figure import figaspect
from scipy.stats import spearmanr

sns.set()


def clean(df):
    """ Clean one dataframe from 'Postponing, undefined, TIMEOUT' values"""
    df = df.replace('Happy TIMEOUT', 'Happy')
    df = df.replace('Neutral TIMEOUT', 'Neutral')
    df = df.replace('Sad TIMEOUT', 'Sad')
    df = df.replace('Stressed TIMEOUT', 'Stressed')
    df = df.replace('Relaxation TIMEOUT', 'Relaxation')
    df = df.replace('Tiredness TIMEOUT', 'Tiredness')
    df = df.replace('Sickness TIMEOUT', 'Sickness')
    df = df.replace('undefined TIMEOUT', 'undefined')
    df = df.replace('Postponing TIMEOUT', 'Postponing')
    df = df[(df['Mood'] != 'undefined') &
            (df['Mood'] != 'Postponing') &
            (df['Physical_State'] != 'Postponing') & 
            (df['Physical_State'] != 'undefined')].reset_index(drop=True)

    return df


def evol(df, name, device, label):
    """ Plotting the evolution of Mood labels in time
        Just change label and device variables
        label = 'Mood'
        device = 'iOS' """
    # Clean df from undefined, Postponing, TIMEOUT values
    df = clean(df)
    # Keep only sessions with NumberOfKeystrokes > 5
    # df = df[df['Keystrokes'] > 5]
    # Keep only label and Date columns
    df = df[[label, 'Date']]
    # str(Date) to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    # Keep only recent sessions
    df = df[df['Date'] > '2019-11-01']
    df = df.drop_duplicates()
    # Count labels for each specific Date
    df = df.groupby(df.columns.tolist()).size().reset_index().\
        rename(columns={0: 'records'})
    # Pivot necessary for plotting
    df = df.pivot(index='Date', columns=label, values='records')    
    df = df.fillna(0)
    userid = str(os.path.abspath(os.path.join(os.getcwd(), "./."))).split('/')[-1]
    title = 'UserID: ' + userid + ', Device: ' + device
    if not df.empty:
        if len(df.columns) > 1:
            df.plot(linewidth=4, title=title)
            plt.axvline(x='2020-01-25', linewidth=2, color='r')
            plt.axvline(x='2020-02-28', linewidth=2, color='g')
            plt.show()
        else:
            if len(df) == 1:
                df.plot.bar(title=title)
            else:
                df.plot(linewidth=4, title=title)
                plt.axvline(x='2020-01-25', linewidth=2, color='r')
                plt.axvline(x='2020-02-28', linewidth=2, color='g')
        plt.close()


def label_distribution(df, name, device, label):
    """ Plotting the distribution of Mood or Physical_State labels 
        in time periods"""
    # Clean df from undefined, Postponing, TIMEOUT values
    df = clean(df)
    # Keep only sessions with NumberOfKeystrokes > 5
    # df = df[df['Keystrokes'] > 5]
    # Keep only label and Date columns 
    df = df[['User_PHQ9', label, 'Date']]
    if not df.empty:
        userphq9 = df['User_PHQ9'][0]
    else:
        userphq9 = 'empty'
    peakdate = '2020-02-28'
    # Keep only recent sessions
    df = df[df['Date'] > '2019-12-25']
    df = df.drop_duplicates()
    df.loc[(df.Date < peakdate), 'Date'] = 'period1'
    df.loc[(df.Date >= peakdate) & 
           (df.Date != 'period1'), 'Date'] = 'period2'
    df = df.sort_values(by=['Date'])
    userid = str(os.path.abspath(os.path.join(os.getcwd(), "./.")))\
        .split('/')[-1]
    title = 'UserID: ' + userid + ',\n User_PHQ9: ' + str(userphq9) + \
            ', Device: ' + device
    if not df.empty:
        if (df.Date.nunique() > 1):
            df.groupby(label).Date.value_counts().unstack(1).plot.barh(title=title)
            plt.gcf()
            plt.show()
            plt.close()


def dynamics_distribution(df, name, device, dynamics_variable):
    """ Plot the distribution of keystroke dynamics in 2 periods
        Violin Plots """
    df = df.dropna()
    # Keep only recent sessions
    peakdate = '2020-02-28'
    df = df[df['Date'] > '2019-12-25']
    df.loc[(df.Date < peakdate), 'Date'] = 'period1'
    df.loc[(df.Date >= peakdate) & 
           (df.Date != 'period1'), 'Date'] = 'period2'
    df = df.sort_values(by=['Date'])
    userid = str(os.path.abspath(os.path.join(os.getcwd(), "./.")))\
        .split('/')[-1]
    title = 'UserID: ' + userid + ', Device: ' + device
    # Cut extreme values
    if device == 'iOS':
        df = df[df.Hold_Time < 0.3]
        df = df[df.Speed < 5000]
        df = df[df.Flight_Time < 3]
    elif device == 'Android':
        df = df[df.Speed < 5]
        df = df[df.Press_Flight_Rate < 10]
    df = df[[dynamics_variable, 'Date']]
    
    # Keep only users with all 3 periods
    if not df.empty and ('period1' in df.Date.values) and \
                        ('period2' in df.Date.values):
        sns.set() 
        os.chdir('/home/jason/Documents/Thesis/TypingData/' + device + '/Plots')
        if dynamics_variable == 'Hold_Time':
            sns.violinplot(y=df.Date, x=df.Hold_Time, bw=.2).set_title(title)
            plt.show()
            plt.close()
        elif dynamics_variable == 'Flight_Time':
            sns.violinplot(y=df.Date, x=df.Flight_Time, bw=.2).set_title(title)
            plt.show()
            plt.close()
        elif dynamics_variable == 'Speed':
            sns.violinplot(y=df.Date, x=df.Speed, bw=.2).set_title(title)
            plt.show()
            plt.close()
        elif dynamics_variable == 'Press_Flight_Rate':
            sns.violinplot(y=df.Date, x=df.Press_Flight_Rate, bw=.2).set_title(title)
            plt.show()
            plt.close()
        else:
            print('wrong dynamics input')

    return


def ratio(df, label, labelvalue, periods):
    """ Compute percentage and total of a label in a given time period """
    s = 0
    percentages = []
    numberall = []
    labels = labelvalue.split('+')
    for p in periods:
        # Total
        totals = [len(df[(df[label] == lab) & (df.Date == p)]) 
                  for lab in labels]
        s += sum(totals)
        numberall.append(len(df[df.Date == p]))
        # Percentage
        if len(df[df.Date == p]) != 0:
            percentages.append((sum(totals)) / len(df[df.Date == p]))
        else: 
            percentages.append(0)
    if percentages[0] == 0 and percentages[1] == 0:
        # No change in ratio
        ratio = 1
    elif percentages[0] == 0:
        # Added 1 on both num and denum
        ratio = (percentages[1] + 1 / numberall[1]) / \
                (percentages[0] + 1 / numberall[0])
    else:
        ratio = percentages[1] / percentages[0]
   
    return ratio, s


def label_distribution_sorted(df, label, labelvalue, device, k, peakdate):
    """ Plot label distribution for all users sorted 
        using 'statistics_total_added_info.csv' 
        For multiple labels, separate with '+' 
        k: offset index for plots"""
    df = df.drop_duplicates()
    df = df[df['Date'] > '2020-01-14']
    df.loc[(df.Date < peakdate), 'Date'] = 'period1'
    df.loc[(df.Date >= peakdate) & 
           (df.Date != 'period1'), 'Date'] = 'period2'
    periods = ['period1', 'period2']
    dfall = pd.DataFrame([])
    for value, data in df.groupby(['UserID', 'User_PHQ9']):
        dfuser = data
        # All periods inside Date values
        if 'period1' in dfuser.Date.values and \
           'period2' in dfuser.Date.values:
            r = round(ratio(dfuser, label, labelvalue, periods)[0], 3)
            totals = ratio(dfuser, label, labelvalue, periods)[1]
            dfratios = pd.DataFrame({'User_PHQ9': value[1],
                                     'Ratio ' + str(labelvalue): r,
                                     'Total': totals},
                                    index=[value[0]])
            dfall = pd.concat([dfall, dfratios])
    dfall.index.rename('UserID', inplace=True)
    nusers = len(dfall)
    sns.set()
    title = labelvalue + ' ' + label + \
        ' Ratios for all users in 2 time periods\n' + 'Device: ' + device + \
        ', Number of Users: ' + str(nusers) + ', Peakdate: ' + peakdate + \
        '\nOn the left: Total Number of ' + labelvalue + ' ' + label + \
        ' occurences.'
    # Aspect ratio of figure png
    w, h = figaspect(3 / 2)
    plt.figure(figsize=(w, h))    
    ax = plt.gca()
    dfall.sort_values('User_PHQ9').plot.barh(y='Ratio ' + str(labelvalue),
                                             x='User_PHQ9',
                                             title=title, ax=ax)
    plt.axvline(x=1, linewidth=2, color='r')
    for i, v in enumerate(dfall.sort_values('User_PHQ9').Total):
        ax.text(k, round(i, 1), str(v), color='green', fontweight='bold')
    for i, v in enumerate(dfall.sort_values('User_PHQ9')['Ratio ' + str(labelvalue)]):
        ax.text(v + 0.1, round(i, 1), str(round(v, 2)), color='blue', fontweight='bold')
    os.chdir('/home/jason/Documents/Thesis/azuretry2/iOS/DF')
    dfall.sort_values('User_PHQ9').to_csv('labels_' + str(labelvalue) + '_' +
                                          str(peakdate) + '.csv', 
                                          mode='w', index=True, header=True)
    plt.show()
    plt.close()



def dynamics_sorted(df, variable, device, peakdate, k, t):
    """ Plot ratios of each dynamics variable feature 
        between 2 time periods 
        using dynamics_total_added_PEAKDATE.csv """
    
    df = df[['UserID', 'User_PHQ9', variable, 'Sessions', 'Date']]
    nusers = df.UserID.nunique()
    dfall = pd.DataFrame([])
    for value, data in df.groupby(['UserID', 'User_PHQ9']):
        r = t * abs((data[data.Date == 'period2'][variable].values[0] - 
                     data[data.Date == 'period1'][variable].values[0])) 
        s = data[data.Date == 'period2'].Sessions.values[0] + \
            data[data.Date == 'period1'].Sessions.values[0]
        dfratios = pd.DataFrame({'User_PHQ9': value[1],
                                 'Ratio ' + str(variable): round(r, 4), 'Total': s},
                                index=[value[0]])
        dfall = pd.concat([dfall, dfratios])
    dfall.index.rename('UserID', inplace=True)
    sns.set()
    title = variable + \
        ' Absolute difference *' + str(t) + ' of users between 2 time periods\n' + \
        'Device: ' + device + \
        ', Number of Users: ' + str(nusers) + '\n' + \
        'On the left: Total Number of Characters\n' + \
        'Red vertical line: Median of values = ' \
        + str(round(dfall['Ratio ' + str(variable)].median(), 3))
    # Aspect ratio of figure png
    ax = plt.gca()
    dfall.sort_values('User_PHQ9').plot.barh(y='Ratio ' + str(variable),
                                             x='User_PHQ9', width=1, 
                                             title=title, ax=ax)
    plt.axvline(x=dfall['Ratio ' + str(variable)].median(), linewidth=2, color='r')
    for i, v in enumerate(dfall.sort_values('User_PHQ9').Total):
        ax.text(k, i, str(v), color='green', fontweight='bold')
    for i, v in enumerate(dfall.sort_values('User_PHQ9')['Ratio ' + str(variable)]):
        ax.text(v, i, str(round(v, 2)), color='blue', fontweight='bold', bbox=dict(facecolor='white', alpha=0.5))
    plt.show()
    os.chdir('/home/jason/Documents/Thesis/azuretry2/iOS/DF')
    dfall.sort_values('User_PHQ9').to_csv('dynamics_' + str(variable) + '_' +  
                                          str(peakdate) + '.csv', 
                                          mode='w', index=True, header=True)
    plt.close()
    



def multiline(dirname, device, label, plot, dynamics_variable):
    """ Different kind of plots """
    # Delete previous versions of .png files in directory
    os.chdir(dirname)
    for root, dirs, files in os.walk(os.getcwd(), topdown=False):
        for filename in files:
            os.chdir(os.path.abspath(root))
            if filename.endswith('.png'):
                os.remove(filename)

    os.chdir(dirname)
    for root, dirs, files in os.walk(os.getcwd(), topdown=False):
        for filename in files:
            os.chdir(os.path.abspath(root))
            # UserID is the name of parent directory of file
            userid = str(os.path.abspath(os.path.join(os.getcwd(), "./.")))\
                .split('/')[-1]
            if device == 'Android':
                if plot == 'evolution':
                    if filename.endswith('statistics_user.csv'):
                        data = pd.read_csv(filename)
                        df = pd.DataFrame(data)
                        if not df.empty:
                            evol(df, userid, device, label)
                elif plot == 'distribution':
                    if filename.endswith('statistics_user.csv'):
                        data = pd.read_csv(filename)
                        df = pd.DataFrame(data)
                        if not df.empty:
                            label_distribution(df, userid, device, label)
                elif plot == 'dynamics':
                    if filename.endswith('dynamics_user.csv'):
                        data = pd.read_csv(filename)
                        df = pd.DataFrame(data)
                        if not df.empty:
                            dynamics_distribution(df, userid, device, dynamics_variable)

            if device == 'iOS':
                if plot == 'evolution':
                    if filename.endswith('statistics_user_info_emotion.csv'):
                        data = pd.read_csv(filename)
                        df = pd.DataFrame(data)
                        if not df.empty:
                            evol(df, userid, device, label)
                elif plot == 'distribution':
                    if filename.endswith('statistics_user_info_emotion.csv'):
                        data = pd.read_csv(filename)
                        df = pd.DataFrame(data)
                        if not df.empty:
                            label_distribution(df, userid, device, label)
                elif plot == 'dynamics':
                    if filename.endswith('dynamics_user.csv'):
                        data = pd.read_csv(filename)
                        df = pd.DataFrame(data)
                        if not df.empty:
                            dynamics_distribution(df, userid, device, dynamics_variable)


def cors_windows(plot):
    """ Plot correlation 'heatmap' of users' features and labels 
        OR
        'scatterplot' of feature with strongest p-value"""
    sns.set()
    os.chdir('/home/jason/Documents/Thesis/azuretry2/iOS')
    p = 0
    for root, dirs, files in os.walk(os.getcwd(), topdown=True):
        for f in files:
            os.chdir(os.path.abspath(root))
            if f.startswith('windows_user.csv'):
                data = pd.read_csv(f)
                df = pd.DataFrame(data)
                if len(df.dropna()) > 5:
                    p += 1
                    userid = str(os.path.abspath(os.path.join(os.getcwd(), "./.")))\
                        .split('/')[-1]
                    r = []
                    a = []
                    for c in df.loc[:, 'HT_Mean':'PFR_Kurtosis'].columns:
                        a.append(round(spearmanr(df.dropna()[c],
                                                 df.dropna().Mood)[1], 3))
                        r.append(round(spearmanr(df.dropna()[c],
                                                 df.dropna().Mood)[0], 3))
                    cormat = pd.DataFrame({'Mood': r, 'P-values': a})
                    cormat = cormat.set_index(df.loc[:, 'HT_Mean':'PFR_Kurtosis'].columns)
                    if max(abs(cormat.Mood.values)) > 0.3:
                        if plot == 'heatmap':
                            ax = sns.heatmap(cormat[abs(cormat.Mood) > 
                                                    max(abs(cormat.Mood.values)) - .2],
                                             annot=True, cmap="YlGnBu")
                            ax.set_title(userid + '\n Spearman, Sample Length:' + 
                                         str(len(df.dropna())))
                        elif plot == 'scatterplot':
                            ax = sns.regplot(
                                x=df.dropna()['FT_Mean'],
                                y=df.dropna().Mood)
                            ax.set_title(userid + '\n Spearman, Sample Length:' + 
                                         str(len(df.dropna())) + ' P-value:' + 
                                         str(cormat['P-values']['FT_Mean']))
                        elif plot == 'cormat':
                            print(userid)
                            print(cormat)
            
                        plt.show()
                        plt.close()
    print('Number of users with sample length > 5: ', p)


def feature_distributions(dirname, feature):
    """ Plot distribution of keystroke features along different mood labels """
    os.chdir(dirname)
    sns.set()
    for root, dirs, files in os.walk(os.getcwd(), topdown=True):
        for f in files:
            os.chdir(os.path.abspath(root))
            if f.startswith('distributions.csv'):
                data = pd.read_csv(f)
                df = pd.DataFrame(data)
                df = df.round(5)
                # Keep recent data
                df = df[df.Date > '2020-01-15']
                # Dynamics requirements
                # df = df[df.Mood.notna()]
                df.Mood = df.Mood.fillna('undefined')
                df = df[df.Hold_Time < 1]
                df = df[df.Flight_Time < 3]
                df = df[df.Speed < 1000]
                df = df[df.Press_Flight_Rate < 1.5]
                # df = df[(df.window >= 6) & (df.window < 12)]
                if not df.empty:
                    # FacetGrid plot
                    g = sns.FacetGrid(df, col='Mood', row='period', hue='Date',
                                      height=4, aspect=.6)
                    g.map(sns.distplot, feature,
                          hist=False, rug=True, kde_kws={"shade": True})
                    userid = str(os.path.abspath(os.path.join(os.getcwd(), "./.")))\
                        .split('/')[-1]
                    plt.subplots_adjust(top=.85)
                    g.fig.suptitle(userid.split('-')[0])
                    # print(df.describe())
                    plt.show()
                    if df.Mood.nunique() > 2:
                        plt.show()
                        plt.close()


def sessions_feature_plot(dirname, feature, mood):
    """ Plot evolution of specific feature in time """
    os.chdir(dirname)
    sns.set()
    for root, dirs, files in os.walk(os.getcwd(), topdown=True):
        for f in files:
            os.chdir(os.path.abspath(root))
            if f.startswith('sessions_user.csv'):
                userid = str(os.path.abspath(os.path.join(os.getcwd(), "./.")))\
                    .split('/')[-1]
                print(userid)
                data = pd.read_csv(f)
                df = pd.DataFrame(data)
                df = df[df.Mood == mood]
                df.Date = pd.to_datetime(df.Date)
                if not df.empty and len(df) > 5:
                    df.set_index('Date').sort_index().plot(y=feature)
                    plt.axvline(x='2020-02-28', linewidth=2, color='g')
                    plt.show()


def boxplots_users(dirname, average, date_or_session):
    """ Compute BOXPLOTS features 
        per date or session for users output_user.csv """
    os.chdir(dirname)
    for root, dirs, files in os.walk(os.getcwd(), topdown=True):
        for f in files:
            os.chdir(os.path.abspath(root))
            if f.startswith('output_user.csv'):
                data = pd.read_csv(f)
                df = pd.DataFrame(data)
                if date_or_session == 'Date':
                    dfall = pd.DataFrame([])
                    for a, b in df.groupby('Date'):
                        if a < '2020-02-28': 
                            period = 0
                        else:
                            period = 1
                        if average == 'mean':
                            stat = {        
                                'HT_Mean': b.HT_Mean.mean(),
                                'HT_STD': b.HT_STD.mean(),
                                'HT_Skewness': b.HT_Skewness.mean(),
                                'HT_Kurtosis': b.HT_Kurtosis.mean(), 
                                
                                'FT_Mean': b.FT_Mean.mean(),
                                'FT_STD': b.FT_STD.mean(),
                                'FT_Skewness': b.FT_Skewness.mean(),
                                'FT_Kurtosis': b.FT_Kurtosis.mean(), 
                                
                                'SP_Mean': b.SP_Mean.mean(),
                                'SP_STD': b.SP_STD.mean(),
                                'SP_Skewness': b.SP_Skewness.mean(),
                                'SP_Kurtosis': b.SP_Kurtosis.mean(), 
                                
                                'PFR_Mean': b.PFR_Mean.mean(),
                                'PFR_STD': b.PFR_STD.mean(),
                                'PFR_Skewness': b.PFR_Skewness.mean(),
                                'PFR_Kurtosis': b.PFR_Kurtosis.mean(), 
                                
                                'Sessions': len(b),
                                'Date': a,
                                'Period': period,
                                'Mood': b.Mood.values[0],
                                'Physical_State': b.Physical_State.values[0]}
                        elif average == 'median':
                            stat = {        
                                'HT_Mean': b.HT_Mean.median(),
                                'HT_STD': b.HT_STD.median(),
                                'HT_Skewness': b.HT_Skewness.median(),
                                'HT_Kurtosis': b.HT_Kurtosis.median(), 
                                
                                'FT_Mean': b.FT_Mean.median(),
                                'FT_STD': b.FT_STD.median(),
                                'FT_Skewness': b.FT_Skewness.median(),
                                'FT_Kurtosis': b.FT_Kurtosis.median(), 
                                
                                'SP_Mean': b.SP_Mean.median(),
                                'SP_STD': b.SP_STD.median(),
                                'SP_Skewness': b.SP_Skewness.median(),
                                'SP_Kurtosis': b.SP_Kurtosis.median(), 
                                
                                'PFR_Mean': b.PFR_Mean.median(),
                                'PFR_STD': b.PFR_STD.median(),
                                'PFR_Skewness': b.PFR_Skewness.median(),
                                'PFR_Kurtosis': b.PFR_Kurtosis.median(), 
                                
                                'Sessions': len(b),
                                'Date': a,
                                'Period': period,
                                'Mood': b.Mood.values[0],
                                'Physical_State': b.Physical_State.values[0]}
                        dfall = pd.concat([dfall, pd.DataFrame([stat])])
                    

                    userid = \
                        str(os.path.abspath(os.path.join(os.getcwd(), "./.")))\
                        .split('/')[-1]
                    if dfall.Date.nunique() > 15:
                        title = userid.split('-')[0] + \
                            ', Period 0 dates: ' + str(len(dfall[dfall.Period == 0])) + \
                            ', Period 1 dates: ' + str(len(dfall[dfall.Period == 1]))  
                        sns.boxplot(y="FT_Mean", x="Mood", hue='Period',
                                    data=dfall).set_title(title)
                        sns.stripplot(y="FT_Mean", x="Mood", hue='Period',
                                      color='0', data=dfall, dodge=True)\
                            .set_title(title)
                        plt.show()                
                        plt.close()
                elif date_or_session == 'Session':
                    df['Period'] = df.Date.apply(lambda x: 0 if x < '2020-02-28' else 1)
                    userid = \
                        str(os.path.abspath(os.path.join(os.getcwd(), "./.")))\
                        .split('/')[-1]
                    if df.Date.nunique() > 15:
                        title = userid.split('-')[0] + \
                            ', Period 0 sessions: ' + str(len(df[df.Period == 0])) + \
                            ', Period 1 sessions: ' + str(len(df[df.Period == 1]))  
                        sns.boxplot(y="HT_STD", x="Mood", hue='Period',
                                    data=df, whis=2).set_title(title)
                        sns.stripplot(y="HT_STD", x="Mood", hue='Period',
                                      data=df, color='0.5', dodge=True)\
                            .set_title(title)
                        plt.show()                
                        plt.close()


def facetgrid_boxplots(dirname, label):
    """ Trying combined boxplots on sns facetgrid 
        Insert label = Mood for all labels compared OR
               label = Stressed, etc for specific label comparison"""
    os.chdir(dirname)
    for root, dirs, files in os.walk(os.getcwd(), topdown=True):
        for f in files:
            os.chdir(os.path.abspath(root))
            if f.startswith('output_user.csv'):
                data = pd.read_csv(f)
                df = pd.DataFrame(data)
                # df = df[df.Mood != 'Neutral']
                df['Period'] = df.Date.apply(lambda x: 0 if x < '2020-02-28'
                                             else 1)
                userid = \
                    str(os.path.abspath(os.path.join(os.getcwd(), "./.")))\
                    .split('/')[-1]
                # if len(df[df.Mood == label]) > 50:
                if len(df) > 50:
                    title = userid.split('-')[0] + \
                        ', Period 0 sessions: ' + str(len(df[df.Period == 0])) + \
                        ', Period 1 sessions: ' + str(len(df[df.Period == 1]))  
    
                    if label != 'Mood':
                        k = 'Label'
                        df['Label'] = df.Mood.apply(lambda x: label if 
                                                    x == label else 'Not ' + label)
                    else:
                        k = 'Mood'
                    
                    fig, axes = plt.subplots(2, 2)
                    
                    # Boxplots
                    sns.boxplot(x=k, y="HT_Mean", hue='Period',
                                data=df, orient='v', ax=axes[0, 0], showfliers=False)
                    sns.boxplot(x=k, y="FT_Mean", hue='Period',
                                data=df, orient='v', ax=axes[0, 1], showfliers=False)
                    sns.boxplot(x=k, y="SP_Mean", hue='Period', 
                                data=df, orient='v', ax=axes[1, 0], showfliers=False)
                    sns.boxplot(x=k, y="PFR_Mean", hue='Period',
                                data=df, orient='v', ax=axes[1, 1], showfliers=False)
                    
                    # Stripplots
                    sns.stripplot(y="HT_Mean", x=k, data=df, hue='Period',
                                  color='0.5', dodge=True, ax=axes[0, 0])
                    sns.stripplot(y="FT_Mean", x=k, data=df, hue='Period',
                                  color='0.5', dodge=True, ax=axes[0, 1])
                    sns.stripplot(y="SP_Mean", x=k, data=df, hue='Period',
                                  color='0.5', dodge=True, ax=axes[1, 0])
                    sns.stripplot(y="PFR_Mean", x=k, data=df, hue='Period',
                                  color='0.5', dodge=True, ax=axes[1, 1])

                    # Title
                    axes[0, 0].set_title(title)

                    plt.show()                
                    plt.close()
