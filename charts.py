import pandas as pd

from utils import generateSeasons

import matplotlib.pyplot as plt
import numpy as np

def homeAdvantageChart():
    percentage = {}
    for season in generateSeasons(2018, 2023):
        season_percentage = {}
        game_logs = pd.read_csv(f'resources/game-logs/season_{season}.tsv', sep='\t')
        length = len(game_logs[game_logs["MATCHUP"].str.contains('vs.')][game_logs["WL"] == "W"].values)
        length2 = len(game_logs[game_logs["MATCHUP"].str.contains('@')][game_logs["WL"] == "W"].values)
        # print(season, length/1230.0, length2/1230.0)
        season_percentage["wins_home"] = length / (len(game_logs.values) / 2)
        season_percentage["wins_away"] = length2 / (len(game_logs.values) / 2)
        percentage[season] = season_percentage

    # Extract item values for each group
    wins_home_values = [percentage[season]["wins_home"] for season in percentage]
    wins_away_values = [percentage[season]["wins_away"] for season in percentage]

    # Number of groups
    num_groups = len(percentage)

    # Group labels
    group_labels = list(percentage.keys())

    # Width of bars
    bar_width = 0.35

    # Index for the x-axis
    index = np.arange(num_groups)

    # Create subplots
    fig, ax = plt.subplots()

    ax.axhline(y=sum(wins_home_values) / len(wins_home_values), color='black', linestyle='dashed',
               label=f'Średnia zwycięstw w domu ({round(sum(wins_home_values) / len(wins_home_values) * 100, 2)}%)')
    ax.axhline(y=sum(wins_away_values) / len(wins_away_values), color='black', linestyle='dotted',
               label=f'Średnia zwycięstw na wyjeździe ({round(sum(wins_away_values) / len(wins_away_values) * 100, 2)}%)')
    ax.axhline(y=0.5, color='red', linestyle='-.')
    # Plot item1
    bar1 = ax.bar(index, wins_home_values, bar_width, label='Zwycięstwa w domu w danym sezonie', color='forestgreen')

    # Plot item2
    bar2 = ax.bar(index + bar_width, wins_away_values, bar_width, label='Zwycięstwa na wyjeździe w danym sezonie',
                  color='royalblue')
    ax.set_ylim([0.0, 1.0])
    # Add labels, title, and legend
    ax.set_xlabel('Sezon')
    ax.set_ylabel('Procent wygranych')
    ax.set_title('Procent wygranych spotkań w zależności od sezonu\n i formy spotkania (w domu lub na wyjeździe)')
    ax.set_xticks(index + bar_width / 2)
    ax.set_yticks(np.arange(0., 1.05, 0.1))
    ax.set_xticklabels(group_labels)
    ax.legend(loc='upper right')

    # Show plot
    # plt.show()
    plt.savefig("resources/charts/home-advantage.png", dpi=300)