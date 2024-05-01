import pandas as pd

from utils import generateSeasons

if __name__ == '__main__':
    # for season in generateSeasons(2018, 2023):
    for season in generateSeasons(2018, 2018):

        per_game_statistics = pd.read_csv(f'resources/per-game-statistics/season_{season}.tsv', sep='\t')
        elo_ratings = pd.read_csv(f'resources/elo-ratings/season_{season}.tsv', sep='\t')

        elo_ratings_teams_x = elo_ratings[["Game_ID", "Team_ID_x", "ELO_x"]]
        elo_ratings_teams_x.rename(columns={"Game_ID": "GAME_ID", "Team_ID_x": "TEAM_ID", "ELO_x": "ELO"}, inplace=True)

        elo_ratings_teams_y = elo_ratings[["Game_ID", "Team_ID_y", "ELO_y"]]
        elo_ratings_teams_y.rename(columns={"Game_ID": "GAME_ID", "Team_ID_y": "TEAM_ID", "ELO_y": "ELO"}, inplace=True)

        elo_ratings_simplified = pd.concat([elo_ratings_teams_x, elo_ratings_teams_y], ignore_index=True)

        per_game_statistics_with_elo = per_game_statistics.merge(elo_ratings_simplified, on=['GAME_ID', 'TEAM_ID'])

        # print(per_game_statistics_with_elo)

        home_away = per_game_statistics_with_elo.merge(per_game_statistics, on=['GAME_ID'])


        # place for adding sentiment analysis

        #

        game_logs = pd.read_csv(f"resources/game-logs/season_{season}.tsv", sep='\t')[["Game_ID", "MATCHUP", "Team_ID", "WL"]]

        home_matchups = game_logs[game_logs["MATCHUP"].str.contains(".vs")]
        away_matchups = game_logs[game_logs["MATCHUP"].str.contains("@")]

        games = home_matchups.merge(away_matchups, how="inner", on="Game_ID", suffixes=("_home", "_away"))
        games["WL_home"] = games["WL_home"].map(lambda result: 1 if result == "W" else 0)
        games.rename(columns={"Game_ID": "GAME_ID", "Team_ID_home": "TEAM_ID_home", "Team_ID_away": "TEAM_ID_away", "WL_home": "OUTCOME", "MATCHUP_home": "MATCHUP"}, inplace=True)

        games = games.drop(columns=["MATCHUP_away", "WL_away"])


        matchups = per_game_statistics_with_elo.merge(per_game_statistics_with_elo, on=['GAME_ID'], suffixes=("_home", "_away"))


        matchups = matchups[matchups["TEAM_ID_home"] != matchups["TEAM_ID_away"]]
        print(matchups)
        matchups = matchups.merge(games, how="inner", on=["GAME_ID", "TEAM_ID_home", "TEAM_ID_away"])
        print(matchups)

