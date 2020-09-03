# analysis.py
#
# Script for analyzing and modeling keystrokes for 
# PHQ9 regression and Mood classification
# for Android devices and iOS
#
# Iason Ofeidis 2019



# Use numpy to convert to arrays
import os
import numpy as np
import pandas as pd
# Import the model we are using
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression
from sklearn import svm

import matplotlib.pyplot as plt


def warn(*args, **kwargs):
    pass


import warnings
warnings.warn = warn

        
# Mood Classification

def classification_all(df, label):
    """ Random Forest Classification for all Users LOSO CVed """
    # Make binary classification (Happy/ Not Happy)
    
    df = df.dropna()
    # Don't consider Neutral Labels
    df = df[df.Mood != 'Neutral']
    # Only sessions with Length > 10
    df = df[df.Length > 10]
    # Keep certain users
    df = df[(df.UserID == 'D557D8F8-4507-4C85-9E72-73D8DA37D2EC') | 
            # (df.UserID == '1F7161C5-77C5-4811-B738-8732A5615E6F') |
            # (df.UserID == 'ohSuhaila') |
            (df.UserID == 'A8820B23-2BAA-4A6C-9E62-81BE4E82C85A') |
            (df.UserID == 'BB9F141D-DA36-44C8-B254-5F48DE21F3CE') |
            (df.UserID == 'A1D07844-C62F-4D3E-9598-A011D27C6C80')]
    # Physical State dummy variables
    df1 = pd.get_dummies(df.Physical_State)
    df = pd.concat([df, df1], axis=1)
    df = df.drop(columns=['Physical_State'])
    # Labels are the values we want to predict
    stat = {'Label': df.Mood.apply(lambda x: label if 
                                   x == label else 'Not ' + label)}
    df = pd.concat([df, pd.DataFrame(stat)], axis=1)
    # Remove the labels from the features
    # axis 1 refers to the columns
    # features = df.drop('Mood', axis=1)
    df2 = df[['HT_Mean', 
              'HT_STD',
              'HT_Skewness',
              'HT_Kurtosis',
              'FT_Mean', 
              'FT_STD',
              'FT_Skewness',
              'FT_Kurtosis',
              'SP_Mean', 
              'SP_STD',
              'SP_Skewness',
              'SP_Kurtosis',
              'PFR_Mean', 
              'PFR_STD',
              'PFR_Skewness',
              'PFR_Kurtosis']]
    features = pd.concat([df2, df1], axis=1)
    
    # features = pd.concat([features, df['Physical_State']], axis=1)
    # Saving feature names for later use
    # feature_list = list(features.columns)
    # Convert to numpy array
    labels = np.array(df['Label'])
    features = np.array(features)

    # Leave One Group Out Cross-Validation
    groups = df['UserID']
    logo = LeaveOneGroupOut()
    user_f1_total = []
    user_auc_total = []

    # LOSO CV
    for train, test in logo.split(features, labels, groups=groups):
        train_features_loso, test_features_loso = features[train], features[test]
        train_labels_loso, test_labels_loso = labels[train], labels[test]

        # All but one users are in train dataset
        # and last user is in test dataset

        # Stratified 5-fold Cross-Validation
        from sklearn.model_selection import StratifiedKFold
        skf = StratifiedKFold(n_splits=5)
        skf.get_n_splits(train_features_loso, train_labels_loso)

        # Debugging
        # print('Training Features Shape:', train_features.shape)
        # print('Training Labels Shape:', train_labels.shape)
        # print('Testing Features Shape:', test_features.shape)
        # print('Testing Labels Shape:', test_labels.shape)
        
        user_f1 = []
        user_auc = []
        for train_index, test_index in skf.split(train_features_loso,
                                                 train_labels_loso):
            train_features = train_features_loso[train_index]
            train_labels = train_labels_loso[train_index].ravel()
            # test_features = train_features_loso[test_index]
            # test_labels = train_labels_loso[test_index].ravel()

            # Stratified k-folds for training dataset
            
            # SMOTE FOR DATA IMBALANCE ON TRAINING DATA
            from imblearn.over_sampling import SMOTE
            sm = SMOTE(random_state=33, k_neighbors=4)
            train_features_new, train_labels_new = \
                sm.fit_sample(train_features, train_labels)
            
            # print('Old: ' + str(len(train_labels)))
            # print('New: ' + str(len(train_labels_new)))
    
            # Instantiate model with 100 decision trees
            clf = RandomForestClassifier(n_estimators=100, random_state=42)
            # Train the model on training data
            clf.fit(train_features_new, train_labels_new)

            # Use the model's predict method on the test data
            # Probabilities for ROCAUC
            predictions_prob = clf.predict_proba(test_features_loso)
            # Absolute Predictions
            predictions = clf.predict(test_features_loso)
            # print(predictions)
            # print(confusion_matrix(test_labels, predictions))

            # print('Test: ', test_labels)
            # print('Predictions: ', predictions)
            # print(classification_report(test_labels, predictions,
            #                             labels=[label, 'Not ' + label]))

            from sklearn.metrics import f1_score
            user_f1.append(f1_score(test_labels_loso, predictions, average='macro'))
                            
            # print(test_labels)
            # print(predictions)

            

            from sklearn.metrics import roc_auc_score
            auc = roc_auc_score(test_labels_loso, predictions_prob[:, 1])
            user_auc.append(auc)
            print(round(auc, 3))

            # metrics.plot_roc_curve(clf, test_features, test_labels)
            # plt.show()

            # FEATURE IMPORTANCE

            # # Get numerical feature importances
            # importances = list(clf.feature_importances_)
            # # List of tuples with variable and importance
            # feature_importances = [(feature, round(importance, 2))
            #                        for feature, importance in 
            #                        zip(features_list, importances)]
            # # Sort the feature importances by most important first
            # feature_importances = sorted(feature_importances, key=lambda x: x[1],
            #                              reverse=True)
            # # Print out the feature and importances 
            # [print('Variable: {:20} Importance: {}'.format(*pair))
            #     for pair in feature_importances]

        user_f1_total.append(pd.Series(user_f1).mean())
        user_auc_total.append(pd.Series(user_auc).mean())

    print('Mean AUC: ' + str(round(pd.Series(user_auc_total).mean(), 3)) + ', STD AUC: ' + 
          str(round(pd.Series(user_auc_total).std(), 3)))
    print('Mean F1: ' + str(round(pd.Series(user_f1_total).mean(), 3)) + ', STD F1: ' + 
          str(round(pd.Series(user_f1_total).std(), 3)))
    


def clasf_user(dirname, label):
    """ Random Forest Classification Per User 
        Makes binary classification (Happy/ Not Happy)
        label = Happy, Sad, Stressed
        neutral = Neutral, No-Neutral
        smote = Smote, No-Smote
        physical = Physical, No-Physical
    """
    os.chdir(dirname)
    p = 0
    auc_scores = []
    f1_scores = []
    print('RANDOM FOREST CLASSIFICATION, ' + label)
    for root, dirs, files in os.walk(os.getcwd(), topdown=True):
        for f in files:
            os.chdir(os.path.abspath(root))
            if f.startswith('output_user.csv'):
                data = pd.read_csv(f)
                df = pd.DataFrame(data)
                df = df.dropna()
                # Don't consider Neutral Labels
                df = df[df.Mood != 'Neutral']
                # Work only with users with sessions > 50
                if len(df[df.Mood == label]) > 50 and df.Mood.nunique() > 1:
                    userid = \
                        str(os.path.abspath(os.path.join(os.getcwd(), "./.")))\
                        .split('/')[-1].split('-')[0]
                    
                    print('UserID: ' + userid)
                    p += 1
                    df1 = pd.DataFrame([])
                    # One Hot Encode for Physical State
                    df1 = pd.get_dummies(df.Physical_State)
                    # Concat features
                    df = pd.concat([df, df1], axis=1)
                    df = df.drop(columns=['Physical_State'])
                    # Labels are the values we want to predict
                    stat = {'Label': df.Mood.apply(lambda x: label if 
                                                   x == label else 'Not ' + label)}
                    df = pd.concat([df, pd.DataFrame(stat)], axis=1)
                    
                    # Remove the labels from the features
                    # axis 1 refers to the columns
                    # features = df.drop('Mood', axis=1)
                    df2 = df[['HT_Mean', 
                              'HT_STD',
                              'HT_Skewness',
                              'HT_Kurtosis',
                              'FT_Mean', 
                              'FT_STD',
                              'FT_Skewness',
                              'FT_Kurtosis',
                              'SP_Mean', 
                              'SP_STD',
                              'SP_Skewness',
                              'SP_Kurtosis',
                              'PFR_Mean', 
                              'PFR_STD',
                              'PFR_Skewness',
                              'PFR_Kurtosis']]
                    features = pd.concat([df2, df1], axis=1)

                    # print('Features are: ')
                    # print(features.columns)
                    print('Class Balance: ' + str(round(len(df[df.Mood == label]) / len(df), 2)))

                    # Transform DF to NP.ARRAYS for modeling
                    # labels = np.array(labels)
                    labels = np.array(df['Label'])
                    features = np.array(features)

                    # SPLITTING OF DATASET

                    # Stratified 5-fold Cross-Validation
                    from sklearn.model_selection import StratifiedKFold
                    skf = StratifiedKFold(n_splits=5)
                    skf.get_n_splits(features, labels)

                    user_f1 = []
                    user_auc = []
                    for train_index, test_index in skf.split(features, labels):
                        train_features = features[train_index]
                        train_labels = labels[train_index].ravel()
                        test_features = features[test_index]
                        test_labels = labels[test_index].ravel()
                        
                        # SMOTE FOR DATA IMBALANCE ON TRAINING DATA
                        from imblearn.over_sampling import SMOTE
                        sm = SMOTE(random_state=33, k_neighbors=4)
                        train_features_new, train_labels_new = \
                            sm.fit_sample(train_features, train_labels)
                        
                        # print('Old: ' + str(len(train_labels)))
                        # print('New: ' + str(len(train_labels_new)))
                
                        # Instantiate model with 100 decision trees
                        clf = RandomForestClassifier(n_estimators=100, random_state=42)
                        # Train the model on training data
                        clf.fit(train_features_new, train_labels_new)

                        # Use the model's predict method on the test data
                        # Probabilities for ROCAUC
                        predictions_prob = clf.predict_proba(test_features)
                        # Absolute Predictions
                        predictions = clf.predict(test_features)
                        # print(predictions)
                        # print(confusion_matrix(test_labels, predictions))

                        # print('Test: ', test_labels)
                        # print('Predictions: ', predictions)
                        print(classification_report(test_labels, predictions,
                                                    labels=[label, 'Not ' + label]))

                        from sklearn.metrics import f1_score
                        user_f1.append(f1_score(test_labels, predictions, average='macro'))
                                        
                        # print(test_labels)
                        # print(predictions)

                        

                        from sklearn.metrics import roc_auc_score
                        auc = roc_auc_score(test_labels, predictions_prob[:, 1])
                        user_auc.append(auc)
                        print(round(auc, 3))

                        # metrics.plot_roc_curve(clf, test_features, test_labels)
                        # plt.show()

                        # FEATURE IMPORTANCE

                        # # Get numerical feature importances
                        # importances = list(clf.feature_importances_)
                        # # List of tuples with variable and importance
                        # feature_importances = [(feature, round(importance, 2))
                        #                        for feature, importance in 
                        #                        zip(features_list, importances)]
                        # # Sort the feature importances by most important first
                        # feature_importances = sorted(feature_importances, key=lambda x: x[1],
                        #                              reverse=True)
                        # # Print out the feature and importances 
                        # [print('Variable: {:20} Importance: {}'.format(*pair))
                        #     for pair in feature_importances]

                    f1_scores.append(pd.Series(user_f1).mean())
                    auc_scores.append(pd.Series(user_auc).mean())
    print('Number of users used: ' + str(p))
    print('Mean AUC: ' + str(round(pd.Series(auc_scores).mean(), 3)) + ', STD AUC: ' + 
          str(round(pd.Series(auc_scores).std(), 3)))
    print('Mean F1: ' + str(round(pd.Series(f1_scores).mean(), 3)) + ', STD F1: ' + 
          str(round(pd.Series(f1_scores).std(), 3)))
    

def logistic_regression_user(dirname, label):
    """ Make Logistic Regression for each user 
        label = Happy, Sad, Stressed
    """
    os.chdir(dirname)
    p = 0
    auc_scores = []
    f1_scores = []
    print('LOGISTIC REGRESSION')
    for root, dirs, files in os.walk(os.getcwd(), topdown=True):
        for f in files:
            os.chdir(os.path.abspath(root))
            if f.startswith('output_user.csv'):
                data = pd.read_csv(f)
                df = pd.DataFrame(data)
                df = df.dropna()
                # Don't consider Neutral Labels
                # df = df[df.Mood != 'Neutral']
                # Work only with users with sessions > 50
                if len(df[df.Mood == label]) > 50 and df.Mood.nunique() > 1:
                    userid = \
                        str(os.path.abspath(os.path.join(os.getcwd(), "./.")))\
                        .split('/')[-1].split('-')[0]
                        
                    print('UserID: ' + userid)
                        
                    p += 1
                    # One Hot Encode for Physical State
                    df1 = pd.get_dummies(df.Physical_State)
                    # Concat features
                    df = pd.concat([df, df1], axis=1)
                    df = df.drop(columns=['Physical_State'])
                    # Labels are the values we want to predict
                    stat = {'Label': df.Mood.apply(lambda x: label if 
                                                   x == label else 'Not ' + label)}
                    df = pd.concat([df, pd.DataFrame(stat)], axis=1)
                    
                    # Remove the labels from the features
                    # axis 1 refers to the columns
                    # features = df.drop('Mood', axis=1)
                    df2 = df[['HT_Mean', 
                              'HT_STD',
                              'HT_Skewness',
                              'HT_Kurtosis',
                              'FT_Mean', 
                              'FT_STD',
                              'FT_Skewness',
                              'FT_Kurtosis',
                              'SP_Mean', 
                              'SP_STD',
                              'SP_Skewness',
                              'SP_Kurtosis',
                              'PFR_Mean', 
                              'PFR_STD',
                              'PFR_Skewness',
                              'PFR_Kurtosis']]
                    features = pd.concat([df2, df1], axis=1)

                    # print('Features are: ')
                    # print(features.columns)
                    print('Class Balance: ' + str(round(len(df[df.Mood == label]) / len(df), 2)))

                    # Transform DF to NP.ARRAYS for modeling
                    # labels = np.array(labels)
                    labels = np.array(df['Label'])
                    features = np.array(features)

                    # SPLITTING OF DATASET
                    # Stratified 5-fold Cross-Validation
                    from sklearn.model_selection import StratifiedKFold
                    skf = StratifiedKFold(n_splits=5)
                    skf.get_n_splits(features, labels)

                    user_f1 = []
                    user_auc = []
                    for train_index, test_index in skf.split(features, labels):
                        train_features = features[train_index]
                        train_labels = labels[train_index].ravel()
                        test_features = features[test_index]
                        test_labels = labels[test_index].ravel()
                        
                        # SMOTE FOR DATA IMBALANCE ON TRAINING DATA
                        # from imblearn.over_sampling import SMOTE
                        # sm = SMOTE(random_state=33, k_neighbors=4)
                        # train_features_new, train_labels_new = \
                        #     sm.fit_sample(train_features, train_labels.ravel())
                        
                        # print('Old: ' + str(len(train_labels)))
                        # print('New: ' + str(len(train_labels_new)))

                        # Debugging
                        # print('Training Features Shape:', train_features.shape)
                        # print('Training Labels Shape:', train_labels.shape)
                        # print('Testing Features Shape:', test_features.shape)
                        # print('Testing Labels Shape:', test_labels.shape)

            
                        
                        # Instantiate model with 1000 decision trees
                        clf = LogisticRegression(solver='liblinear', random_state=42)
                        # Train the model on training data
                        clf.fit(train_features, train_labels)

                        # Use the forest's predict method on the test data
                        predictions_prob = clf.predict_proba(test_features)
                        predictions = clf.predict(test_features)
                        # print(predictions)
                        # print(confusion_matrix(test_labels, predictions))

                        # print('Test: ', test_labels)
                        # print('Predictions: ', predictions)
                        # print(classification_report(test_labels, predictions,
                        #                             labels=[label, 'Not ' + label]))

                        from sklearn.metrics import f1_score
                        f1_scores.append(f1_score(test_labels, predictions, average='macro'))
                                                
                        # print(test_labels)
                        # print(predictions)

                        

                        from sklearn.metrics import roc_auc_score
                        auc = roc_auc_score(test_labels, predictions_prob[:, 1])
                        auc_scores.append(auc)
                        print(round(auc, 3))

                        # metrics.plot_roc_curve(clf, test_features, test_labels)
                        # plt.show()

                        # FEATURE IMPORTANCE

                        # # Get numerical feature importances
                        # importances = list(clf.feature_importances_)
                        # # List of tuples with variable and importance
                        # feature_importances = [(feature, round(importance, 2))
                        #                        for feature, importance in 
                        #                        zip(features_list, importances)]
                        # # Sort the feature importances by most important first
                        # feature_importances = sorted(feature_importances, key=lambda x: x[1],
                        #                              reverse=True)
                        # # Print out the feature and importances 
                        # [print('Variable: {:20} Importance: {}'.format(*pair))
                        #     for pair in feature_importances]
                    f1_scores.append(pd.Series(user_f1).mean())
                    auc_scores.append(pd.Series(user_auc).mean())
    print('Number of users used: ' + str(p))
    print('Mean AUC: ' + str(round(pd.Series(auc_scores).mean(), 3)) + ', STD AUC: ' + 
          str(round(pd.Series(auc_scores).std(), 3)))
    print('Mean F1: ' + str(round(pd.Series(f1_scores).mean(), 3)) + ', STD F1: ' + 
          str(round(pd.Series(f1_scores).std(), 3)))
    

def svm_clf_user(dirname, label):
    """ Make SVM Classification for each user 
        label = Happy, Sad, Stressed
    """
    os.chdir(dirname)
    p = 0
    auc_scores = []
    f1_scores = []
    print('SVM CLASSIFICATION')
    for root, dirs, files in os.walk(os.getcwd(), topdown=True):
        for f in files:
            os.chdir(os.path.abspath(root))
            if f.startswith('output_user.csv'):
                data = pd.read_csv(f)
                df = pd.DataFrame(data)
                df = df.dropna()
                # Don't consider Neutral Labels
                # df = df[df.Mood != 'Neutral']
                # Work only with users with sessions > 50
                if len(df[df.Mood == label]) > 50 and df.Mood.nunique() > 1:
                    userid = \
                        str(os.path.abspath(os.path.join(os.getcwd(), "./.")))\
                        .split('/')[-1].split('-')[0]
                        
                    print('UserID: ' + userid)
                        
                    p += 1
                    # One Hot Encode for Physical State
                    df1 = pd.get_dummies(df.Physical_State)
                    # Concat features
                    df = pd.concat([df, df1], axis=1)
                    df = df.drop(columns=['Physical_State'])
                    # Labels are the values we want to predict
                    stat = {'Label': df.Mood.apply(lambda x: label if 
                                                   x == label else 'Not ' + label)}
                    df = pd.concat([df, pd.DataFrame(stat)], axis=1)
                    
                    # Remove the labels from the features
                    # axis 1 refers to the columns
                    # features = df.drop('Mood', axis=1)
                    df2 = df[['HT_Mean', 
                              'HT_STD',
                              'HT_Skewness',
                              'HT_Kurtosis',
                              'FT_Mean', 
                              'FT_STD',
                              'FT_Skewness',
                              'FT_Kurtosis',
                              'SP_Mean', 
                              'SP_STD',
                              'SP_Skewness',
                              'SP_Kurtosis',
                              'PFR_Mean', 
                              'PFR_STD',
                              'PFR_Skewness',
                              'PFR_Kurtosis']]
                    features = pd.concat([df2, df1], axis=1)

                    # print('Features are: ')
                    # print(features.columns)
                    print('Class Balance: ' + str(round(len(df[df.Mood == label]) / len(df), 2)))

                    # Transform DF to NP.ARRAYS for modeling
                    # labels = np.array(labels)
                    labels = np.array(df['Label'])
                    features = np.array(features)

                    # SPLITTING OF DATASET
                    # Stratified 5-fold Cross-Validation
                    from sklearn.model_selection import StratifiedKFold
                    skf = StratifiedKFold(n_splits=5)
                    skf.get_n_splits(features, labels)

                    user_f1 = []
                    user_auc = []
                    for train_index, test_index in skf.split(features, labels):
                        train_features = features[train_index]
                        train_labels = labels[train_index].ravel()
                        test_features = features[test_index]
                        test_labels = labels[test_index].ravel()
                        
                        # SMOTE FOR DATA IMBALANCE ON TRAINING DATA
                        # from imblearn.over_sampling import SMOTE
                        # sm = SMOTE(random_state=33, k_neighbors=4)
                        # train_features_new, train_labels_new = \
                        #     sm.fit_sample(train_features, train_labels.ravel())
                        
                        # print('Old: ' + str(len(train_labels)))
                        # print('New: ' + str(len(train_labels_new)))

                        # Debugging
                        # print('Training Features Shape:', train_features.shape)
                        # print('Training Labels Shape:', train_labels.shape)
                        # print('Testing Features Shape:', test_features.shape)
                        # print('Testing Labels Shape:', test_labels.shape)

            
                        
                        # Instantiate model with 1000 decision trees
                        clf = svm.SVC(kernel='rbf', gamma='auto', probability=True)
                        # Train the model on training data
                        clf.fit(train_features, train_labels)

                        # Use the forest's predict method on the test data
                        predictions_prob = clf.predict_proba(test_features)
                        predictions = clf.predict(test_features)
                        # print(predictions)
                        # print(confusion_matrix(test_labels, predictions))

                        # print('Test: ', test_labels)
                        # print('Predictions: ', predictions)
                        # print(classification_report(test_labels, predictions,
                        #                             labels=[label, 'Not ' + label]))

                        from sklearn.metrics import f1_score
                        f1_scores.append(f1_score(test_labels, predictions, average='macro'))
                                                
                        # print(test_labels)
                        # print(predictions)

                        

                        from sklearn.metrics import roc_auc_score
                        auc = roc_auc_score(test_labels, predictions_prob[:, 1])
                        auc_scores.append(auc)
                        print(round(auc, 3))

                        # metrics.plot_roc_curve(clf, test_features, test_labels)
                        # plt.show()

                        # FEATURE IMPORTANCE

                        # # Get numerical feature importances
                        # importances = list(clf.feature_importances_)
                        # # List of tuples with variable and importance
                        # feature_importances = [(feature, round(importance, 2))
                        #                        for feature, importance in 
                        #                        zip(features_list, importances)]
                        # # Sort the feature importances by most important first
                        # feature_importances = sorted(feature_importances, key=lambda x: x[1],
                        #                              reverse=True)
                        # # Print out the feature and importances 
                        # [print('Variable: {:20} Importance: {}'.format(*pair))
                        #     for pair in feature_importances]
                    f1_scores.append(pd.Series(user_f1).mean())
                    auc_scores.append(pd.Series(user_auc).mean())
    print('Number of users used: ' + str(p))
    print('Mean AUC: ' + str(round(pd.Series(auc_scores).mean(), 3)) + ', STD AUC: ' + 
          str(round(pd.Series(auc_scores).std(), 3)))
    print('Mean F1: ' + str(round(pd.Series(f1_scores).mean(), 3)) + ', STD F1: ' + 
          str(round(pd.Series(f1_scores).std(), 3)))
