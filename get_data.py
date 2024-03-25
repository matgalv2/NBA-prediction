from nba_api.stats.endpoints import teamgamelog, boxscoreadvancedv2
from nba_api.stats.static.teams import get_teams
from pandas import DataFrame


def getTeamsDetails() -> DataFrame:
    teams_details = get_teams()
    teams_details_dataframe = DataFrame(teams_details)
    return teams_details_dataframe


def getTeamGameLogs(team_id, season) -> DataFrame:
    team_game_log = teamgamelog.TeamGameLog(team_id=f"{team_id}", season=season)
    team_game_log_dataframe = team_game_log.get_data_frames()[0]
    return team_game_log_dataframe


def getBoxScoreAdvanced(game_id) -> DataFrame:
    box_score = boxscoreadvancedv2.BoxScoreAdvancedV2(game_id=game_id)
    box_score_teams = box_score.get_normalized_dict()["TeamStats"]

    advanced_details = {
        'Game_ID': [box_score_teams[0]["GAME_ID"], box_score_teams[1]["GAME_ID"]],
        'Team_ID': [box_score_teams[0]["TEAM_ID"], box_score_teams[1]["TEAM_ID"]],
        'OFF_RATING': [box_score_teams[0]["OFF_RATING"], box_score_teams[1]["OFF_RATING"]],
        'DEF_RATING': [box_score_teams[0]["DEF_RATING"], box_score_teams[1]["DEF_RATING"]],
        'NET_RATING': [box_score_teams[0]["NET_RATING"], box_score_teams[1]["NET_RATING"]],
        'AST_PCT': [box_score_teams[0]["AST_PCT"], box_score_teams[1]["AST_PCT"]],
        'AST_TOV': [box_score_teams[0]["AST_TOV"], box_score_teams[1]["AST_TOV"]],
        'AST_RATIO': [box_score_teams[0]["AST_RATIO"], box_score_teams[1]["AST_RATIO"]],
        'OREB_PCT': [box_score_teams[0]["OREB_PCT"], box_score_teams[1]["OREB_PCT"]],
        'DREB_PCT': [box_score_teams[0]["DREB_PCT"], box_score_teams[1]["DREB_PCT"]],
        'REB_PCT': [box_score_teams[0]["REB_PCT"], box_score_teams[1]["REB_PCT"]],
        'TM_TOV_PCT': [box_score_teams[0]["TM_TOV_PCT"], box_score_teams[1]["TM_TOV_PCT"]],
        'EFG_PCT': [box_score_teams[0]["EFG_PCT"], box_score_teams[1]["EFG_PCT"]],
        'TS_PCT': [box_score_teams[0]["TS_PCT"], box_score_teams[1]["TS_PCT"]],
        'PACE': [box_score_teams[0]["PACE"], box_score_teams[1]["PACE"]],
        'PIE': [box_score_teams[0]["PIE"], box_score_teams[1]["PIE"]],
    }

    return DataFrame(data=advanced_details)
