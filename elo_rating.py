from typing import Dict, List

import numpy as np
from pandas import read_csv, DataFrame, merge

from domain import date
from domain.matchup import getHomeTeamIDByMatchUp
from utils import generateSeasons


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


def kFactor(margin_of_victory, elo_difference, **kwargs):
    """
    :param margin_of_victory: the difference between points scored by winner and points scored by loser
    :param elo_difference: the difference between winner's elo rating and loser's elo rating
    :return: K-factor with base value equals 20
    """
    numerator = (margin_of_victory + 3) ** 0.8
    denominator = 7.5 + 0.006 * elo_difference
    return 20 * numerator / denominator


def simple_kFactor(margin_of_victory, elo_difference, k0=20, lambda_exp=0.5, **kwargs):
    """
    :param margin_of_victory: the difference between points scored by winner and points scored by loser
    :param elo_difference: the difference between winner's elo rating and loser's elo rating
    :param k0:
    :param lambda_exp:
    :return: K-factor with base value equals 20
    """
    return k0 * ((1 + margin_of_victory) ** lambda_exp)


def enrichSeasonGameLogsWithElo(matchups: DataFrame, team_details: DataFrame, ratings: Dict[str, int], kFactor_func, **kwargs):
    for i in range(len(matchups.values)):

        row = matchups.iloc[i].to_dict()
        # assigning elo to game logs
        teamID_x = row["Team_ID_x"]
        row["ELO_x"] = ratings[teamID_x]
        teamID_y = row["Team_ID_y"]
        row["ELO_y"] = ratings[teamID_y]

        matchups.iloc[i] = row

        # calculating new elo ratings
        actual_score_x = 1 if row["WL_x"] == "W" else 0
        actual_score_y = 1 if row["WL_y"] == "W" else 0

        team_x_elo = ratings[teamID_x]
        team_y_elo = ratings[teamID_y]

        # home team gets +100 elo
        home_team_id = getHomeTeamIDByMatchUp(row["MATCHUP"], team_details)

        if home_team_id == teamID_x:
            team_x_elo += 100 * kwargs["basic_elo"]/1500
        else:
            team_y_elo += 100 * kwargs["basic_elo"]/1500

        if row["WL_x"] == "W":
            elo_diff = team_x_elo - team_y_elo
        else:
            elo_diff = team_y_elo - team_x_elo

        mov = abs(row["PTS_x"] - row["PTS_y"])
        k_factor = kFactor_func(mov, elo_diff, **kwargs)

        estimated_score_x = estimatedScore(team_x_elo, team_y_elo)
        estimated_score_y = estimatedScore(team_y_elo, team_x_elo)

        ratings[teamID_x] = round(updatedEloRating(ratings[teamID_x], actual_score_x, estimated_score_x, k_factor))
        ratings[teamID_y] = round(updatedEloRating(ratings[teamID_y], actual_score_y, estimated_score_y, k_factor))

    return matchups


def eloYearToYearCarryOver(old_elo: int) -> int:
    return int((.75 * old_elo) + (.25 * 1505))


def enrichLogsWithElo(teamIDs: List[str], team_details: DataFrame, game_logs_per_season: Dict[str,DataFrame], basic_elo_rating, kFactor_func, **kwargs):
    elo_ratings = {teamID: basic_elo_rating for teamID in teamIDs}

    all_season_matchups_with_elo: Dict[str,DataFrame] = {}

    for season, game_logs in game_logs_per_season.items():
        matchups = game_logs[["Game_ID", "GAME_DATE", "Team_ID", "WL", "PTS", "MATCHUP"]]
        columns_to_drop = ["GAME_DATE", "MATCHUP"]

        matchups = merge(matchups, matchups.drop(columns=columns_to_drop), on="Game_ID", how='inner')

        matchups = matchups[matchups["Team_ID_x"] != matchups["Team_ID_y"]].drop_duplicates(subset=["Game_ID"])
        matchups['GAME_DATE'] = matchups['GAME_DATE'].map(lambda x: date.NBADate.create(x).value)

        matchups = matchups.sort_values(by=["GAME_DATE", "Game_ID"])

        matchups["ELO_x"] = np.nan
        matchups["ELO_y"] = np.nan

        kwargs.update(basic_elo=basic_elo_rating)

        matchups_elo = enrichSeasonGameLogsWithElo(matchups, team_details, elo_ratings, kFactor_func, **kwargs)
        all_season_matchups_with_elo[season] = matchups_elo
        # update elo ratings for new season
        elo_ratings = {teamID: eloYearToYearCarryOver(elo_ratings[teamID]) for teamID, rating in elo_ratings.items()}

    return all_season_matchups_with_elo



if __name__ == '__main__':
    team_details = read_csv("resources/teams_details.tsv", sep='\t')
    teamIDs = team_details['id']
    game_logs_per_season = {}
    for season in generateSeasons(2018, 2023):
        game_logs_per_season[season] = read_csv(f"resources/game-logs/season_{season}.tsv", sep='\t')

    matchups_with_elo = enrichLogsWithElo(teamIDs, team_details, game_logs_per_season, basic_elo_rating=1500, kFactor_func=kFactor)

    for season, matchups_elo in matchups_with_elo.items():
        matchups_elo.to_csv(f"resources/elo-ratings/season_{season}.tsv", sep="\t", index=False)

