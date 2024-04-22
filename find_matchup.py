import pandas
from pandas import DataFrame


def findGameIdByTeamNamesAndPoints(team1, team2, dataset: DataFrame) -> DataFrame:
    matchups = [
        f"{team1} vs. {team2}",
        f"{team2} vs. {team1}",
        f"{team1} @ {team2}",
        f"{team2} @ {team1}"
    ]
    columns = ["Team_ID", "Game_ID", "GAME_DATE", "MATCHUP", "PTS"]
    return dataset[dataset["MATCHUP"].isin(matchups)].sort_values(by="Game_ID")[columns]




if __name__ == "__main__":
    df = pandas.read_csv("resources/game-logs/season_2023-24.tsv", sep="\t")
    entry = ""
    while entry != "0":
        try:
            entry = input("\nEnter teams abbreviations':\n")
            print(findGameIdByTeamNamesAndPoints(*entry.upper().split(" "), df))
        except TypeError as typeError:
            continue