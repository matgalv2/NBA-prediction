import pandas
from pandas import DataFrame


def showTeamsByGameID(gameID: str, game_logs: DataFrame, per_game_statistics: DataFrame):
    print("---------------------------------------")
    columns_logs = ["Game_ID", "Team_ID", "GAME_DATE", "MATCHUP"]
    print(game_logs[game_logs["Game_ID"] == gameID][columns_logs], '\n')
    columns_statistics = ["GAME_ID", "TEAM_ID", "TEAM_ABBREVIATION", "TEAM_CITY","TEAM_NAME", "PTS"]
    print(per_game_statistics[per_game_statistics["GAME_ID"] == gameID][columns_statistics])


if __name__ == "__main__":
    per_game_statistics = pandas.read_csv("resources/per-game-statistics/season_2023-24.tsv", sep="\t").astype({"GAME_ID": "str"})
    game_logs = pandas.read_csv("resources/game-logs/season_2023-24.tsv", sep="\t").astype({"Game_ID": "str"})

    entry = ""
    while entry != "q":
        try:
            entry = input("\nEnter game id:\n")
            showTeamsByGameID(entry, game_logs, per_game_statistics)
        except Exception as error:
            print(error)
            continue