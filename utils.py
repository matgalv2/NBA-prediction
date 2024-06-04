from typing import List

import pandas as pd
from pandas import DataFrame
from sklearn.preprocessing import MinMaxScaler, StandardScaler

from domain import date


def generateSeasons(first, last):
    for year in range(first, last + 1):
        yield f"{year}-{str(year + 1)[2:]}"

def findNextGameID(gameID: int, df: DataFrame):
    df = df.copy()
    df['GAME_DATE'] = df['GAME_DATE'].map(lambda x: date.NBADate.create(x).value)

    teamIDs = {teamId: "" for teamId in df[df["Game_ID"] == gameID]["Team_ID"].tolist()}

    for teamId in teamIDs:
        games = df[df["Team_ID"] == teamId].sort_values(by="GAME_DATE", ascending=False)
        games.reset_index(inplace=True)
        games.drop(columns=["index"], inplace=True)

        gameID_index = games[games["Game_ID"] == gameID].index.values[0]
        next_game_index = gameID_index - 1 if gameID_index != 0 else -1

        if next_game_index < 0:
            teamIDs[teamId] = ""
        else:
            teamIDs[teamId] = games.iloc[gameID_index - 1]["Game_ID"]


    return teamIDs


def findPreviousNGameIDs(gameID: int, teamID: int, df: DataFrame):
    games = df.copy()
    games['GAME_DATE'] = games['GAME_DATE'].map(lambda x: date.NBADate.create(x).value)
    games = games[games["TEAM_ID"] == teamID].sort_values(by="GAME_DATE", ascending=True)
    games.reset_index(inplace=True)
    games.drop(columns=["index"], inplace=True)

    gameID_index = games[games["GAME_ID"] == gameID].index.values[0]

    if gameID_index < 3:
        return []
    else:
        return games.iloc[gameID_index - 3: gameID_index]["GAME_ID"].values.tolist()




def getAverageStatisticsFromLastNGames(teamID:int, gameIDs: List[int], df: DataFrame):
    lastGames = df[df["GAME_ID"].isin(gameIDs)][df["TEAM_ID"] == teamID]
    features = ['FG_PCT', 'FG3_PCT',
    'FT_PCT', 'REB', 'OREB', 'DREB', 'AST', 'STL', 'BLK',
    'OFF_RATING', 'DEF_RATING', 'TS_PCT', "TOV"]

    return lastGames[features].mean().to_dict()


def calculateAverageStatisticsForLast3Games(test_dataset: DataFrame):
    # test_games = test_dataset.copy()
    test_games = test_dataset
    full_stats = pd.read_csv('resources/all-seasons-statistics.tsv', sep='\t')
    for index in test_games.index:
        row = test_games.loc[index]
        game_id = row['GAME_ID']

        home_team_id = row['TEAM_ID_home']
        last_gameIDs_home = findPreviousNGameIDs(game_id, home_team_id, full_stats)
        avg_stats_home = getAverageStatisticsFromLastNGames(home_team_id, last_gameIDs_home, full_stats)

        for key, value in avg_stats_home.items():
            test_games.at[index, key + "_home"] = value

        away_team_id = row['TEAM_ID_away']
        last_gameIDs_away = findPreviousNGameIDs(game_id, away_team_id, full_stats)
        avg_stats_away = getAverageStatisticsFromLastNGames(away_team_id, last_gameIDs_away, full_stats)

        for key, value in avg_stats_away.items():
            test_games.at[index, key + "_away"] = value
    return test_games




def normalizeHomeAndAwayTeamsTogether(raw_dataset: DataFrame):

    home_df = DataFrame()
    away_df = DataFrame()
    dataset = raw_dataset.copy()
    common_columns = ['GAME_ID', 'MATCHUP', 'OUTCOME']

    attributes_to_be_normalized = [
        'FG_PCT', 'FG3_PCT', 'FT_PCT', 'REB', 'OREB', 'DREB', 'AST', 'STL',
        'BLK', 'OFF_RATING', 'DEF_RATING', 'TS_PCT', 'TOV', 'ELO',
        "SENTIMENT"
    ]

    for index in dataset.index:
        row = dataset.loc[index]
        home = {}
        away = {}
        for column in dataset.columns:
            if column in common_columns:
                home[column] = row[column]
                away[column] = row[column]
            elif "_home" in column:
                home[column.removesuffix("_home")] = [row[column]]
            else:
                away[column.removesuffix("_away")] = [row[column]]
        home["IS_HOME"] = [1]
        away["IS_HOME"] = [0]
        home_df = pd.concat([DataFrame(home),home_df], ignore_index=True)
        away_df = pd.concat([DataFrame(away),away_df], ignore_index=True)

    all_stats = pd.concat([home_df, away_df], ignore_index=True)

    scaler = StandardScaler()
    all_stats[attributes_to_be_normalized] = scaler.fit_transform(all_stats[attributes_to_be_normalized])

    home_normalized = all_stats[all_stats["IS_HOME"] == 1].drop(columns=["IS_HOME"])
    away_normalized = all_stats[all_stats["IS_HOME"] == 0].drop(columns=["IS_HOME", "MATCHUP", "OUTCOME"])

    return home_normalized.merge(away_normalized, how="inner", on="GAME_ID", suffixes=("_home", "_away"))











#### Script for creating all seasons stats


# all_seasons_stats = pd.DataFrame()
# for season in generateSeasons(2018, 2023):
#     game_logs = pd.read_csv(f"resources/game-logs/season_{season}.tsv", sep="\t")
#     game_logs.rename(columns={"Game_ID": "GAME_ID", "Team_ID": "TEAM_ID"}, inplace=True)
#
#     per_game_statistics = pd.read_csv(f"resources/per-game-statistics/season_{season}.tsv", sep="\t")
#
#     elo_ratings = pd.read_csv(f'resources/elo-ratings/season_{season}.tsv', sep='\t')
#
#     elo_ratings_teams_x = elo_ratings[["Game_ID", "Team_ID_x", "ELO_x"]]
#     elo_ratings_teams_x.rename(columns={"Game_ID": "GAME_ID", "Team_ID_x": "TEAM_ID", "ELO_x": "ELO"}, inplace=True)
#
#     elo_ratings_teams_y = elo_ratings[["Game_ID", "Team_ID_y", "ELO_y"]]
#     elo_ratings_teams_y.rename(columns={"Game_ID": "GAME_ID", "Team_ID_y": "TEAM_ID", "ELO_y": "ELO"}, inplace=True)
#
#     elo_ratings_simplified = pd.concat([elo_ratings_teams_x, elo_ratings_teams_y], ignore_index=True)
#
#     per_game_statistics_full = per_game_statistics.merge(elo_ratings_simplified, on=['GAME_ID', 'TEAM_ID'])[per_game_statistics_features]
#
#
#
#     full_statistics = game_logs[game_logs_features].merge(per_game_statistics_full, on=["GAME_ID", "TEAM_ID"], how="left")
#     all_seasons_stats = pd.concat([all_seasons_stats, full_statistics])
#
# all_seasons_stats.to_csv("resources/all-seasons-statistics.tsv", index=False, sep='\t')

