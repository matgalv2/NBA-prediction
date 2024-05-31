import nltk
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer

import emoji
from sklearn.preprocessing import MinMaxScaler
from transformers import pipeline

# import tensorflow as tf
# tf.keras.mixed_precision.set_global_policy("mixed_float16")


from typing import List

import pandas as pd
import os

from utils import *

nltk.download('vader_lexicon')# Compute sentiment labels
# tweet = 'Lakers were great in last match'
tweet1 = "Hey Grizz you might wanna win tomorrow against the Overrated Loser Warriors this is a MUST win cause it’s gonna come down to the last Play In Tournament and who’s gonna get that last spot this is an important win GET THAT WIN GUYS I know we don’t have Ja Goat 🐐🤴🏾 but I’m gonna spread positivity and positive vibes that the boys WILL and CAN get this win they’ve got this Taylor get them ready I am ready for the boys to pounce 😈😈😈😈😈😈the rest of the games and get revenge for Ja Goat 🐐🤴🏾 💙😈😈😈😈😈😈😈😈😈😈😈😈😈😈😈💪🏾💪🏾🦵🏾🦵🏾🏀🏆💍💯💯💯💯💯💯💯💯💯💯💯💯💯 Memphis Grizzlies"
# tweet2 = "love you 💖💖💖💖"
# tweet3 = "love you"
# tweet4 = "fuck you"
# tweet5 = "FUCK YOU !!!! 🖕🖕🖕"
# tweet6 = "fuck you ..."
# tweet7 = "fuck you 🖕"
# tweet8 = "lakes in ohio are very big and deep"



# bertweet = pipeline('sentiment-analysis', model='siebert/sentiment-roberta-large-english')
# bertweet = pipeline('sentiment-analysis', model='distilbert/distilbert-base-uncased-finetuned-sst-2-english')
# bertweet = pipeline('sentiment-analysis', model='finiteautomata/bertweet-base-sentiment-analysis')
vader = SentimentIntensityAnalyzer()
# tweets = [tweet1, tweet2, tweet3, tweet4, tweet5, tweet6, tweet7, tweet8]
tweets = [tweet1]

scaler = MinMaxScaler(feature_range=(0,1))

team_details = pd.read_csv("resources/teams_details.tsv", sep="\t")


filenames: List[str] = os.listdir("resources/comments")
print(len(filenames))
gameIDs = [int(filename.removesuffix(".tsv")) for filename in filenames]

# dataset = DataFrame(columns=["GAME_ID", "TEAM_ID", "VADER", "BERTWEET", "COMBINATION"])
game_logs = pd.read_csv("resources/game-logs/season_2023-24.tsv", sep="\t")

dataset = DataFrame(columns=["GAME_ID", "TEAM_ID", "SENTIMENT"])
for gameID in gameIDs:
    post = pd.read_csv(f"resources/comments/{gameID}.tsv", sep="\t")
    # team_abbreviations = set(post["TEAM_ABBREVIATION"].dropna().tolist()).difference({"SPAM"})
    team_abbreviations = game_logs[game_logs["Game_ID"] == gameID][game_logs["MATCHUP"].str.contains("vs.")]["MATCHUP"].str.split(" vs. ").values[0]
    for team_abbreviation in team_abbreviations:
        teamID = team_details.loc[team_details["abbreviation"] == team_abbreviation, "id"].values[0]
        comments = post[post["TEAM_ABBREVIATION"] == team_abbreviation]["COMMENT"].tolist()

        polarities = {
            "SENTIMENT" :[],
            # "VADER" :[],
            # "BERTWEET": [],
            # "COMBINATION": []
        }

        for comment in comments:
            vader_value = vader.polarity_scores(comment)["compound"]
            # huggingface = bertweet(comment)[0]
            # if huggingface["label"] == "POS":
            #     huggingface_value = huggingface["score"]
            # elif huggingface["label"] == "NEU":
            #     huggingface_value = 0
            # else:
            #     huggingface_value = -huggingface["score"]

            polarities["SENTIMENT"].append(vader_value)
            # polarities["VADER"].append(vader_value)
            # polarities["BERTWEET"].append(huggingface_value)
            # polarities["COMBINATION"].append((vader_value+huggingface_value)/2)

        data = {
            "GAME_ID": [gameID],
            "TEAM_ID": [teamID]
        }

        for key, value in polarities.items():
            data[key] = [sum(value)/len(value) if len(value) > 0 else 0]

        dataset = pd.concat([dataset, DataFrame(data)])

dataset["SENTIMENT"] = scaler.fit_transform(np.array(dataset["SENTIMENT"].tolist()).reshape(-1, 1))

dataset.to_csv("resources/sentiment-analysis/fans-sentiment.tsv", sep="\t", index=False)



# for tweet in tweets:
#     emojis = "".join([element["emoji"] for element in emoji.emoji_list(tweet)])
#
#     print("Tweet: ", tweet)
#     vader_value = vader.polarity_scores(tweet)["compound"]
#     huggingface = bertweet(tweet)[0]
#     if huggingface["label"] == "POS":
#         huggingface_value = huggingface["score"]
#     elif huggingface["label"] == "NEG":
#         huggingface_value = -huggingface["score"]
#     else:
#         huggingface_value = 0
#
#     print("huggingface: ", huggingface_value)
#     print("vader: ", vader_value)
#     print((huggingface_value + vader_value)/2)