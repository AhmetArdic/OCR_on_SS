import desktop_audio_recorder
import screenshot_ocr

import time
import threading

if __name__ == "__main__":
    recorder = desktop_audio_recorder.DesktopAudioRecorder()
    ocr = screenshot_ocr.ScreenshotOCR()

    print("Kaydetmek icin 'k' tusuna basin. Kaydetmeyi durdurmak icin 'k' tusunu birakin.")
    print("Ekran goruntusu almak icin, secilecek metnin sol ust kosesine cursor getirip 'shift' tusuna basin, bu tus basili iken")
    print("metnin sag alt kosesine cursor getirin ve 'shift' tusundan elinizi cekin.")
    print("OCR yapmak icin 'o' tusuna basin.")
    print("OCR metnini yazdirmak için 'p' tusuna basin.")
    print("-----------------------------------------")

    threading.Thread(target=recorder.run())
    threading.Thread(target=ocr.run()) 

while True:
    time.sleep(100)