from typing import List, Type

from nba_api.stats.endpoints import teamgamelog, BoxScoreAdvancedV2,BoxScoreTraditionalV2
from nba_api.stats.static.teams import get_teams
from pandas import DataFrame

from const import traditional_box_score_attributes, advanced_box_score_attributes

def getTeamsDetails() -> DataFrame:
    teams_details = get_teams()
    teams_details_dataframe = DataFrame(teams_details)
    return teams_details_dataframe


def getTeamGameLogs(team_id, season) -> List[str]:
    team_game_log = teamgamelog.TeamGameLog(team_id=f"{team_id}", season=season)
    game_logs = team_game_log.get_data_frames()[0]
    return game_logs

def getTeamGameIds(game_logs: DataFrame) -> List[str]:
    return game_logs["Game_ID"].tolist()


def __getBoxScore(game_id: str,
                  BoxScoreEndpoint: Type[BoxScoreAdvancedV2] | Type[BoxScoreTraditionalV2],
                  box_score_attributes: List[str]
                  ) -> DataFrame:

    def mapMinutes(minutes: str):
        return minutes.split(".")[0]

    box_score = BoxScoreEndpoint(game_id=game_id)
    box_score_teams = box_score.get_normalized_dict()["TeamStats"]

    details = {
        attribute : [
            box_score_teams[0][attribute],
            box_score_teams[1][attribute]
        ] if attribute != "MIN" else [
            mapMinutes(box_score_teams[0][attribute]),
            mapMinutes(box_score_teams[1][attribute])
        ] for attribute in box_score_attributes
    }
    return DataFrame(data=details)


def getBoxScoreAdvanced(game_id: str) -> DataFrame:
    endpoint = BoxScoreAdvancedV2
    return __getBoxScore(game_id, endpoint, advanced_box_score_attributes)


def getBoxScoreTraditional(game_id: str) -> DataFrame:
    endpoint = BoxScoreTraditionalV2
    return __getBoxScore(game_id, endpoint, traditional_box_score_attributes)
