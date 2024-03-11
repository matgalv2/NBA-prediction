# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pandas
from nba_api.stats.endpoints.teamgamelog import TeamGameLog




def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    print(TeamGameLog(team_id="1610612737").team_game_log.get_data_frame().columns)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

