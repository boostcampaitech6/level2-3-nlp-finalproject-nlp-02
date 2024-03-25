import string
from typing import Dict, Literal, get_args
from .gram_out_json import get_cleaned_token_list, get_scrs_tok


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

    return round(error_count / sentence_count, 2)


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
        result = (1 - (error_count / word_count)) * 100

    return round(result, 2)

# ec = error count, psc = per sentence count, pwc = per word count
_TYPES = Literal["ec", "psc", "pwc"]


def get_score(
        checker_data: Dict,
        score_type: _TYPES = "pwc",
):
    # raise error if the score type is not in the _TYPE list
    options = get_args(_TYPES)
    assert score_type in options, f"'{score_type}' is not in {options}"

    if score_type == "ec":
        return get_error_count(checker_data=checker_data)
    elif score_type == "psc":
        return get_error_rate_sen(checker_data=checker_data)
    elif score_type == "pwc":
        return get_error_rate_word(checker_data=checker_data)