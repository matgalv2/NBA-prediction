import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn.preprocessing import MinMaxScaler

from utils import generateSeasons


per_game_statistics_features = [
    'GAME_ID', 'TEAM_ID', 'TEAM_ABBREVIATION', 'FG_PCT', 'FG3_PCT',
    'FT_PCT', 'REB', 'OREB', 'DREB', 'AST', 'STL', 'BLK',
    'OFF_RATING', 'DEF_RATING', 'TS_PCT', "ELO"
]
game_logs_features = ["Game_ID", "MATCHUP", "Team_ID", "WL", "TOV"]


final_order_columns = [
    'GAME_ID', 'MATCHUP', 'OUTCOME', 'TEAM_ID_home', 'TEAM_ABBREVIATION_home', 'FG_PCT_home',
    'FG3_PCT_home', 'FT_PCT_home', 'REB_home', 'OREB_home', 'DREB_home', 'AST_home','STL_home',
    'BLK_home', 'OFF_RATING_home', 'DEF_RATING_home', 'TS_PCT_home', 'TOV_home', 'ELO_home',
    "SENTIMENT_home", 'TEAM_ID_away', 'TEAM_ABBREVIATION_away', 'FG_PCT_away', 'FG3_PCT_away',
    'FT_PCT_away', 'REB_away', 'OREB_away', 'DREB_away', 'AST_away', 'STL_away', 'BLK_away',
    'OFF_RATING_away', 'DEF_RATING_away', 'TS_PCT_away', 'TOV_away', 'ELO_away', "SENTIMENT_away"
]


final_order_columns_no_sentiment = [
    'GAME_ID', 'MATCHUP', 'OUTCOME', 'TEAM_ID_home', 'TEAM_ABBREVIATION_home', 'FG_PCT_home',
    'FG3_PCT_home', 'FT_PCT_home', 'REB_home', 'OREB_home', 'DREB_home', 'AST_home','STL_home',
    'BLK_home', 'OFF_RATING_home', 'DEF_RATING_home', 'TS_PCT_home', 'TOV_home', 'ELO_home',
    'TEAM_ID_away', 'TEAM_ABBREVIATION_away', 'FG_PCT_away', 'FG3_PCT_away',
    'FT_PCT_away', 'REB_away', 'OREB_away', 'DREB_away', 'AST_away', 'STL_away', 'BLK_away',
    'OFF_RATING_away', 'DEF_RATING_away', 'TS_PCT_away', 'TOV_away', 'ELO_away'
]

attributes_to_be_normalized = [
    'FG_PCT_home',
    'FG3_PCT_home', 'FT_PCT_home', 'REB_home', 'OREB_home', 'DREB_home', 'AST_home','STL_home',
    'BLK_home', 'OFF_RATING_home', 'DEF_RATING_home', 'TS_PCT_home', 'TOV_home', 'ELO_home',
    "SENTIMENT_home", 'FG_PCT_away', 'FG3_PCT_away',
    'FT_PCT_away', 'REB_away', 'OREB_away', 'DREB_away', 'AST_away', 'STL_away', 'BLK_away',
    'OFF_RATING_away', 'DEF_RATING_away', 'TS_PCT_away', 'TOV_away', 'ELO_away', "SENTIMENT_away"
]


if __name__ == '__main__':
    data = DataFrame()
    # for season in generateSeasons(2018, 2023):
    for season in generateSeasons(2023, 2023):

        per_game_statistics = pd.read_csv(f'resources/per-game-statistics/season_{season}.tsv', sep='\t')
        elo_ratings = pd.read_csv(f'resources/elo-ratings/season_{season}.tsv', sep='\t')

        elo_ratings_teams_x = elo_ratings[["Game_ID", "Team_ID_x", "ELO_x"]]
        elo_ratings_teams_x.rename(columns={"Game_ID": "GAME_ID", "Team_ID_x": "TEAM_ID", "ELO_x": "ELO"}, inplace=True)

        elo_ratings_teams_y = elo_ratings[["Game_ID", "Team_ID_y", "ELO_y"]]
        elo_ratings_teams_y.rename(columns={"Game_ID": "GAME_ID", "Team_ID_y": "TEAM_ID", "ELO_y": "ELO"}, inplace=True)

        elo_ratings_simplified = pd.concat([elo_ratings_teams_x, elo_ratings_teams_y], ignore_index=True)

        per_game_statistics_full = per_game_statistics.merge(elo_ratings_simplified, on=['GAME_ID', 'TEAM_ID'])[per_game_statistics_features]

        # place for adding sentiment analysis
        sentiment = pd.read_csv(f'resources/sentiment-analysis/next-game-sentiment.tsv', sep='\t')
        sentiment.rename(columns={"GAME_ID": "PREVIOUS_GAME_ID", "NEXT_GAME_ID": "GAME_ID"}, inplace=True)
        per_game_statistics_full = per_game_statistics_full.merge(sentiment, on=['GAME_ID', 'TEAM_ID'], how='inner')

        game_logs = pd.read_csv(f"resources/game-logs/season_{season}.tsv", sep='\t')[game_logs_features]

        home_matchups = game_logs[game_logs["MATCHUP"].str.contains(".vs")]
        away_matchups = game_logs[game_logs["MATCHUP"].str.contains("@")]

        games = home_matchups.merge(away_matchups, how="inner", on="Game_ID", suffixes=("_home", "_away"))
        games["WL_home"] = games["WL_home"].map(lambda result: 1 if result == "W" else 0)
        games.rename(columns={"Game_ID": "GAME_ID", "Team_ID_home": "TEAM_ID_home", "Team_ID_away": "TEAM_ID_away", "WL_home": "OUTCOME", "MATCHUP_home": "MATCHUP"}, inplace=True)

        games = games.drop(columns=["MATCHUP_away", "WL_away"])

        matchups = per_game_statistics_full.merge(per_game_statistics_full, on=['GAME_ID'], suffixes=("_home", "_away"))

        matchups = matchups[matchups["TEAM_ID_home"] != matchups["TEAM_ID_away"]]

        matchups = matchups.merge(games, how="inner", on=["GAME_ID", "TEAM_ID_home", "TEAM_ID_away"])

        data = pd.concat([data, matchups])

    # scaler = MinMaxScaler(feature_range=(0, 1))
    # data[attributes_to_be_normalized] = scaler.fit_transform(data[attributes_to_be_normalized])
    data[final_order_columns].to_csv(f"resources/datasets/data.csv", sep='\t', index=False)

