import warnings

from pandas import read_csv

from download_data import getGameLogs, getStatistics
from get_data import getTeamGameIds
from utils import generateSeasons


if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    teams = read_csv("resources/teams_details.tsv", sep="\t")
    team_ids = teams["id"]
    seasons = generateSeasons(2018, 2023)

    for season in seasons:
        logs = getGameLogs(team_ids, season)
        game_ids = getTeamGameIds(logs)
        perGameStatistics = getStatistics(game_ids)
        logs.to_csv(f"resources/game-logs/season_{season}.tsv", sep="\t", index=False)
        perGameStatistics.to_csv(f"resources/per-game-statistics/season_{season}.tsv", sep="\t", index=False)
