import math

import pandas
from pandas import DataFrame


def checkIntegrity(gameID: str, per_game_statistics: DataFrame):

    post = pandas.read_csv(f'resources/comments/{gameID}.tsv', sep='\t')
    labels = post["TEAM_ABBREVIATION"].tolist()
    teams = per_game_statistics[per_game_statistics["GAME_ID"] == gameID]["TEAM_ABBREVIATION"].tolist()
    for i, label in enumerate(labels):
        if not label in teams and (type(label) == str or not math.isnan(label)):
            print(f"Comment at {i} th position not recognized: {label}")

    if set(filter(lambda label: type(label) == str, labels)).issubset(set(teams)):
        print(f"{gameID} - OK!")


if __name__ == "__main__":
    per_game_statistics = pandas.read_csv("resources/per-game-statistics/season_2023-24.tsv", sep="\t").astype({"GAME_ID": "str"})

    entry = ""
    while entry != "q":
        try:
            entry = input("\nEnter game id:\n")
            checkIntegrity(entry, per_game_statistics)
        except Exception as error:
            print(error)
            continue