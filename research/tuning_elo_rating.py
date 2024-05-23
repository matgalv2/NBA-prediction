import numpy as np
import pandas as pd
from pandas import read_csv, DataFrame
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import RepeatedStratifiedKFold, GridSearchCV, KFold, cross_val_score

from elo_rating import enrichLogsWithElo, simple_kFactor
from utils import generateSeasons


def generateEloParameters(k0_range=(2,20,2), lambda_range=(0.2,2.0,0.2), basic_elo_rating_range=(500,1800,100)):
    for basic_elo_rating in range(*basic_elo_rating_range):
        for k0 in range(*k0_range):
            for lambda_exp in np.arange(*lambda_range):
                yield basic_elo_rating,k0,lambda_exp


def hypertune_logistic_regression(x, y):
    model = LogisticRegression()
    # solvers = ['newton-cg', 'lbfgs', 'liblinear']
    solvers = ['saga', 'liblinear']
    penalty = ['l1', 'l2']
    c_values = [100, 10, 1.0, 0.1, 0.01]
    # define grid search
    grid = dict(solver=solvers, penalty=penalty, C=c_values)
    cv = KFold(n_splits=10)
    grid_search = GridSearchCV(estimator=model, param_grid=grid, n_jobs=-1, cv=cv, scoring='accuracy', error_score=0)
    grid_result = grid_search.fit(x, y)
    print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
    means = grid_result.cv_results_['mean_test_score']
    stds = grid_result.cv_results_['std_test_score']
    params = grid_result.cv_results_['params']
    for mean, stdev, param in zip(means, stds, params):
        print("%f (%f) with: %r" % (mean, stdev, param))


def evaluate_elo_parameters(dataset_elo: DataFrame):
    dataset_elo['sub'] = dataset_elo["ELO_x"] - dataset_elo["ELO_y"]
    dataset_elo["target"] =  dataset_elo["WL_x"].map(lambda result: 1 if result == "W" else 0)

    x = np.array(dataset_elo['sub'].tolist()).reshape(-1, 1)
    y = np.array(dataset_elo['target'].tolist()).reshape(-1, 1)

    model = LogisticRegression(C=100, penalty='l1', solver='liblinear')
    scores_acc = cross_val_score(model, x, y, cv=10, scoring='accuracy')
    scores_precision = cross_val_score(model, x, y, cv=10, scoring='precision')
    scores_recall = cross_val_score(model, x, y, cv=10, scoring='recall')
    scores_f1 = cross_val_score(model, x, y, cv=10, scoring='f1')
    scores_roc_auc = cross_val_score(model, x, y, cv=10, scoring='roc_auc')
    return round(scores_acc.mean(),4), round(scores_precision.mean(),4), round(scores_recall.mean(),4), round(scores_f1.mean(),4), round(scores_roc_auc.mean(),4)





if __name__ == "__main__":
    absolute_path = "X:/ProgramFiles/JetBrains/PycharmProjects/NBA-predictor/resources"
    data = [
        read_csv(f'{absolute_path}/elo-ratings/season_{season}.tsv',
                 sep='\t') for season in generateSeasons(2018, 2023)]
    dataset = DataFrame(data=pd.concat(data))
    with open(f"{absolute_path}/researches/elo_parameters.tsv", 'a') as file:
        file.write("Basic ELO\tk0\tlambda\taccuracy\tprecision\trecall\tf1\troc_auc\n")

        accuracy, precision, recall, f1, roc_auc = evaluate_elo_parameters(dataset)
        file.write(f"{1500}\t{20}\t{float('nan')}\t{accuracy}\t{precision}\t{recall}\t{f1}\t{roc_auc}\n")

        team_details = read_csv(f"{absolute_path}/teams_details.tsv", sep='\t')
        teamIDs = team_details['id']
        game_logs_per_season = {}
        for season in generateSeasons(2018, 2023):
            game_logs_per_season[season] = read_csv(f"{absolute_path}/game-logs/season_{season}.tsv", sep='\t')

        for basic_elo, k0, lambda_exp in generateEloParameters():
            print(f"Basic elo: {basic_elo}, k0: {k0}, lambda: {lambda_exp}")
            matchups_with_elo = enrichLogsWithElo(teamIDs, team_details, game_logs_per_season, basic_elo, simple_kFactor, basic_elo=basic_elo, k0=k0, lambda_exp=lambda_exp)

            data = [matchups_elo for matchups_elo in matchups_with_elo.values()]
            dataset = DataFrame(data=pd.concat(data))
            accuracy, precision, recall, f1, roc_auc = evaluate_elo_parameters(dataset)
            file.write(f"{basic_elo}\t{k0}\t{lambda_exp}\t{accuracy}\t{precision}\t{recall}\t{f1}\t{roc_auc}\n")