import pandas as pd
from pandas import DataFrame

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


def findPreviousNGameIDs(gameID: int, df: DataFrame):
    df = df.copy()
    team_details = pd.read_csv("resources/teams_details.tsv", sep="\t")

    home, away = df[df["Game_ID"] == gameID][df["MATCHUP"].str.contains("vs.")]["MATCHUP"].str.split(" vs. ").values[0]

    home_team_id = team_details.loc[team_details["abbreviation"] == home, "id"].values[0]
    away_team_id = team_details.loc[team_details["abbreviation"] == away, "id"].values[0]

    df['GAME_DATE'] = df['GAME_DATE'].map(lambda x: date.NBADate.create(x).value)

    teamIDs = {
        home_team_id: "",
        away_team_id: "",
    }

    for teamId in teamIDs:
        games = df[df["Team_ID"] == teamId].sort_values(by="GAME_DATE", ascending=True)
        games.reset_index(inplace=True)
        games.drop(columns=["index"], inplace=True)

        gameID_index = games[games["Game_ID"] == gameID].index.values[0]

        if gameID_index < 3:
            teamIDs[teamId] = []
        else:
            teamIDs[teamId] = games.iloc[gameID_index - 3 : gameID_index]["Game_ID"].values.tolist()
    return teamIDs






# dataset = pd.read_csv(f"resources/game-logs/season_2023-24.tsv", sep='\t')
#
# filenames: List[str] = os.listdir("resources/comments")
# gameIDs = [int(filename.removesuffix(".tsv")) for filename in filenames]
#
#
# nextGames = {
#     gameID : findNextGameID(gameID, dataset) for gameID in gameIDs
# }
# print(nextGames)

# # print(findNextGameIDs(22300069, dataset))
# print(findPreviousNGameIDs(22300139, dataset))
