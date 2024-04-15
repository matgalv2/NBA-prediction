import time

from pandas import concat

from const import full_box_score_attributes, game_log_attributes
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


def getStatistics(all_game_ids: List[str]) -> DataFrame:
    game_ids = set(all_game_ids)
    attributes = full_box_score_attributes
    game_logs = DataFrame(columns=attributes)

    for i, game_id in enumerate(game_ids):
        box_score_traditional = tryUntilSuccess(getBoxScoreTraditional, game_id)
        box_score_advanced = tryUntilSuccess(getBoxScoreAdvanced, game_id)
        full_game_log = box_score_traditional.merge(box_score_advanced, how='left', on=['GAME_ID', 'TEAM_ID'])
        game_logs = concat([full_game_log, game_logs], ignore_index=True)
        print(f"{round((i + 1) * 100 / len(game_ids), 3)}%")

    return game_logs


def getGameLogs(team_ids: List[str], season: str) -> DataFrame:
    games = DataFrame(columns=game_log_attributes)
    teams_no = len(team_ids)

    for i, team_id in enumerate(team_ids):
        game_logs = tryUntilSuccess(getTeamGameLogs, team_id, season)
        games = concat([games, game_logs])
        print(f"{round((i + 1) * 100/teams_no, 3)}% ---- season {season}")

    return games

