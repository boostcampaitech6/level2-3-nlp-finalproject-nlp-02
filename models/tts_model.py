from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
from datasets import load_dataset
import torch
import soundfile as sf
from datasets import load_dataset

import json

#warnings 무시
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

#json 파일 로드
##json파일경로 받을 위치 -> '/home/minari/dataset/label.json'##
with open('/home/minari/dataset/label.json', 'r') as file:
    data = json.load(file)


#모델 경로 지정
model_save_path = 'microsoft/speecht5_tts'
vocoder_save_path = 'microsoft/speecht5_hifigan'
processor_save_path = 'microsoft/speecht5_tts'

#모델 불러오기
processor = SpeechT5Processor.from_pretrained(processor_save_path)
vocoder = SpeechT5HifiGan.from_pretrained(vocoder_save_path)
model = SpeechT5ForTextToSpeech.from_pretrained(model_save_path)


inputs = processor(text="Do you think parks are important? How are parks in your country different from parks in other countries?", return_tensors="pt")

# load xvector containing speaker's voice characteristics from a dataset
embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
speaker_embeddings = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)

speech = model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=vocoder)

audio_file_path = data['basic_info']['wav_path']

sf.write(audio_file_path, speech.numpy(), samplerate=16000)

