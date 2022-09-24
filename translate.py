import pyscreenshot
import pytesseract
import cv2
import numpy
from  pynput import keyboard
import pyautogui
from time import sleep
from googletrans import Translator


OFFSETX = 0
OFFSETY = 0
GENISLIK = 0
UZUNLUK = 0


def onRelease(key):

  global OFFSETX, OFFSETY, GENISLIK, UZUNLUK

  if key == keyboard.Key.shift:
    GENISLIK, UZUNLUK = pyautogui.position()
    return False

def onPress(key):

  global OFFSETX, OFFSETY, GENISLIK, UZUNLUK

  OFFSETX, OFFSETY, GENISLIK, UZUNLUK = 0, 0, 0, 0

  if key == keyboard.Key.shift:
    OFFSETX, OFFSETY = pyautogui.position()

def main():

  global OFFSETX, OFFSETY, GENISLIK, UZUNLUK

  with keyboard.Listener(on_press=onPress, on_release=onRelease) as shiftWaiter:
    shiftWaiter.join()

    translator = Translator()
    pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract"

    while True:
      try:
        clip = pyscreenshot.grab(bbox=(OFFSETX, OFFSETY, GENISLIK, UZUNLUK))
        ocrString = pytesseract.image_to_string(clip)
        ocrString = ocrString.replace("-\n", "")
        ocrString = ocrString.replace("\n", " ")
        try:
          print(translator.translate(ocrString, dest="tr").text)
          print("-----------------------------------------")
          sleep(3)
        except:
          sleep(500/1000)
          continue
      except FileNotFoundError:
        sleep(500/1000)
        continue


if __name__ == "__main__":
  main()
