import string
from typing import Dict, Literal, get_args

from gram_out_json import get_cleaned_token_list, get_scrs_tok, get_tag_grammar, get_phase_2_inner_data


# ec = error count, psc = per sentence count, pwc = per word count
_STYPES = Literal["ec", "psc", "pwc"]
_ETYPES = Literal["new", "old"]


def get_error_count(
    checker_data: Dict,
    error_count_type: _ETYPES = "new",
    token_path: str = "../gector/data/token_labels.txt"
):
    error_count = 0
    ctl = get_cleaned_token_list(token_path)

    # 중복 에러 없앤 버전
    if error_count_type == "new":
        og_list = list(checker_data.keys())
        # corr_list = [v.get('fin_sentence') for _, v in checker_data.items()]
        tag_grammar = get_tag_grammar(ctl)

        for og_sent, inner_dict in checker_data.items():
            gector_dict = get_scrs_tok(inner_dict, ctl)
            sid = og_list.index(og_sent)
            sent = og_sent
            corr_sent = inner_dict["fin_sentence"]
            edited = inner_dict["edited"]
            ref_word_list = gector_dict["og_word"]
            tag_list = gector_dict["full_tag"]
            if edited == True:
                inner = get_phase_2_inner_data(sid=sid, sent=sent, corr_sent=corr_sent, edited=edited, ref_word_list=ref_word_list, 
                                            tag_list=tag_list, tag_grammar=tag_grammar)
                error_count += len(inner["ref_word"])

    # 기존 버전
    elif error_count_type == "old":
        metric_data = {
            "main": {}
        }
        for og_sent, inner_dict in checker_data.items():
            if inner_dict["edited"] == True:
                inner_data = get_scrs_tok(inner_dict, ctl)
                metric_data["main"][og_sent] = inner_data
            else:
                metric_data["main"][og_sent] = {"edited": False, "corrected_sentence": inner_dict["fin_sentence"]}

        for og in metric_data["main"]:
            v = metric_data["main"][og]
            if v["edited"] == True:
                error_count += len(v["action_tag"])

    return error_count


def get_error_rate_sen(
    checker_data: Dict,
    error_count_type: _ETYPES = "new",
    token_path: str = "../gector/data/token_labels.txt"
):
    og_list = list(checker_data.keys())
    error_count = get_error_count(checker_data=checker_data, error_count_type=error_count_type, token_path=token_path)
    sentence_count = len(og_list)

    return round(error_count / sentence_count, 2)


def get_error_rate_word(
    checker_data: Dict,
    error_count_type: _ETYPES = "new",
    token_path: str = "../gector/data/token_labels.txt"
):
    og_list = list(checker_data.keys())
    error_count = get_error_count(checker_data=checker_data, error_count_type=error_count_type, token_path=token_path)

    word_count = 0
    for sen in og_list:
        # remove punctuations
        new_sen = sen.translate(str.maketrans("", "", string.punctuation))
        word_count += len(new_sen.split(" "))
        result = (1 - (error_count / word_count)) * 100

    return round(result, 2)


def get_score(
        checker_data: Dict,
        score_type: _STYPES = "pwc",
        error_count_type: _ETYPES = "new",
        token_path: str = "../gector/data/token_labels.txt"
):
    # raise error if the score type is not in the _TYPE list
    soptions = get_args(_STYPES)
    eoptions = get_args(_ETYPES)
    assert score_type in soptions, f"'{score_type}' is not in {soptions}"
    assert error_count_type in eoptions, f"'{error_count_type}' is not in {eoptions}"

    if score_type == "ec":
        return get_error_count(checker_data=checker_data, error_count_type=error_count_type, token_path=token_path)
    elif score_type == "psc":
        return get_error_rate_sen(checker_data=checker_data, error_count_type=error_count_type, token_path=token_path)
    elif score_type == "pwc":
        return get_error_rate_word(checker_data=checker_data, error_count_type=error_count_type, token_path=token_path)

if __name__ == "__main__":
    token_path = "../gector/data/token_labels.txt"
    get_cleaned_token_list(token_path)