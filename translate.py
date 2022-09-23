import pyscreenshot
import pytesseract
from threading import Thread
from time import sleep
from PIL import Image
from googletrans import Translator

pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract"

def clipperForTranslate():

  OFFSETX = 0
  OFFSETY = 100
  GENISLIK = 720
  UZUNLUK = 980

  while True:
    clip = pyscreenshot.grab(bbox=(OFFSETX, OFFSETY, GENISLIK, UZUNLUK))
    clip.save("clip.jpg")
    sleep(1500/1000)

def OCRandTranslate():

  translator = Translator()

  while True:
    try:
      clip = Image.open("clip.jpg")
      ocrString = pytesseract.image_to_string(clip)
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

Thread(target=OCRandTranslate).start()
Thread(target=clipperForTranslate, daemon=True).start()
