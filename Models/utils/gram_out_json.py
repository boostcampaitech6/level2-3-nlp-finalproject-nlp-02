import json
import re
import logging
logging.basicConfig(
    format = '%(asctime)s:%(levelname)s:%(message)s',
    datefmt = '%m/%d/%Y %I:%M:%S %p',
    level = logging.INFO
)

from collections import OrderedDict
from pprint import pprint
from copy import deepcopy
from typing import List, Dict


def load_token_list(
        token_path: str = "../gector/data/token_labels.txt"
    ):
    with open(token_path, "r", encoding="utf-8") as t:
        token_list = list(map(lambda x: x.strip(), t.readlines()))
    
    return token_list


def get_cleaned_token_list(
        token_path: str = "../gector/data/token_labels.txt"
    ):    
    token_list = load_token_list(token_path)

    fundamental_pattern = r'[$](KEEP|TRANSFORM_CASE|TRANSFORM_SPLIT_HYPHEN|MERGE_HYPHEN|MERGE_SPACE)'
    punct_pattern  = r'[$](REPLACE|APPEND)_[^\w\s]$'
    combined_pattern = r"%s|%s" % (fundamental_pattern, punct_pattern)
    remove_list = [item for item in token_list if re.match(combined_pattern, item)]
    final_token_list = [x for x in token_list if x not in remove_list]

    return final_token_list


def get_scrs_tok(
        inner_dict: Dict, 
        tok_list: List
    ):
    """Creates the inner dictionary of check file including original sentence, edited, og_word,
    action_tag, full_tag and corrected sentence

    Args:
        inner_dict (Dict): inner dictionary of check data file
        tok_list (List): output from get_cleaned_token_list

    Returns:
        Dict: inner data
    """
    inner_data = {
        "edited": True,
        "og_word": [],
        "action_tag": [],
        "full_tag": [],
        "corrected_sentence": ""
    }
    sent_list = inner_dict["sentence_list"]
    tag_list = inner_dict["tag_list"]
    for i in range(len(inner_dict["sentence_list"])):
        for j in range(len(tag_list[i])):
            if tag_list[i][j] in tok_list:
                inner_data["og_word"].append(sent_list[i][j])
                inner_data["action_tag"].append(tag_list[i][j].split("_")[0])
                inner_data["full_tag"].append(tag_list[i][j])
    inner_data["corrected_sentence"] = inner_dict["fin_sentence"]
    
    return inner_data


def get_tag_grammar(
        tok_list: List
    ):
    """Creates tag-grammar dictionary and indicates the category of the grammar correction

    Args:
        tok_list (List): output from get_cleaned_token_list

    Returns:
        Dict: provides the explanation of GEC
    """
    # trans = r'[$](TRANSFORM)_[\w]'
    # trans_list = [item for item in tag_list if re.match(trans, item)]

    tag_grammar_dict = {
        "$TRANSFORM_VERB_VB_VBZ": {
            "category": "주어-동사 수일치",
            "desc": "PLURAL TO SINGULAR VERB",
        },
        "$TRANSFORM_VERB_VB_VBN": {
            "category": "시제",
            "desc": "PRESENT TO PAST PARTICIPLE",
        },
        "$TRANSFORM_VERB_VB_VBD": {"category": "시제", "desc": "PRESENT TO PAST TENSE"},
        "$TRANSFORM_VERB_VB_VBG": {
            "category": "동사 형태",
            "desc": "PRESENT TO PRESENT PARTICIPLE",
        },
        "$TRANSFORM_VERB_VBZ_VB": {
            "category": "동사 형태",
            "desc": "SINGULAR TO PLURAL VERB",
        },
        "$TRANSFORM_VERB_VBZ_VBN": {
            "category": "동사 형태",
            "desc": "SINGULAR VERB TO PAST PARTICIPLE",
        },
        "$TRANSFORM_VERB_VBZ_VBD": {
            "category": "시제",
            "desc": "SINGULAR VERB TO PAST TENSE",
        },
        "$TRANSFORM_VERB_VBZ_VBG": {
            "category": "동사 형태",
            "desc": "SINGULAR VERB TO PRESENT PARTICIPLE",
        },
        "$TRANSFORM_VERB_VBN_VB": {
            "category": "시제",
            "desc": "PAST PARTICIPLE TO PRESENT TENSE",
        },
        "$TRANSFORM_VERB_VBN_VBZ": {
            "category": "동사 형태",
            "desc": "PAST PARTICIPLE TO SINGULAR VERB",
        },
        "$TRANSFORM_VERB_VBN_VBD": {
            "category": "시제",
            "desc": "PAST PARTICIPLE TO PAST TENSE",
        },
        "$TRANSFORM_VERB_VBN_VBG": {
            "category": "동사 형태",
            "desc": "PAST PARTICIPLE TO PRESENT PARTICIPLE",
        },
        "$TRANSFORM_VERB_VBD_VB": {
            "category": "시제",
            "desc": "PAST TENSE TO PRESENT TENSE",
        },
        "$TRANSFORM_VERB_VBD_VBZ": {
            "category": "동사 형태",
            "desc": "PAST TENSE TO SINGULAR VERB",
        },
        "$TRANSFORM_VERB_VBD_VBN": {
            "category": "동사 형태",
            "desc": "PAST TENSE TO PAST PARTICIPLE",
        },
        "$TRANSFORM_VERB_VBD_VBG": {
            "category": "동사 형태",
            "desc": "PAST TENSE TO PRESENT PARTICIPLE",
        },
        "$TRANSFORM_VERB_VBG_VB": {
            "category": "시제",
            "desc": "PRESENT PARTICIPLE TO PRESENT TENSE",
        },
        "$TRANSFORM_VERB_VBG_VBZ": {
            "category": "시제",
            "desc": "PRESENT PARTICIPLE TO SINGULAR VERB",
        },
        "$TRANSFORM_VERB_VBG_VBN": {
            "category": "동사 형태",
            "desc": "PRESENT PARTICIPLE TO PAST PARTICIPLE",
        },
        "$TRANSFORM_VERB_VBG_VBD": {
            "category": "시제",
            "desc": "PRESENT PARTICIPLE TO PAST TENSE",
        },
        "$TRANSFORM_AGREEMENT_SINGULAR": {
            "category": "명사 수일치",
            "desc": "SINGULAR TO PLURAL NOUN",
        },
        "$TRANSFORM_AGREEMENT_PLURAL": {
            "category": "명사 수일치",
            "desc": "PLURAL TO SINGULAR NOUN",
        },
    }

    # 33 common preposition list
    preps = [
        "across", "to", "on", "with", "in", "of", "at", "inside", "during", "from", "as",
        "through", "for", "along", "about", "into", "towards", "down", "behind", "round", "before", "by",
        "against", "between", "onto", "off", "beside", "around", "over", "among", "above", "after", "beneath",
    ]
    preps_tag_list = [tag for tag in tok_list if tag.split("_")[-1] in preps]

    for p in preps_tag_list:
        tag_grammar_dict[p] = {
            'category': '전치사',
            'desc': 'PREPOSITION'
        }

    return tag_grammar_dict


def get_phase_1_data(
        score: float, 
        checker_data: Dict
    ):
    og_list = list(checker_data.keys())
    corrected_list = [str(checker_data[og]["fin_sentence"]) for og in checker_data.keys()]

    inner = {
        "score": score,
        "original_passage": ' '.join(og_list),
        "corrected_passage": ' '.join(corrected_list)
    }
    phase_1 = {"phase_1": inner}
    
    return phase_1


def get_ref_word_in_sentence(
        ref_word_list: List,
        sen_list: List
    ):
    """
    인식한 tag가 og/corr sentence 어디에 위치해있는지 확인

    Args:
        ref_word_list (List): GEC 과정에서 잡은 단어
        sen_list (List): 발화 문장 (ex. 원래 발화 문장, GEC 후 문장)

    Returns:
        OrderedDict: ref_word에 나온 단어가 sen_list 어디서 등장하는지 인덱스를 정리한 딕셔너리 (단어 : [인덱스])
    """
    idx_dict = OrderedDict()
    for i in range(len(sen_list)):
        if sen_list[i] in ref_word_list:
            if sen_list[i] in idx_dict:
                idx_dict[sen_list[i]].append(i)
            else:
                idx_dict[sen_list[i]] = [i]

    return idx_dict


def get_by_peek_nearest_word(
        og_list: List, 
        corr_list: List, 
        word: str, 
        idx_dict_og: Dict, 
        idx_dict_corr: Dict
    ):
    """
    delete/replace/verb/noun transform을 하면 GEC된 문장에서 해당 단어가 사라지기 때문에 같은 단어가 여러개일 때 정확한 index를 얻을 수 없음
    그렇기 때문에 전이나 후의 단어를 확인해보기로 함
    또, GEC된 문장에 해당 단어가 존재하면 안됨

    Args:
        og_list (List): 원래 발화된 문장을 단어마다 tokenize한 리스트
        corr_list (List): GEC된 문장을 단어마다 tokenize한 리스트
        word (str): ref_word에 있는 단어
        idx_dict_og (OrderedDict): ref_word에 나온 단어가 og_list 어디서 등장하는지 인덱스를 정리한 딕셔너리 (단어 : [인덱스])
        idx_dict_corr (OrderedDict): ref_word에 나온 단어가 corr_list 어디서 등장하는지 인덱스를 정리한 딕셔너리 (단어 : [인덱스])

    Returns:
        List: og_list의 어디서 등장하는지 idx가 들어있는 리스트
    """
    
    o_dict = deepcopy(idx_dict_og)
    c_dict = deepcopy(idx_dict_corr)

    result = []
    while True:
        if not o_dict[word]:
            break

        try:
            # GEC된 문장에 인덱스가 존재하는 경우는 그냥 넘어가기
            if c_dict[word].pop(0):
                o_dict[word].pop(0)
                continue
        except:
            processed_idx = o_dict[word].pop(0)
            # processed_idx가 마지막 인덱스일 때
            if processed_idx == len(idx_dict_corr):
                _peek, peek_idx = "pre", processed_idx - 1
            else:
                _peek, peek_idx = "post", processed_idx + 1

            peek_word = og_list[peek_idx]

            for i in range(len(corr_list)):
                # peek_word가 corr_sen에 존재하면 넣기
                if peek_word == corr_list[i]:
                    idx_dict_og[word].remove(processed_idx)
                    result.append(processed_idx)

    return result


def get_word_index_by_tag(
        sent: str, 
        corr_sent: str,
        ref_word_list: List,
        tag_list: List,
):
    """
    APPEND/DELETE/REPLACE/TRANSFORM(VERB)/NOUN 총 5개의 Tag Type별로 index를 뽑기 위한 함수.
    sent를 공백 별로 tokenize한 og_list의 index를 기준으로 기록된 리스트를 반환함.

    DELETE/TRANSFORM/NOUN 은 주어진 ref_word 전/후 단어를 확인 후 index의 정확도를 올림.
    APPEND 는 ref_word 이후에 등장하는 단어가 tag에 달려있는 단어와 같은지 확인 후 index를 저장함. (e.g. $APPEND_the)
    REPLACE 는 위의 두 방식을 합쳐 전/후 단어를 확인 후 주어진 index의 단어가 tag에 달려있는 단어와 같은지 확인 후 index를 저장함.

    Args:
        sent (str): 원래 발화
        corr_sent (str): GEC된 발화
        sid (int): 문장 id
        ref_word_list (List): 원래 발화에서 GEC된 단어를 담고 있는 리스트
        tag_list (List): GEC 과정에서 어떤 tag가 적용되었는지 담고 있는 리스트

    Returns:
        List: 각 ref_word의 원래 발화의 어디서 등장하는지 담고있는 리스트
    """    
    og_list = sent.split(" ")
    corr_list = corr_sent.split(" ")

    # 잡은 tag들이 sentence 어디에 위치해있는지 확인
    idx_dict_og = get_ref_word_in_sentence(ref_word_list, og_list)
    idx_dict_corr = get_ref_word_in_sentence(ref_word_list, corr_list)

    fin_idx_list = []
    # tag에 따른 index 추출 (og sentence 기준)
    for idx, word in enumerate(ref_word_list):
        try:
            # 해당하는 index가 하나만 있을 때
            if len(idx_dict_og[word]) == 1:
                idx_og = idx_dict_og[word][0]
                fin_idx_list.append(idx_og)
                continue
            
            append = r'[$]APPEND'
            delete = r'[$]DELETE'
            replace = r'[$]REPLACE'
            transform = r'[$]TRANSFORM'
            noun = r'[$]NOUN'
            if re.match(append, tag_list[idx]):
                # tag에서 단어 분리
                _append, ap_word = tag_list[idx].split("_")

                o_dict = deepcopy(idx_dict_og)
                c_dict = deepcopy(idx_dict_corr)
                # GEC된 문장에서 ref word index 뽑기
                while True:
                    if not o_dict[word] or not c_dict[word]:
                        break

                    idx_og = o_dict[word].pop(0)
                    idx_corr = c_dict[word].pop(0)
                    # 해당 단어의 뒷 단어가 ap_word면 fin_idx_list에 넣어주기
                    if corr_list[idx_corr + 1] == ap_word:
                        idx_dict_og[word].remove(idx_og)
                        fin_idx_list.append(idx_og)
                        break

            elif re.match(delete, tag_list[idx]):
                fin_idx_list.extend(get_by_peek_nearest_word(og_list, corr_list, word, idx_dict_og, idx_dict_corr))
                
            elif re.match(replace, tag_list[idx]):
                _replace, re_word = tag_list[idx].split("_")

                o_dict = deepcopy(idx_dict_og)
                c_dict = deepcopy(idx_dict_corr)
                while True:
                    if not o_dict[word]:
                        break

                    processed_idx = o_dict[word].pop(0)
                    if processed_idx == len(idx_dict_corr):
                        _peek, peek_idx = "pre", processed_idx - 1
                    else:
                        _peek, peek_idx = "post", processed_idx + 1

                    peek_word = og_list[peek_idx]

                    for i in range(len(corr_list)):
                        # peek_word가 corr_sen에 존재하면 넣기
                        if peek_word == corr_list[i] and corr_list[processed_idx] == re_word:
                            idx_dict_og[word].remove(processed_idx)
                            fin_idx_list.append(processed_idx)

            elif re.match(transform, tag_list[idx]):
                fin_idx_list.extend(get_by_peek_nearest_word(og_list, corr_list, word, idx_dict_og, idx_dict_corr))

            elif re.match(noun, tag_list[idx]):
                fin_idx_list.extend(get_by_peek_nearest_word(og_list, corr_list, word, idx_dict_og, idx_dict_corr))

            else:
                # 혹시 모르니까 넣어놓음.. for debugging
                fin_idx_list.append(-1)
        except:
            logging.info(
                "Tag의 index 처리 중 문제가 발생했을 수도 있습니다. 결과값 확인 후 문제가 있다면 Models/utils/gram_out_json.py에 있는 get_word_index_by_tag를 확인해주세요."
            )

    return fin_idx_list


def get_phase_2_inner_data(
        sid: int, 
        sent: str, 
        corr_sent: str,
        edited: bool,
        ref_word_list: List,
        tag_list: List,
        tag_grammar: Dict,
    ):
    inner = {
        "sid": int,
        "sentence": str,
        "corrected_sentence": str,
        "edited": False,
        "ref_word": [],
        "og_index": [],
        "category": [],
        "tag": [],
        "grammar_description": []
    }

    idx_list = get_word_index_by_tag(sent=sent, corr_sent=corr_sent, ref_word_list=ref_word_list, tag_list=tag_list)

    # (ref_word, index, tag) 으로 모아주기
    rit_list = []
    for i in range(len(ref_word_list)):
        try:
            r = ref_word_list[i]
            idx = idx_list[i]
            t = tag_list[i]

            # set 처리
            if (r, idx, t) not in rit_list:
                rit_list.append((r, idx, t))
        except IndexError:
            continue

    inner["edited"] = edited
    inner["sid"] = sid
    inner["sentence"] = sent
    inner["corrected_sentence"] = corr_sent
    inner["edited"] = edited
    inner["ref_word"] = list(list(zip(*rit_list))[0]) # zip으로 분리 후 리스트 wrapping
    inner["og_index"] = list(list(zip(*rit_list))[1])
    inner["tag"] = list(list(zip(*rit_list))[2])

    # 카테고리 추가
    for tag in inner["tag"]:
        if tag in tag_grammar:
            inner["category"].append(tag_grammar[tag]["category"])
            inner["grammar_description"].append(tag_grammar[tag]["desc"])
        else:
            inner["category"].append("어휘")
            inner["grammar_description"].append("WRONG USE OF VOCABULARY")

    return inner


def get_phase_2_data(
        p1_data: Dict,
        checker_data: Dict,
        ctl: List,
        tag_grammar: Dict
    ):
    tag_gram_dict = {
        "tag_grammar_info": []
    }
    sentence_list = list(checker_data.keys())

    for og_sent, inner_dict in checker_data.items():
        gector_dict = get_scrs_tok(inner_dict, ctl)
        sid = sentence_list.index(og_sent)
        sent = og_sent
        corr_sent = inner_dict["fin_sentence"]
        edited = inner_dict["edited"]
        ref_word_list = gector_dict["og_word"]
        tag_list = gector_dict["full_tag"]
        # GEC가 실행됐다면 inner_data 만들기
        if edited == True:
            inner = get_phase_2_inner_data(sid=sid, sent=sent, corr_sent=corr_sent, edited=edited, ref_word_list=ref_word_list, 
                                            tag_list=tag_list, tag_grammar=tag_grammar)
            tag_gram_dict["tag_grammar_info"].append(inner)

    fin_inner = p1_data["phase_1"].copy()
    fin_inner.update(tag_gram_dict)
    phase_2 = {"phase_2": fin_inner}

    return phase_2


def create_json(
        phase: str,
        out_path: str,
        score: float,
        checker_data: Dict,
        token_path: str = "../gector/data/token_labels.txt"

    ):
    ctl = get_cleaned_token_list(token_path)
    tag_grammar = get_tag_grammar(ctl)

    data = get_phase_1_data(score=score, checker_data=checker_data)

    if phase == "phase_2":
        data = get_phase_2_data(
            p1_data=data, checker_data=checker_data, ctl=ctl, tag_grammar=tag_grammar
        )

    # saves JSON file of the output
    # with open(out_path, "w", encoding="utf-8") as out:
    #    json.dump(data, out, ensure_ascii = False, indent="\t")

    return data
