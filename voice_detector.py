from yamabiko import IVoiceDetector
import time

import pyaudio
import whisper
import collections
import wave

CHUNK =  4096 # 1度にどれくらい音を録るか
FORMAT = pyaudio.paInt16
CHANNELS = 1 # モノナルなら1、ステレオなら2。今回はラズパイなので1
RATE = 48000 # サンプリングレート
RECORD_SECONDS = 15 # 録音する秒数

class RingBuffer(object):
    def __init__(self, size=4096):
        self._buf = collections.deque(maxlen=size)

    def extend(self, data):
        self._buf.extend(data)

    def get(self):
        tmp = bytes(bytearray(self._buf))
        self._buf.clear()
        return tmp

class VoiceDetector(IVoiceDetector):

    def __init__(self):
        self._audio = pyaudio.PyAudio()
        self._stream_in = self._audio.open(
            input=True,
            output=False,
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            stream_callback=self.audio_callback
        )
        self._ring_buffer = RingBuffer(CHANNELS * RATE * 5)
        self._running = True
        self._model = whisper.load_model("tiny") # モデルを指定する

    def audio_callback(
            self,
            in_data,
            frame_count,
            time_info,
            status
        ):
        self._ring_buffer.extend(in_data)
        play_data = chr(0) * len(in_data)
        return play_data, pyaudio.paContinue
    
    def include_hotword(self, data):
        pass
        # data -> wave file
        # with wave.open("test.wav", "wb") as f:
        #     f.setnchannels(CHANNELS)
        #     f.setframerate(RATE)
        #     f.setsampwidth(self._audio.get_sample_size(FORMAT))
        #     f.writeframes(data)

        # result = self._model.transcribe(
        #     data,
        #     verbose=True,
        #     language="ja"
        # )
        # sentence = result["text"]
        # print(sentence)
        # if "天気" in sentence:
        #     return True
        # else:
        #     return False

    def start(self):
        while self._running:
            data = self._ring_buffer.get()
            if len(data) == 0:
                time.sleep(1)
                print("data is empty")
                continue

            # print(type(data))
            # print(len(data)) # 36864 = 288 * 128 bytes

            with wave.open("test.wav", "wb") as f:
                f.setnchannels(CHANNELS)
                f.setframerate(RATE)
                f.setsampwidth(self._audio.get_sample_size(FORMAT))

            # if self.include_hotword(data):
                # print("天気")


    