import pyaudio
import wave

CHUNK =  4096 # 1度にどれくらい音を録るか
FORMAT = pyaudio.paInt16
CHANNELS = 1 # モノナルなら1、ステレオなら2。今回はラズパイなので1
RATE = 48000 # サンプリングレート
RECORD_SECONDS = 3 # 録音する秒数
dev_index = 1 # デバイスのインデックス


with wave.open("test.wav", "wb") as f:

    p = pyaudio.PyAudio()

    f.setnchannels(CHANNELS)
    f.setsampwidth(p.get_sample_size(FORMAT))
    f.setframerate(RATE)

    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        input_device_index=dev_index
    )

    print('Recording...')
    for _ in range(0, RATE // CHUNK * RECORD_SECONDS):
        ret = stream.read(CHUNK, exception_on_overflow = False)
        f.writeframes(ret)
    print('Recording Completed')

    stream.close()
    p.terminate()
