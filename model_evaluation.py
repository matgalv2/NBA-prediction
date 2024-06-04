import pandas as pd
import numpy as np
import sklearn
from matplotlib import pyplot as plt
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier

from sklearn.metrics import *

import utils

attributes_to_be_normalized = [
    'FG_PCT_home',
    'FG3_PCT_home', 'FT_PCT_home', 'REB_home', 'OREB_home', 'DREB_home', 'AST_home','STL_home',
    'BLK_home', 'OFF_RATING_home', 'DEF_RATING_home', 'TS_PCT_home', 'TOV_home', 'ELO_home',
    "SENTIMENT_home", 'FG_PCT_away', 'FG3_PCT_away',
    'FT_PCT_away', 'REB_away', 'OREB_away', 'DREB_away', 'AST_away', 'STL_away', 'BLK_away',
    'OFF_RATING_away', 'DEF_RATING_away', 'TS_PCT_away', 'TOV_away', 'ELO_away', "SENTIMENT_away"
]

columns_to_be_dropped = ['GAME_ID', 'MATCHUP','TEAM_ID_home','TEAM_ABBREVIATION_home',
                         'TEAM_ID_away','TEAM_ABBREVIATION_away']


raw_dataset = pd.read_csv('resources/datasets/data.csv', sep='\t')


train_raw_dataset = raw_dataset.sample(frac=0.9, random_state=0)
test_raw_dataset = raw_dataset.drop(train_raw_dataset.index)

test_raw_dataset_rebased = utils.calculateAverageStatisticsForLast3Games(test_raw_dataset)

raw_dataset.loc[test_raw_dataset_rebased.index] = test_raw_dataset_rebased


dataset = utils.normalizeHomeAndAwayTeamsTogether(raw_dataset).drop(columns=columns_to_be_dropped)

test_dataset = dataset.loc[test_raw_dataset_rebased.index]
train_dataset = dataset.drop(test_dataset.index)

train_features = train_dataset.copy()
test_features = test_dataset.copy()

train_labels = train_features.pop('OUTCOME')
test_labels = test_features.pop('OUTCOME')



results = {
    "basic": [],
    "norm": [],
    "no_sent": [],
    "no_elo": []
}

# random_state random forest - 1




from sklearn import metrics, svm




model = svm.SVC(probability=True, kernel='poly', C=1.0, degree=3)

model2 = LogisticRegression(solver='liblinear', C=1, penalty='l1')
model3 = GaussianNB()




model.fit(train_features, train_labels)
model2.fit(train_features, train_labels)
model3.fit(train_features, train_labels)


#set up plotting area
plt.figure(0).clf()

#fit logistic regression model and plot ROC curve

y_pred = model.predict_proba(test_features)[:, 1]
fpr, tpr, _ = metrics.roc_curve(test_labels, y_pred)
auc = round(metrics.roc_auc_score(test_labels, y_pred), 4)
plt.plot(fpr,tpr,label=f"SVM (AUC={auc})")


y_pred = model2.predict_proba(test_features)[:, 1]
fpr, tpr, _ = metrics.roc_curve(test_labels, y_pred)
auc = round(metrics.roc_auc_score(test_labels, y_pred), 4)
plt.plot(fpr,tpr,label=f"Logistic regression (AUC={auc}")

y_pred = model2.predict_proba(test_features)[:, 1]
fpr, tpr, _ = metrics.roc_curve(test_labels, y_pred)
auc = round(metrics.roc_auc_score(test_labels, y_pred), 4)
plt.plot(fpr,tpr,label=f"Logistic regression (AUC={auc}")

#add legend
plt.legend()
plt.show()





















# for random_state in range(10):
#     print("Random state {}".format(random_state), "--------------------------------------")
#     model = MLPClassifier(hidden_layer_sizes=(128,), activation='relu',alpha=0.01, solver='sgd', learning_rate='adaptive', learning_rate_init=0.0001, max_iter=5000, random_state=random_state)
#     # model = RandomForestClassifier(n_estimators=20, max_features=14, max_depth=60, min_samples_split=4, min_samples_leaf=4, bootstrap=True, random_state=random_state)
#     # model = LogisticRegression(solver='liblinear', C=1, penalty='l1', random_state=random_state)
#     # model = GaussianNB()
#     # model = svm.SVC(kernel='poly', C=1.0, degree=3)
#     model.fit(train_features, train_labels)
#     results["norm"].append(accuracy_score(test_labels, model.predict(test_features)))
#
#     model = MLPClassifier(hidden_layer_sizes=(128,), activation='relu',alpha=0.01, solver='sgd', learning_rate='adaptive', learning_rate_init=0.0001, max_iter=5000, random_state=random_state)
#     # model = RandomForestClassifier(n_estimators=20, max_features=14, max_depth=60, min_samples_split=4, min_samples_leaf=4, bootstrap=True, random_state=random_state)
#     # model = LogisticRegression(solver='liblinear', C=1, penalty='l1', random_state=random_state)
#     # model = GaussianNB()
#     # model = svm.SVC(kernel='poly', C=1.0, degree=3)
#     model.fit(train_features.drop(columns=["ELO_home", "ELO_away"]), train_labels)
#     results["no_elo"].append(accuracy_score(test_labels, model.predict(test_features.drop(columns=["ELO_home", "ELO_away"]))))
#
#     model = MLPClassifier(hidden_layer_sizes=(128,), activation='relu',alpha=0.01, solver='sgd', learning_rate='adaptive', learning_rate_init=0.0001, max_iter=5000, random_state=random_state)
#     # model = RandomForestClassifier(n_estimators=20, max_features=14, max_depth=60, min_samples_split=4, min_samples_leaf=4, bootstrap=True, random_state=random_state)
#     # model = LogisticRegression(solver='liblinear', C=1, penalty='l1', random_state=random_state)
#     # model = GaussianNB()
#     # model = svm.SVC(kernel='poly', C=1.0, degree=3)
#     model.fit(train_features.drop(columns=["SENTIMENT_home", "SENTIMENT_away"]), train_labels)
#     results["no_sent"].append(accuracy_score(test_labels, model.predict(test_features.drop(columns=["SENTIMENT_home", "SENTIMENT_away"]))))
#
#     model = MLPClassifier(hidden_layer_sizes=(128,), activation='relu',alpha=0.01, solver='sgd', learning_rate='adaptive', learning_rate_init=0.0001, max_iter=5000, random_state=random_state)
#     # model = RandomForestClassifier(n_estimators=20, max_features=14, max_depth=60, min_samples_split=4, min_samples_leaf=4, bootstrap=True, random_state=random_state)
#     # model = LogisticRegression(solver='liblinear', C=1, penalty='l1', random_state=random_state)
#     # model = GaussianNB()
#     # model = svm.SVC(kernel='poly', C=1.0, degree=3)
#     model.fit(train_features.drop(columns=["SENTIMENT_home", "SENTIMENT_away", "ELO_home", "ELO_away"]), train_labels)
#     results["basic"].append(
#         accuracy_score(test_labels, model.predict(test_features.drop(columns=["SENTIMENT_home", "SENTIMENT_away", "ELO_home", "ELO_away"]))))
#
#     for key, value in results.items():
#         print(key, np.mean(value))