import desktop_audio_recorder
import screenshot_ocr
import communication
import dual_writer

from pynput import keyboard
from time import sleep
import sys

class Main:
    def __init__(self):
        self.recorder = desktop_audio_recorder.DesktopAudioRecorder()
        self.ocr = screenshot_ocr.ScreenshotOCR()

        # self.settings_for_serial_communication()
        self.settings_for_this_computer()

    def settings_for_this_computer(self):
        print("-----------------------------------------")
        print("k, K -> ses kayit/kaydet")
        print("l, L -> kayitli sesi yaziya cevir")
        print("shift (on_press) -> yazi kapsayan cercevenin sol ust kosesi (first corner)")
        print("shift (on_release) -> yazi kapsayan cercevenin sag alt kosesi (second corner)")
        print("o, O -> ekran goruntusunden OCR yap ve yazdir")
        print("-----------------------------------------")
        

    def settings_for_serial_communication(self):
        self.communication = communication.SerialModule('COM1', 9600, 'N', 8)
        self.dual_printer = dual_writer.DualWriter(self.communication, sys.stdout)

        sys.stdout = self.dual_printer

        self.communication.open()

        print("-----------------------------------------")
        print("k, K -> ses kayit/kaydet")
        print("l, L -> kayitli sesi yaziya cevir")
        print("f, F -> yazi kapsayan cercevenin sol ust kosesi (first corner)")
        print("s, S -> yazi kapsayan cercevenin sag alt kosesi (second corner)")
        print("o, O -> ekran goruntusunden OCR yap ve yazdir")
        print("-----------------------------------------")

        self.communication.add_listener('f', self.ocr.process_f); self.communication.add_listener('F', self.ocr.process_f)
        self.communication.add_listener('s', self.ocr.process_s); self.communication.add_listener('S', self.ocr.process_s)
        self.communication.add_listener('o', self.ocr.process_o); self.communication.add_listener('O', self.ocr.process_o)
        # self.communication.add_listener('p', self.ocr.process_p); self.communication.add_listener('P', self.ocr.process_p)
        self.communication.add_listener('k', self.recorder.process_k); self.communication.add_listener('K', self.recorder.process_k)
        self.communication.add_listener('l', self.recorder.process_l); self.communication.add_listener('L', self.recorder.process_l)

    def on_release(self, key):
        if key == keyboard.Key.shift:
            self.ocr.process_s()

    def on_press(self, key):
        try:
            charKey = key.char
        except AttributeError:
            charKey = None
        
        if key == keyboard.Key.shift:
            self.ocr.process_f()

        elif charKey in ["o", "O"]:
            self.ocr.process_o()
        elif charKey in ["k", "K"]:
            self.recorder.process_k()
        elif charKey in ["l", "L"]:
            self.recorder.process_l()

    def run(self):
        # self.communication.listen()
        keyboard.Listener(on_press=self.on_press, on_release=self.on_release).start()

        while True:
            sleep(100)

if __name__ == "__main__":
    main = Main()
    main.run()