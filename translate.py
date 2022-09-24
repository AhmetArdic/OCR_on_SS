import pyscreenshot
import pytesseract
from  pynput import keyboard
import pyautogui
from time import sleep
from googletrans import Translator
from PIL import Image


X1, Y1, X2, Y2 = 0, 0, 1, 1
tempX1, tempY1, tempX2, tempY2 = 0, 0, 0, 0

def onRelease(key):

  global tempX2, tempY2

  if key == keyboard.Key.shift:
    tempX2, tempY2 = pyautogui.position()

def onPress(key):

  global X1, Y1, X2, Y2
  global tempX1, tempY1, tempX2, tempY2

  if key == keyboard.Key.shift:
    tempX1, tempY1 = pyautogui.position()
  elif key.char in ["y", "Y"]:
    X1, Y1, X2, Y2 = tempX1, tempY1, tempX2, tempY2


def setDPI300(file_path):
  im = Image.open(file_path)
  length_x, width_y = im.size
  factor = min(1, float(1024.0 / length_x))
  size = int(factor * length_x), int(factor * width_y)
  im_resized = im.resize(size, Image.Resampling.LANCZOS)
  im_resized.save(file_path, dpi=(300, 300))


def main():

  global X1, Y1, X2, Y2

  with keyboard.Listener(on_press=onPress, on_release=onRelease):

    translator = Translator()
    pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract"

    while True:

      pyscreenshot.grab(bbox=(X1, Y1, X2, Y2)).save("clip.jpg")
      setDPI300("clip.jpg")
      clip = Image.open("clip.jpg")
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


if __name__ == "__main__":
  main()
