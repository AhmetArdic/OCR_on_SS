import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence

class SpeechRecognizer:
    def __init__(self, path):
        self.r = sr.Recognizer()
        self.path = path

    def transcribe_audio(self, path):
        with sr.AudioFile(path) as source:
            audio_listened = self.r.record(source)
            text = self.r.recognize_google(audio_listened)
        return text

    def get_large_audio_transcription_on_silence(self):
        sound = AudioSegment.from_file(self.path)
        chunks = split_on_silence(sound, min_silence_len=500, silence_thresh=sound.dBFS-14, keep_silence=500)
        folder_name = "audio-chunks"
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)
        whole_text = ""
        for i, audio_chunk in enumerate(chunks, start=1):
            chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
            audio_chunk.export(chunk_filename, format="wav")
            try:
                text = self.transcribe_audio(chunk_filename)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                whole_text += text
        return whole_text

    def get_large_audio_transcription_fixed_interval(self, seconds=60):
        sound = AudioSegment.from_file(self.path)  
        # split the audio file into chunks
        chunk_length_ms = int(1000 * seconds)
        chunks = [sound[i:i + chunk_length_ms] for i in range(0, len(sound), chunk_length_ms)]
        folder_name = "audio-fixed-chunks"
        # create a directory to store the audio chunks
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)
        whole_text = ""
        # process each chunk 
        for i, audio_chunk in enumerate(chunks, start=1):
            # export audio chunk and save it in
            # the `folder_name` directory.
            chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
            audio_chunk.export(chunk_filename, format="wav")
            # recognize the chunk
            try:
                text = self.transcribe_audio(chunk_filename)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                whole_text += text
        # return the text for all chunks detected
        return whole_text
    
    def run_for_large_audio(self):
        self.full_text = self.get_large_audio_transcription_on_silence()

    def run(self):
        self.full_text = self.transcribe_audio(self.path)
        

# if __name__ == "__main__":
#     recognizer = SpeechRecognizer("output.wav")
#     recognizer.run()
#     print("\nFull text:", recognizer.full_text)
