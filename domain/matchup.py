from pandas import DataFrame


def getHomeTeamIDByMatchUp(match_up: str, team_details: DataFrame) -> int:

    team1_abbreviation, determinant, team2_abbreviation = match_up.split()

    if determinant == "vs.":
        home_team_abbreviation = team1_abbreviation
    else:
        home_team_abbreviation = team2_abbreviation

    return team_details.loc[team_details["abbreviation"] == home_team_abbreviation, "id"].values[0]

