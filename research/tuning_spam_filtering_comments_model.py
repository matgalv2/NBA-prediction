from typing import TextIO

import pandas as pd
import os

from sklearn import svm
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold, GridSearchCV, train_test_split

import nltk
from nltk.corpus import stopwords
from nltk.stem import *

# def hypertune_svm(x, y, file: TextIO, technique:str):
#     model = svm.SVC()
#     kernel = ['linear', 'rbf', 'sigmoid']
#     C = [1000, 100, 50, 10, 1.0, 0.1, 0.01]
#
#     grid = dict(kernel=kernel,C=C)
#
#     cv = KFold(n_splits=10)
#     grid_search = GridSearchCV(estimator=model, param_grid=grid, n_jobs=-1, cv=cv, scoring='precision', error_score=0, verbose=2)
#     grid_result = grid_search.fit(x, y)
#
#     means = grid_result.cv_results_['mean_test_score']
#     params = grid_result.cv_results_['params']
#     for mean, param in zip(means, params):
#         c, kernel = param["C"], param["kernel"]
#         file.write(f"{technique}\t{kernel}\t{c}\t-\t{round(mean,5)}\n")
#
#     kernel2 = ['poly']
#     degree = range(1, 11)
#     grid2 = dict(kernel=kernel2,C=C,degree=degree)
#
#
#     grid_search = GridSearchCV(estimator=model, param_grid=grid2, n_jobs=-1, cv=cv, scoring='precision', error_score=0,verbose=2)
#     grid_result = grid_search.fit(x, y)
#
#     means = grid_result.cv_results_['mean_test_score']
#     params = grid_result.cv_results_['params']
#     for mean, param in zip(means, params):
#         c, degree, kernel = param["C"], param["degree"],param["kernel"]
#         file.write(f"{technique}\t{kernel}\t{c}\t{degree}\t{round(mean, 5)}\n")


def hypertune_lgr(x, y, file: TextIO, technique:str):
    model = LogisticRegression(max_iter=10000)

    penalty1 = ['l1']
    solvers1 = ['saga', 'liblinear']
    # c_values = [1000, 100, 50, 10, 1.0, 0.1, 0.01]
    c_values = [0.01]
    lgr_grid1 = dict(solver=solvers1, penalty=penalty1, C=c_values)

    penalty2 = ['l2']
    solvers2 = ['lbfgs', 'liblinear', 'newton-cg', 'newton-cholesky', 'sag', 'saga']
    lgr_grid2 = dict(solver=solvers2, penalty=penalty2, C=c_values)

    cv = KFold(n_splits=10)

    grid_search1 = GridSearchCV(estimator=model, param_grid=lgr_grid1, n_jobs=-1, cv=cv, scoring='accuracy', error_score=0, verbose=2)
    grid_result1 = grid_search1.fit(x, y)

    means = grid_result1.cv_results_['mean_test_score']
    params = grid_result1.cv_results_['params']
    combinations1 =  zip(means, params)

    for mean, param in combinations1:
        c, penalty, solver = param["C"], param["penalty"], param["solver"]
        file.write(f"{technique}\t{c}\t{penalty}\t{solver}\t{round(mean, 5)}\n")

    grid_search2 = GridSearchCV(estimator=model, param_grid=lgr_grid2, n_jobs=-1, cv=cv, scoring='accuracy',
                               error_score=0, verbose=2)
    grid_result2 = grid_search2.fit(x, y)

    means = grid_result2.cv_results_['mean_test_score']
    params = grid_result2.cv_results_['params']
    combinations2 = zip(means, params)

    for mean, param in combinations2:
        c, penalty, solver = param["C"], param["penalty"], param["solver"]
        file.write(f"{technique}\t{c}\t{penalty}\t{solver}\t{round(mean, 5)}\n")



if __name__ == '__main__':
    path = "X:/ProgramFiles/JetBrains/PycharmProjects/NBA-predictor/resources"

    filenames = os.listdir(path + '/comments')
    comments = [pd.read_csv(path + '/comments/' + filename, sep='\t') for filename in filenames]

    dataset = pd.concat(comments)
    dataset["SPAM"] = dataset["TEAM_ABBREVIATION"].apply(lambda x: 1 if x == "SPAM" else 0)

    nltk.download('wordnet')

    stop_words = stopwords.words("english")
    vectorizer = CountVectorizer(stop_words=stop_words, max_features= 5000)


    X = dataset["COMMENT"]
    Y = dataset["SPAM"]

    wnl = WordNetLemmatizer()
    stemmer = PorterStemmer()

    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

    with open(path + "/researches/spam-filtering-comments-svm.tsv", 'w') as file:
        # file.write(f"technique\tkernel\tC\tgamma\tdegree\tprecision\n")
        file.write(f"technique\tC\tregularization\tsolver\taccuracy\n")


        X_lem = vectorizer.fit_transform(X_train.apply(wnl.lemmatize))
        hypertune_svm(X_lem, y_train, file, "lemmatization")
        # hypertune_lgr(X_lem, y_train, file, "lemmatization")

        X_stem = vectorizer.fit_transform(X_train.apply(stemmer.stem))
        hypertune_svm(X_stem, y_train, file, "stemming")
        # hypertune_lgr(X_stem, y_train, file, "stemming")





