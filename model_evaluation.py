import pandas as pd
from sklearn.preprocessing import MinMaxScaler

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



test_raw_dataset = utils.calculateAverageStatisticsForLast3Games(raw_dataset.sample(frac=0.1, random_state=0))

raw_dataset.loc[test_raw_dataset.index] = test_raw_dataset


# raw_dataset = utils.normalizeHomeAndAwayTeamsTogether(raw_dataset)

dataset = utils.normalizeHomeAndAwayTeamsTogether(raw_dataset).drop(columns=columns_to_be_dropped)

test_dataset = dataset.loc[test_raw_dataset.index]
train_dataset = dataset.drop(test_dataset.index)

train_features = train_dataset.copy()
test_features = test_dataset.copy()

train_labels = train_features.pop('OUTCOME')
test_labels = test_features.pop('OUTCOME')




print(dataset.describe().transpose())



