import pyaudio
import wave
import speech_recognizer

class DesktopAudioRecorder:
    def __init__(self):
        self._CHUNK = 1024
        self._FORMAT = pyaudio.paInt16
        self._CHANNELS = 2
        self._RATE = 44100
        self._OUTPUT_FILENAME = "output.wav"
        
        self._p = pyaudio.PyAudio()
        self._frames = []
        self.recording = False
        self._stream = None
        self._device_index = 2

        self.audioString = ""

    def print_audio_device(self):
        for i in range(self._p.get_device_count()):
            info = self._p.get_device_info_by_index(i)
            print(info)

    def start_recording(self):
        print("Kayit basladi...")
        self._stream = self._p.open(format=self._FORMAT,
                                    channels=self._CHANNELS,
                                    rate=self._RATE,
                                    input=True,
                                    input_device_index=self._device_index,
                                    frames_per_buffer=self._CHUNK,
                                    stream_callback=self.record_sound)

    def stop_recording(self):
        print("Kayit tamamlandi.")
        self._stream.stop_stream()
        self._stream.close()
        # self._p.terminate()
        wf = wave.open(self._OUTPUT_FILENAME, "wb")
        wf.setnchannels(self._CHANNELS)
        wf.setsampwidth(self._p.get_sample_size(self._FORMAT))
        wf.setframerate(self._RATE)
        wf.writeframes(b"".join(self._frames))
        wf.close()
        print("Kaydedilen ses dosyasi:", self._OUTPUT_FILENAME)
        print("-----------------------------------------")
        self._frames = []

    def record_sound(self, in_data, frame_count, time_info, status):
        self._frames.append(in_data)
        return (in_data, pyaudio.paContinue)
    
    def speech_to_text(self):
        recognizer = speech_recognizer.SpeechRecognizer("output.wav")
        recognizer.run_for_large_audio()
        self.audioString = recognizer.full_text
        print("\nTam Yazi:", recognizer.full_text)
        print("-----------------------------------------")

    def process_k(self):
        if not self.recording:
            self.recording= True
            self.start_recording()
        elif self.recording:
            self.recording = False
            self.stop_recording()

    def process_l(self):
        self.speech_to_text()

# if __name__ == "__main__":
#     recorder = DesktopAudioRecorder()
#     recorder.run()
