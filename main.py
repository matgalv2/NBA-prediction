import warnings

from pandas import read_csv

from download_data import getGameLogs, getStatistics
from get_data import getTeamGameIds
from utils import generateSeasons


if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    teams = read_csv("resources/teams_details.tsv", sep="\t")
    team_ids = teams["id"]
    seasons = generateSeasons(2018, 2022)

    for season in seasons:
        logs = getGameLogs(team_ids, season)
        game_ids = getTeamGameIds(logs)
        perGameStatistics = getStatistics(game_ids)
        logs.to_csv(f"resources/game-logs-test/season_{season}.tsv", sep="\t", index=False)
        perGameStatistics.to_csv(f"resources/per-game-statistics/season_{season}.tsv", sep="\t", index=False)


# TODO:
#   0. Download new data
#   1. ELO rating
#   2. Check relevance for all parameters (ANOVA or logistic regression)
#   3. Feature selection
#   4. Comments

