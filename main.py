import warnings

from pandas import read_csv

from download_data import getAllTeamsGameLog
from utils import generateSeasons


if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    teams = read_csv("resources/teams_details.tsv", sep="\t")
    team_ids = teams["id"]


    for season in generateSeasons(2018, 2023):
        logs = getAllTeamsGameLog(team_ids, season)
        logs.to_csv(f"resources/game-logs/season_{season}.tsv", sep="\t", index=False)


# TODO:
#   1. ELO rating
#   2. Check relevance for all parameters (ANOVA or logistic regression)
#   3. Feature selection
#   4. Comments

