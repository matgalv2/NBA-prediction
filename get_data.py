from nba_api.stats.endpoints import teamgamelog, boxscoreadvancedv2
from nba_api.stats.static.teams import get_teams
from pandas import DataFrame


def getTeamsDetails() -> DataFrame:
    teams_details = get_teams()
    teams_details_dataframe = DataFrame(teams_details)
    return teams_details_dataframe


def getTeamStatsPerGame():

    box_score = boxscoreadvancedv2.BoxScoreAdvancedV2(game_id="0020001008")
    box_score_teams = box_score.get_normalized_dict()["TeamStats"]

    print(box_score_teams)
    print(box_score_teams[0]["OFF_RATING"], box_score_teams[0]["DEF_RATING"], box_score_teams[0]["TEAM_ID"])
    print(box_score_teams[1]["OFF_RATING"], box_score_teams[1]["DEF_RATING"], box_score_teams[1]["TEAM_ID"])


def generateSeasons(start, end):
    for year in range(start, end):
        yield f"{year}-{str(year + 1)[2:]}"

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
        'DEF_RATING': [box_score_teams[0]["DEF_RATING"], box_score_teams[1]["DEF_RATING"]]
    }

    return DataFrame(data=advanced_details)

