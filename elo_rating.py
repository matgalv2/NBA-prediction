import numpy as np
from pandas import read_csv, DataFrame, merge

from domain import date
from domain.matchup import getHomeTeamIDByMatchUp

basic_elo_rating = 1500


def estimatedScore(elo_rating_player, elo_rating_opponent) -> float:
    return 1 / (1 + 10 ** ((elo_rating_opponent - elo_rating_player) / 400))


def updatedEloRating(old_elo, actual_score, estimated_score, k_factor):
    """
    :param old_elo:
    :param actual_score:
    :param estimated_score:
    :param k_factor:
    :return:
    """
    return old_elo + k_factor * (actual_score - estimated_score)


def kFactor(margin_of_victory, elo_difference):
    """
    :param margin_of_victory: the difference between points scored by winner and points scored by loser
    :param elo_difference: the difference between winner's elo rating and loser's elo rating
    :return: K factor with base value equals 20
    """
    numerator = (margin_of_victory + 3) ** 0.8
    denominator = 7.5 + 0.006 * elo_difference
    return 20 * numerator / denominator


def enrichSeasonGameLogsWithElo(game_logs: DataFrame, team_details: DataFrame):
    teamIDs = set(game_logs["Team_ID"])

    ratings = {teamID: basic_elo_rating for teamID in teamIDs}
    games = game_logs[["Game_ID", "GAME_DATE", "Team_ID", "WL", "PTS", "MATCHUP"]]
    columns_to_drop = ["GAME_DATE", "MATCHUP"]

    df = merge(games, games.drop(columns=columns_to_drop), on="Game_ID", how='inner')
    df = df[df["Team_ID_x"] != df["Team_ID_y"]].drop_duplicates(subset=["Game_ID"])
    df['GAME_DATE'] = df['GAME_DATE'].map(lambda x: date.NBADate.create(x).value)
    df = df.sort_values(by=["GAME_DATE", "Game_ID"])
    df["ELO_x"] = np.nan
    df["ELO_y"] = np.nan

    for i in range(len(df.values)):

        row = df.iloc[i].to_dict()
        # assigning elo to game logs
        teamID_x = row["Team_ID_x"]
        row["ELO_x"] = ratings[teamID_x]
        teamID_y = row["Team_ID_y"]
        row["ELO_y"] = ratings[teamID_y]

        df.iloc[i] = row

        # calculating new elo ratings
        actual_score_x = 1 if row["WL_x"] == "W" else 0
        actual_score_y = 1 if row["WL_y"] == "W" else 0

        team_x_elo = ratings[teamID_x]
        team_y_elo = ratings[teamID_y]

        # home team gets +100 elo
        home_team_id = getHomeTeamIDByMatchUp(row["MATCHUP"], team_details)

        if home_team_id == teamID_x:
            team_x_elo += 100
        else:
            team_y_elo += 100

        if row["WL_x"] == "W":
            elo_diff = team_x_elo - team_y_elo
        else:
            elo_diff = team_y_elo - team_x_elo

        mov = abs(row["PTS_x"] - row["PTS_y"])
        k_factor = kFactor(mov, elo_diff)

        estimated_score_x = estimatedScore(team_x_elo, team_y_elo)
        estimated_score_y = estimatedScore(team_y_elo, team_x_elo)

        ratings[teamID_x] = round(updatedEloRating(ratings[teamID_x], actual_score_x, estimated_score_x, k_factor))
        ratings[teamID_y] = round(updatedEloRating(ratings[teamID_y], actual_score_y, estimated_score_y, k_factor))

    return df


# def enrichLogsWithElo(seasons: List[str]):
#     teamIDs = set(game_logs["Team_ID"])
#
#     ratings = {teamID: basic_elo_rating for teamID in teamIDs}


dataset = read_csv("resources/game-logs/season_2019-20.tsv", sep='\t')
team_details = read_csv("resources/teams_details.tsv", sep='\t')
print(enrichSeasonGameLogsWithElo(dataset, team_details, ))
