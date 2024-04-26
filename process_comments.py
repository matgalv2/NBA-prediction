import re

import pandas
from pandas import DataFrame

whole_comment_pattern = re.compile('<div dir="auto" style="text-align: start;">(.+?)<\/div>(?:.|\n)+?<\/div>(?:.|\n)+?<\/span>(?:.|\n)+?<\/div>')
extracting_emotes_pattern = re.compile('(?:<span(?:.|\n)+?alt=")|("(?:.|\n)+?<\/span>)+?')
remove_tags_pattern = re.compile('(<(?:div|span|a|img)(?:.|\s)*?>)|(</(?:div|span|a|img)>)')
remove_tab_newline_pattern = re.compile('[\n\t]')

xpath_comments_selector = "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div/div[1]/div[4]"

def processComment(html: str):
    comments_html = re.findall(whole_comment_pattern, html)
    comments_with_emotes = []

    for comment in comments_html:
        processed: str = comment
        emote_pattern = re.compile('(?:<img(?:.|\s)*?alt=(\".*?\")(?:.|\s)*?>)')
        if "alt=" in processed:
            emotes = [emote.replace('\"', '') for emote in
                    re.findall(emote_pattern, comment)]
            remove_span_pattern = re.compile('(?:<img(?:.|\s)+?alt=(?:\".*?\")(?:.|\s)*?>)')
            for i, element in enumerate(re.finditer(remove_span_pattern, comment)):
                processed = re.sub(re.escape(element.group()), emotes[i], processed)

        comments_with_emotes.append(processed)

    removed_tags_comments = [re.sub(remove_tags_pattern, '', comment_html) for comment_html in comments_with_emotes]
    removed_tabs_newlines_comments = [re.sub(remove_tab_newline_pattern, '', comment_html) for comment_html in removed_tags_comments]
    return removed_tabs_newlines_comments


if __name__ == "__main__":
    df = pandas.read_csv("resources/game-logs/season_2023-24.tsv", sep="\t")
    entry = ""
    while entry != "0":
        try:
            entry = input("\nType game id:\n")
            html_file = ""
            with open('resources/comment.html', 'r', encoding='utf-8') as file:
                for line in file:
                    html_file += line

            processed_comments = [*filter(lambda comment: not comment.isspace(), processComment(html_file))]
            print(len(processed_comments), processed_comments)

            comments_dict = {
                "TEAM_ABBREVIATION": pandas.Series(data=["" for _ in range(len(processed_comments))]),
                "COMMENT": processed_comments
            }
            df = DataFrame(data=comments_dict)
            df.to_csv(f"resources/comments/{entry}.tsv", index=False, sep="\t")

        except Exception as error:
            print(error)
            continue