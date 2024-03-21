import string
from typing import List, Dict
from gram_out_json import get_cleaned_token_list, get_scrs_tok


def get_error_count(
        checker_data: Dict,
):
    metric_data = {
        "main": {}
    }
    ctl = get_cleaned_token_list()
    for og_sent, inner_dict in checker_data.items():
        if inner_dict["edited"] == True:
            inner_data = get_scrs_tok(inner_dict, ctl)
            metric_data["main"][og_sent] = inner_data
        else:
            metric_data["main"][og_sent] = {"edited": False, "corrected_sentence": inner_dict["fin_sentence"]}

    error_count = 0
    for og in metric_data["main"]:
        v = metric_data["main"][og]
        if v["edited"] == True:
            error_count += len(v["action_tag"])

    return error_count


def get_error_rate_sen(
        checker_data: Dict,
):
    og_list = list(checker_data.keys())
    error_count = get_error_count(checker_data=checker_data)
    sentence_count = len(og_list)

    return error_count / sentence_count


def get_error_rate_word(
        checker_data: Dict,
):
    og_list = list(checker_data.keys())
    error_count = get_error_count(checker_data=checker_data)

    word_count = 0
    for sen in og_list:
        # remove punctuations
        new_sen = sen.translate(str.maketrans('', '', string.punctuation))
        word_count += len(new_sen.split(" "))

    return error_count / word_count