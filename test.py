import speech_recognition
import pyaudio
import wave
 
RECORD_SECONDS = 10         # 録音する時間
FILENAME = 'record.wav'     # 保存するファイル名
iDeviceIndex = 0            # 録音デバイスの番号
FORMAT = pyaudio.paInt16    # 音声フォーマット
CHANNELS = 1                # チャンネル数（モノラル）
RATE = 44100                # サンプリングのレート
CHUNK = 2**11               # データ点数
 
def main():
    record()
    recognition()
 
def record():
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        input_device_index=iDeviceIndex,
                        frames_per_buffer=CHUNK)
    print("recording...")       # 録音開始
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("finish recording")   # 録音終了
 
    stream.stop_stream()
    stream.close()
    audio.terminate()
 
    waveFile = wave.open(FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()
 
def recognition():
    r = speech_recognition.Recognizer()
    with speech_recognition.AudioFile(FILENAME) as src:
        audio = r.record(src)
    print(r.recognize_google(audio, key='Your API Key', language='ja-JP'))
 
if __name__ == '__main__':
    main()