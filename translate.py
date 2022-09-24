import pyscreenshot
import pytesseract
from  pynput import keyboard
import pyautogui
from time import sleep
from googletrans import Translator
from PIL import Image


X1, Y1, X2, Y2 = 0, 0, 1, 1

def onRelease(key):

  global X2, Y2

  if key == keyboard.Key.shift:
    X2, Y2 = pyautogui.position()
    return False

def onPress(key):

  global X1, Y1, X2, Y2

  X1, Y1, X2, Y2 = 0, 0, 0, 0

  if key == keyboard.Key.shift:
    X1, Y1 = pyautogui.position()

def setDPI300(file_path):
  im = Image.open(file_path)
  length_x, width_y = im.size
  factor = min(1, float(1024.0 / length_x))
  size = int(factor * length_x), int(factor * width_y)
  im_resized = im.resize(size, Image.Resampling.LANCZOS)
  im_resized.save(file_path, dpi=(300, 300))


def main():

  global X1, Y1, X2, Y2

  with keyboard.Listener(on_press=onPress, on_release=onRelease) as clipArea:
    clipArea.join()

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
