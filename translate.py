import pyscreenshot
import pytesseract
from time import sleep
from googletrans import Translator


def main():

  pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract"
  translator = Translator()

  OFFSETX = 0
  OFFSETY = 100
  GENISLIK = 720
  UZUNLUK = 980

  while True:
    clip = pyscreenshot.grab(bbox=(OFFSETX, OFFSETY, GENISLIK, UZUNLUK))
    ocrString = pytesseract.image_to_string(clip)
    try:
      print(translator.translate(ocrString, dest="tr").text)
      print("-----------------------------------------")
      sleep(3)
    except:
      sleep(500/1000)
      continue

if __name__ == "__main__":
  main()
