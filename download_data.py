import time

from typing import List
from pandas import concat

from const import game_log_columns, advanced_game_details_columns
from get_data import *


def tryUntilSuccess(func, *args):
    succeeded = False
    result = None
    errors = 0
    while not succeeded:
        if errors >= 2:
            print("Sleeping 300s")
            time.sleep(300)
            errors = 0
        try:
            result = func(*args)
            if result is None:
                succeeded = True
        except Exception as err:
            errors += 1
            print(err)
        finally:
            if result is not None:
                succeeded = True
    return result


def enrichGameLogsWithAdvancedDetails(game_logs: DataFrame) -> DataFrame:
    game_ids = set(game_logs["Game_ID"])
    advanced_game_details = DataFrame(columns=advanced_game_details_columns)
    for i, game_id in enumerate(game_ids):
        time.sleep(1)

        box_score_advanced = tryUntilSuccess(getBoxScoreAdvanced, game_id)
        advanced_game_details = concat([box_score_advanced, advanced_game_details], ignore_index=True)
        print(f"{round((i + 1) * 100 / len(game_ids), 3)}%")
    game_logs = game_logs.merge(advanced_game_details, how='left', on=['Game_ID', 'Team_ID'])

    return game_logs


def getAllTeamsGameLog(team_ids: List[str], season: str) -> DataFrame:
    games = DataFrame(columns=game_log_columns)
    teams_no = len(team_ids)

    for i, team_id in enumerate(team_ids):
        gameLogs = tryUntilSuccess(getTeamGameLogs, team_id, season)
        games = concat([games, gameLogs], ignore_index=True)

        print(f"{round((i + 1) * 100/teams_no, 3)}% ---- season {season}")

    games = enrichGameLogsWithAdvancedDetails(games)
    return games

