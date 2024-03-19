from fastapi import FastAPI, File, UploadFile, Body, HTTPException, Form
from typing import List
import torch
from torchvision import transforms
from PIL import Image
import uvicorn
import shutil
from pydantic import BaseModel
from typing_extensions import Annotated
import os
import sys
from logging import Logger
import uvicorn

from typing import Optional, Union, List, Pattern
from typing_extensions import Literal

from phonemizer.backend import BACKENDS
from phonemizer.backend.base import BaseBackend
from phonemizer.backend.espeak.language_switch import LanguageSwitch
from phonemizer.backend.espeak.words_mismatch import WordMismatch
from phonemizer.logger import get_logger
from phonemizer.punctuation import Punctuation
from phonemizer.separator import default_separator, Separator
from phonemizer.utils import list2str, str2list

from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import soundfile as sf
import torch

import json
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-lv-60-espeak-cv-ft",cache_dir = '/dev/shm/phoneme/lv')
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-lv-60-espeak-cv-ft", cache_dir = '/dev/shm/phoneme/lv')
Backend = Literal['espeak', 'espeak-mbrola', 'festival', 'segments']

app = FastAPI()
# FOAM 관련 참고
# @app.post("/files/")
# async def create_file(
#     fileb: Annotated[UploadFile, File()],
#     token: Annotated[str, Form()],
# ):
#     return {
#         "token": token,
#         "fileb_content_type": fileb.content_type,
#     }

#1. text to phoneme(model1)
def phonemize(  # pylint: disable=too-many-arguments
        text,
        language: str = 'en-us',
        backend: Backend = 'espeak',
        separator: Optional[Separator] = default_separator,
        strip: bool = False,
        prepend_text: bool = False,
        preserve_empty_lines: bool = False,
        preserve_punctuation: bool = False,
        punctuation_marks: Union[str, Pattern] = Punctuation.default_marks(),
        with_stress: bool = False,
        tie: Union[bool, str] = False,
        language_switch: LanguageSwitch = 'keep-flags',
        words_mismatch: WordMismatch = 'ignore',
        njobs: int = 1,
        logger: Logger = get_logger()):

     
    # ensure we are using a compatible Python version
    if sys.version_info < (3, 6):  # pragma: nocover
        logger.error(
            'Your are using python-%s which is unsupported by the phonemizer, '
            'please update to python>=3.6', ".".join(sys.version_info))

    # ensure the arguments are valid
    _check_arguments(
        backend, with_stress, tie, separator, language_switch, words_mismatch)

    # preserve_punctuation and word separator not valid for espeak-mbrola
    if backend == 'espeak-mbrola' and preserve_punctuation:
        logger.warning('espeak-mbrola backend cannot preserve punctuation')
    if backend == 'espeak-mbrola' and separator.word:
        logger.warning('espeak-mbrola backend cannot preserve word separation')

    # initialize the phonemization backend
    if backend == 'espeak':
        phonemizer = BACKENDS[backend](
            language,
            punctuation_marks=punctuation_marks,
            preserve_punctuation=preserve_punctuation,
            with_stress=with_stress,
            tie=tie,
            language_switch=language_switch,
            words_mismatch=words_mismatch,
            logger=logger)
    elif backend == 'espeak-mbrola':
        phonemizer = BACKENDS[backend](
            language,
            logger=logger)
    else:  # festival or segments
        phonemizer = BACKENDS[backend](
            language,
            punctuation_marks=punctuation_marks,
            preserve_punctuation=preserve_punctuation,
            logger=logger)

    # do the phonemization
    return _phonemize(phonemizer, text, separator, strip, njobs, prepend_text, preserve_empty_lines)


def _check_arguments(  # pylint: disable=too-many-arguments
        backend: Backend,
        with_stress: bool,
        tie: Union[bool, str],
        separator: Separator,
        language_switch: LanguageSwitch,
        words_mismatch: WordMismatch):
    """Auxiliary function to phonemize()

    Ensures the parameters are compatible with each other, raises a
    RuntimeError the first encountered error.

    """
    # ensure the backend is either espeak, festival or segments
    if backend not in ('espeak', 'espeak-mbrola', 'festival', 'segments'):
        raise RuntimeError(
            '{} is not a supported backend, choose in {}.'
                .format(backend, ', '.join(
                ('espeak', 'espeak-mbrola', 'festival', 'segments'))))

    # with_stress option only valid for espeak
    if with_stress and backend != 'espeak':
        raise RuntimeError(
            'the "with_stress" option is available for espeak backend only, '
            'but you are using {} backend'.format(backend))

    # tie option only valid for espeak
    if tie and backend != 'espeak':
        raise RuntimeError(
            'the "tie" option is available for espeak backend only, '
            'but you are using {} backend'.format(backend))

    # tie option incompatible with phone separator
    if tie and separator.phone:
        raise RuntimeError(
            'the "tie" option is incompatible with phone separator '
            f'(which is "{separator.phone}")')

    # language_switch option only valid for espeak
    if language_switch != 'keep-flags' and backend != 'espeak':
        raise RuntimeError(
            'the "language_switch" option is available for espeak backend '
            'only, but you are using {} backend'.format(backend))

    # words_mismatch option only valid for espeak
    if words_mismatch != 'ignore' and backend != 'espeak':
        raise RuntimeError(
            'the "words_mismatch" option is available for espeak backend '
            'only, but you are using {} backend'.format(backend))


def _phonemize(  # pylint: disable=too-many-arguments
        backend: BaseBackend,
        text: Union[str, List[str]],
        separator: Separator,
        strip: bool,
        njobs: int,
        prepend_text: bool,
        preserve_empty_lines: bool):

    # remember the text type for output (either list or string)
    text_type = type(text)

    # force the text as a list
    text = [line.strip(os.linesep) for line in str2list(text)]

    # if preserving empty lines, note the index of each empty line
    if preserve_empty_lines:
        empty_lines = [n for n, line in enumerate(text) if not line.strip()]

    # ignore empty lines
    text = [line for line in text if line.strip()]

    if (text):
        # phonemize the text
        phonemized = backend.phonemize(
            text, separator=separator, strip=strip, njobs=njobs)
    else:
        phonemized = []

    # if preserving empty lines, reinsert them into text and phonemized lists
    if preserve_empty_lines:
        for i in empty_lines: # noqa
            if prepend_text:
                text.insert(i, '')
            phonemized.insert(i, '')

    # at that point, the phonemized text is a list of str. Format it as
    # expected by the parameters
    if prepend_text:
        return list(zip(text, phonemized))
    if text_type == str:
        return list2str(phonemized)
    return phonemized


#3. 모델1, 2의 결과 phoneme 비교
def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]

@app.post("/upload/")
async def upload_wav_and_json(
    wav_file: Annotated[UploadFile, File()],
    text: Annotated[str, Form()],
):
    try:
        
        # WAV 파일 저장
        with open(wav_file.filename, "wb") as buffer:
            shutil.copyfileobj(wav_file.file, buffer)
        
        #print(text)
        transcription = text
        ttp_result = phonemize(transcription)
        audio_input, sampling_rate = sf.read(wav_file.filename)
        input_values = processor(audio_input, sampling_rate=sampling_rate, return_tensors="pt").input_values
        # 모델을 사용해 추론
        with torch.no_grad():
            logits = model(input_values).logits

        # 추론된 logits에서 argmax를 취하고 phoneme으로 디코딩
        predicted_ids = torch.argmax(logits, dim=-1)
        # transcription = processor.batch_decode(predicted_ids)
        wtp = processor.batch_decode(predicted_ids, skip_special_tokens=True, output_char_offsets=True)


        #결과 출력
        wtp_result = wtp.text[0]

        #모델의 결과 입력
        result_1 = ttp_result
        result_2 = wtp_result

        #문자열 공백 지우기
        result_1 = result_1.replace(" ", "")
        result_2 = result_2.replace(" ", "")

        #거리 계산
        # distance = levenshtein(pho_model_1, pho_model_2)
        distance = levenshtein(result_1, result_2)
        print(result_1)
        print(result_2)
        print(f"Number of phonemes that differ: {distance}")
        return {"different phenomes":distance}
    except Exception as e:
        return {"wav_filename": None, "json_data": None, "status": f"Error: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)
