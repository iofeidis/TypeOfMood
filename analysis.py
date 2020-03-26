# analysis.py
#
# Script for analyzing and modeling keystrokes for 
# PHQ9 regression and Mood classification
# for Android devices and iOS
#
# Iason Ofeidis 2019

# Use numpy to convert to arrays
import numpy as np


# PHQ9 Regression


def regression(df):
    # Make binary classification (Happy/ Not Happy)
    # list1 = ['Neutral', 'Stressed', 'Sad']
    # for i in list1:
    #     df = df.replace(i, 'Not Happy')
    # print(df)

    # Labels are the values we want to predict
    labels = np.array(df['User_PHQ9'])
    # Remove the labels from the features
    # axis 1 refers to the columns
    # features = df.drop('Mood', axis=1)
    features = df.loc[:, 'HT_Mean':'Delete_Rate']
    # Saving feature names for later use
    # feature_list = list(features.columns)
    # Convert to numpy array
    features = np.array(features)


    from sklearn.model_selection import LeaveOneGroupOut

    groups = df['UserID']
    logo = LeaveOneGroupOut()
    accuracies = []
    maes = []
    for train, test in logo.split(features, labels, groups=groups):
        train_features, test_features = features[train], features[test]
        train_labels, test_labels = labels[train], labels[test]

        # # Using Skicit-learn to split data into training and testing sets
        # from sklearn.model_selection import train_test_split
        # # Random Splitting
        # # Split the data into training and testing sets
        # train_features, test_features, train_labels, test_labels =\
        #     train_test_split(features, labels, test_size=0.25, random_state=42)
    

        # Debugging
        # print('Training Features Shape:', train_features.shape)
        # print('Training Labels Shape:', train_labels.shape)
        # print('Testing Features Shape:', test_features.shape)
        # print('Testing Labels Shape:', test_labels.shape)
        
        # Import the model we are using
        from sklearn.ensemble import RandomForestRegressor
        # Instantiate model with 1000 decision trees
        rf = RandomForestRegressor(n_estimators=100, random_state=42)
        # Train the model on training data
        rf.fit(train_features, train_labels)

        # Use the forest's predict method on the test data
        predictions = rf.predict(test_features)
        # Calculate the absolute errors
        # errors = abs(predictions - test_labels)
        # Print out the mean absolute error (mae)
        # print('Mean Absolute Error:', round(np.mean(errors), 2), 'degrees.')

        # Calculate mean absolute percentage error (MAPE)
        # mape = 100 * (errors / test_labels)
        # Calculate and display accuracy

        from sklearn.metrics import mean_absolute_error
        mae = mean_absolute_error(test_labels, predictions)
        print('MAE:' + str(round(mae, 2)))
        maes.append(mae)
        accuracy = 100 - round(mae, 2)
        accuracies.append(accuracy)
        print('Accuracy:', round(accuracy, 2), '%.')
        # from pprint import pprint

        # Look at parameters used by our current forest
        # print('Parameters currently in use:\n')
        # pprint(rf.get_params())

        # # Get numerical feature importances
        # importances = list(rf.feature_importances_)
        # # List of tuples with variable and importance
        # feature_importances = [(feature, round(importance, 2))
        #                        for feature, importance in 
        #                        zip(feature_list, importances)]
        # # Sort the feature importances by most important first
        # feature_importances = sorted(feature_importances, key=lambda x: x[1],
        #                              reverse=True)
        # # Print out the feature and importances 
        # [print('Variable: {:20} Importance: {}'.format(*pair))
        #     for pair in feature_importances]

    print('Mean Absolute Error:' + str(np.mean(maes)))
    print('Mean Accuracy:' + str(np.mean(accuracies)))

# Mood Classification (Happy)
