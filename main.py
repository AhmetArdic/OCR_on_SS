import desktop_audio_recorder
import screenshot_ocr
import communication
import dual_writer

import sys

class Main:
    def __init__(self):
        self.recorder = desktop_audio_recorder.DesktopAudioRecorder()
        self.ocr = screenshot_ocr.ScreenshotOCR()
        self.communication = communication.SerialModule('COM1', 9600, 'N', 8)
        self.dual_printer = dual_writer.DualWriter(self.communication, sys.stdout)

        sys.stdout = self.dual_printer

        self.communication.open()

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

    def run(self):
        self.communication.listen()

if __name__ == "__main__":
    main = Main()
    main.run()