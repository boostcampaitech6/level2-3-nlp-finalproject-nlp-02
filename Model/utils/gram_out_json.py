import re

import json
from pprint import pprint
from typing import List, Dict


def load_token_list(
        token_path: str
    ):
    with open(token_path, "r", encoding="utf-8") as t:
        token_list = list(map(lambda x: x.strip(), t.readlines()))
    
    return token_list


def get_cleaned_token_list(
        token_path: str = "../gector/data/token_labels.txt"
    ):
    print("=== Removing Tokens ===")
    
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
    """creates the inner dictionary of check file including original sentence, edited, og_word,
    action_tag, full_tag and corrected sentence

    Args:
        inner_dict (Dict): _description_
        tok_list (List): _description_

    Returns:
        _type_: _description_
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
        tag_list: List
    ):
    """Creates tag-grammar dictionary and indicates the category of the grammar correction

    Args:
        tag_list (List): _description_

    Returns:
        _type_: _description_
    """
    # trans = r'[$](TRANSFORM)_[\w]'
    # trans_list = [item for item in tag_list if re.match(trans, item)]

    tag_grammar_dict = {
        '$TRANSFORM_VERB_VB_VBZ': {
            'category': '주어-동사 수일치',
            'desc': 'PLURAL TO SINGULAR VERB'
        },
        '$TRANSFORM_VERB_VB_VBN': {
            'category': '시제',
            'desc': 'PRESENT TO PAST PARTICIPLE'
        },
        '$TRANSFORM_VERB_VB_VBD': {
            'category': '시제',
            'desc': 'PRESENT TO PAST TENSE'
        },
        '$TRANSFORM_VERB_VB_VBG': {
            'category': '동사 형태',
            'desc': 'PRESENT TO PRESENT PARTICIPLE'
        },
        '$TRANSFORM_VERB_VBZ_VB': {
            'category': '동사 형태',
            'desc': 'SINGULAR TO PLURAL VERB'
        },
        '$TRANSFORM_VERB_VBZ_VBN': {
            'category': '동사 형태',
            'desc': 'SINGULAR VERB TO PAST PARTICIPLE'
        },
        '$TRANSFORM_VERB_VBZ_VBD': {
            'category': '시제',
            'desc': 'SINGULAR VERB TO PAST TENSE'
        },
        '$TRANSFORM_VERB_VBZ_VBG': {
            'category': '동사 형태',
            'desc': 'SINGULAR VERB TO PRESENT PARTICIPLE'
        },
        '$TRANSFORM_VERB_VBN_VB': {
            'category': '시제',
            'desc': 'PAST PARTICIPLE TO PRESENT TENSE'
        },
        '$TRANSFORM_VERB_VBN_VBZ': {
            'category': '동사 형태',
            'desc': 'PAST PARTICIPLE TO SINGULAR VERB'
        },
        '$TRANSFORM_VERB_VBN_VBD': {
            'category': '시제',
            'desc': 'PAST PARTICIPLE TO PAST TENSE'
        },
        '$TRANSFORM_VERB_VBN_VBG': {
            'category': '동사 형태',
            'desc': 'PAST PARTICIPLE TO PRESENT PARTICIPLE'
        },
        '$TRANSFORM_VERB_VBD_VB': {
            'category': '시제',
            'desc': 'PAST TENSE TO PRESENT TENSE'
        },
        '$TRANSFORM_VERB_VBD_VBZ': {
            'category': '동사 형태',
            'desc': 'PAST TENSE TO SINGULAR VERB'
        },
        '$TRANSFORM_VERB_VBD_VBN': {
            'category': '동사 형태',
            'desc': 'PAST TENSE TO PAST PARTICIPLE'
        },
        '$TRANSFORM_VERB_VBD_VBG': {
            'category': '동사 형태',
            'desc': 'PAST TENSE TO PRESENT PARTICIPLE'
        },
        '$TRANSFORM_VERB_VBG_VB': {
            'category': '시제',
            'desc': 'PRESENT PARTICIPLE TO PRESENT TENSE'
        },
        '$TRANSFORM_VERB_VBG_VBZ': {
            'category': '시제',
            'desc': 'PRESENT PARTICIPLE TO SINGULAR VERB'
        },
        '$TRANSFORM_VERB_VBG_VBN': {
            'category': '동사 형태',
            'desc': 'PRESENT PARTICIPLE TO PAST PARTICIPLE'
        },
        '$TRANSFORM_VERB_VBG_VBD': {
            'category': '시제',
            'desc': 'PRESENT PARTICIPLE TO PAST TENSE'
        },
        '$TRANSFORM_AGREEMENT_SINGULAR': {
            'category': '명사 수일치',
            'desc': 'SINGULAR TO PLURAL NOUN'
        },
        '$TRANSFORM_AGREEMENT_PLURAL': {
            'category': '명사 수일치',
            'desc': 'PLURAL TO SINGULAR NOUN'
        }
    }

    # 33 common preposition list
    preps = ["across", "to", "on", "with", "in", "of", "at", "inside", "during", "from", 
             "as", "through", "for", "along", "about", "into", "towards", "down", 
             "behind", "round", "before", "by", "against", "between", "onto", "off", "beside", 
             "around", "over", "among", "above", "after", "beneath"]
    preps_tag_list = [tag for tag in tag_list if tag.split('_')[-1] in preps]

    for p in preps_tag_list:
        tag_grammar_dict[p] = {
            'category': '전치사',
            'desc': 'PREPOSITION'
        }

    return tag_grammar_dict


def get_phase_1_data(
        score: float, 
        check_data: Dict
    ):
    og_list = list(check_data.keys())
    corrected_list = [str(check_data[og]["fin_sentence"]) for og in check_data.keys()]

    inner = {
        "score": score,
        "original_passage": ' '.join(og_list),
        "corrected_passage": ' '.join(corrected_list)
    }
    phase_1 = {"phase_1": inner}
    
    return phase_1


def get_phase_2_inner_data(
        sid: int, 
        sent: str, 
        corr_sent: str,
        edited: bool,
        ref_word_list: List,
        tag_list: List,
        tag_grammar: Dict
    ):
    inner = {
        "sid": int,
        "sentence": str,
        "corrected_sentence": str,
        "edited": False,
        "ref_word": [],
        "category": [],
        "tag": [],
        "grammar_description": []
    }
    inner["sid"] = sid
    inner["sentence"] = sent
    inner["corrected_sentence"] = corr_sent
    inner["edited"] = edited
    inner["ref_word"] = ref_word_list
    inner["tag"] = tag_list

    for tag in tag_list:
        if tag in tag_grammar:
            inner["category"].append(tag_grammar[tag]["category"])
            inner["grammar_description"].append(tag_grammar[tag]["desc"])
        else:
            inner["category"].append("어휘")
            inner["grammar_description"].append("WRONG USE OF VOCABULARY")

    return inner


def get_phase_2_data(
        p1_data: Dict,
        check_data: Dict,
        ctl: List,
        tag_grammar: Dict
    ):
    tag_gram_dict = {
        "tag_grammar_info": []
    }
    sentence_list = list(check_data.keys())

    for og_sent, inner_dict in check_data.items():
        gector_dict = get_scrs_tok(inner_dict, ctl)
        sid = sentence_list.index(og_sent)
        sent = og_sent
        corr_sent = inner_dict["fin_sentence"]
        edited = inner_dict["edited"]
        ref_word_list = gector_dict["og_word"]
        tag_list = gector_dict["full_tag"]
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
        check_data: Dict
    ):
    ctl = get_cleaned_token_list()
    tag_grammar = get_tag_grammar(ctl)

    data = get_phase_1_data(score=score, check_data=check_data)

    if phase == "phase_2":
        data = get_phase_2_data(p1_data=data, check_data=check_data, ctl=ctl, tag_grammar=tag_grammar)
    
    # with open(out_path, "w", encoding="utf-8") as out:
    #    json.dump(data, out, ensure_ascii = False, indent="\t")
            
    return data