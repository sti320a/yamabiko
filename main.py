import wave
import sys

import pyaudio

import requests
import json
from pprint import pprint
from datetime import datetime

def get_weather_forecast():
    url = 'https://www.jma.go.jp/bosai/forecast/data/forecast/130000.json'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # 明日の天気情報を取得
        time = data[0]['timeSeries'][0]['timeDefines'][-1]
        dtime = datetime.fromisoformat(time)
        time = datetime.strftime(dtime, '%m月%d日 %H時')
        tomorrow_weather = data[0]['timeSeries'][0]['areas'][0]['weathers'][-1].replace("\u3000", " ")
        return f"明日、{time}の天気は、{tomorrow_weather}です"
    else:
        return "天気予報の取得でエラーが発生しました"

CHUNK =  4096 # 1度にどれくらい音を録るか
FORMAT = pyaudio.paInt16
CHANNELS = 1 # モノナルなら1、ステレオなら2。今回はラズパイなので1
RATE = 48000 # サンプリングレート
RECORD_SECONDS = 15 # 録音する秒数

dev_index = 1 # デバイスのインデックス

with wave.open('output.wav', 'wb') as wf:
    p = pyaudio.PyAudio()

    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)

    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        input_device_index=dev_index
    )

    print('Recording...')
    for _ in range(0, RATE // CHUNK * RECORD_SECONDS):
        wf.writeframes(stream.read(CHUNK, exception_on_overflow = False))
    print('Recording Completed')

    stream.close()
    p.terminate()


### Whisperで文字起こし
import time
import whisper

print('Loading model...')
model = whisper.load_model("tiny") # モデルを指定する

print('Transcribing...')
result = model.transcribe("output.wav", verbose=True, language="ja") # 音声ファイルを指定する
sentence = result["text"]
print(sentence) # 認識結果を出力


if "明日の天気" in sentence:
    answer_sentence  = get_weather_forecast()


# openjtalk.py
import pyopenjtalk
from scipy.io import wavfile
import numpy as np
x, sr = pyopenjtalk.tts(answer_sentence)
answer_wav_name = "answer.wav"
wavfile.write(answer_wav_name, sr, x.astype(np.int16))


# Play Audio
wf = wave.open("answer.wav", 'rb')
p = pyaudio.PyAudio()
stream = p.open(
    format =p.get_format_from_width(wf.getsampwidth()),
    channels = wf.getnchannels(),
    rate = wf.getframerate(),
    output = True
)

data = wf.readframes(CHUNK)

while data:
    stream.write(data)
    data = wf.readframes(CHUNK)

wf.close()
stream.close()    
p.terminate()
