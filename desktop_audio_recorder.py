import pyaudio
import wave
from pynput import keyboard
from time import sleep

class DesktopAudioRecorder:
    def __init__(self):
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 4
        self.RATE = 48000
        self.OUTPUT_FILENAME = "output.wav"
        self.p = pyaudio.PyAudio()
        self.frames = []
        self.recording = False
        self.stream = None
        self.device_index = None

    def find_audio_device(self):
        for i in range(self.p.get_device_count()):
            info = self.p.get_device_info_by_index(i)
            if "Microsoft Sound Mapper - Input" in info["name"]:
                self.device_index = info["index"]
                break

    def start_recording(self):
        if not self.recording:
            print("Kayit basladi...")
            self.recording = True
            self.stream = self.p.open(format=self.FORMAT,
                                      channels=self.CHANNELS,
                                      rate=self.RATE,
                                      input=True,
                                      input_device_index=self.device_index,
                                      frames_per_buffer=self.CHUNK,
                                      stream_callback=self.record_sound)

    def stop_recording(self):
        if self.recording:
            print("Kayit tamamlandi.")
            self.recording = False
            self.stream.stop_stream()
            self.stream.close()
            # self.p.terminate()
            wf = wave.open(self.OUTPUT_FILENAME, "wb")
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b"".join(self.frames))
            wf.close()
            print("Kaydedilen ses dosyasi:", self.OUTPUT_FILENAME)
            self.frames = []

    def record_sound(self, in_data, frame_count, time_info, status):
        self.frames.append(in_data)
        return (in_data, pyaudio.paContinue)

    def on_press(self, key):
        try:
            charKey = key.char
        except AttributeError:
            charKey = None

        if charKey in ["k", "K"]:
            self.start_recording()

    def on_release(self, key):
        try:
            charKey = key.char
        except AttributeError:
            charKey = None

        if charKey in ["k", "K"]:
            self.stop_recording()
            if key == keyboard.Key.esc:
                return False

    def run(self):
        print("Kaydetmek icin 'k' tusuna basin. Kaydetmeyi durdurmak icin 'k' tusunu birakin.")
        self.find_audio_device()

        keyboard.Listener(on_press=self.on_press, on_release=self.on_release).start()

        while True:
            sleep(100)

# if __name__ == "__main__":
#     recorder = DesktopAudioRecorder()
#     recorder.run()
