game_log_attributes = [
    'Team_ID', 'Game_ID', 'GAME_DATE', 'MATCHUP',
    'WL', 'W', 'L', 'W_PCT', 'MIN', 'FGM', 'FGA',
    'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM',
    'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST',
    'STL', 'BLK', 'TOV', 'PF', 'PTS'
]

traditional_box_score_attributes = [
    'GAME_ID', 'TEAM_ID', 'TEAM_NAME', 'TEAM_ABBREVIATION',
    'TEAM_CITY', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M',
    'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB',
    'DREB', 'REB', 'AST', 'STL', 'BLK', 'TO', 'PF', 'PTS', 'PLUS_MINUS'
]

advanced_box_score_attributes = [
    'GAME_ID', 'TEAM_ID', 'OFF_RATING', 'DEF_RATING',
    'NET_RATING', 'AST_PCT', 'AST_TOV', 'AST_RATIO',
    'OREB_PCT', 'DREB_PCT', 'REB_PCT', 'TM_TOV_PCT',
    'EFG_PCT', 'TS_PCT', 'PACE', 'PIE'
]

full_box_score_attributes = traditional_box_score_attributes + advanced_box_score_attributes[2:]
