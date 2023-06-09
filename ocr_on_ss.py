import pyscreenshot
import pytesseract
import pyautogui
import cv2 
from time import sleep
from  pynput import keyboard

pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract"

X1, Y1 = 0, 0
ocrString = ""

def onRelease(key):

  global X1, Y1
  global ocrString

  if key == keyboard.Key.shift:
    X2, Y2 = pyautogui.position()

    try:
      # Ekran görüntüsünü al
      pyscreenshot.grab(bbox=(X1, Y1, X2, Y2)).save("clip.jpg")

      # Ekran görüntüsünü oku
      image = cv2.imread("clip.jpg")

      # Görüntüyü büyüt
      resized = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

      # Ekran görüntüsünü gri tonlamaya dönüştür
      gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

      # Arka planın ortalama yoğunluğunu hesapla
      mean_intensity = cv2.mean(gray)[0]

      # Arka planın karanlık temalı olup olmadığını kontrol et
      if mean_intensity < 127:
          # Arka plan açık temalı, görüntüyü ters çevir
          inverted = cv2.bitwise_not(gray)
      else:
          # Arka plan karanlık temalı, ters çevirme işlemi yapma
          inverted = gray

      # Gürültüyü azaltmak için görüntüyü bulanıklaştır
      blur = cv2.GaussianBlur(inverted, (3, 3), 0)

      # Adaptive threshold uygula
      thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 15, 15)

      # Dil işlemleri ile karakterleri birleştir
      kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
      dilation = cv2.dilate(thresh, kernel, iterations=1)
      closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel, iterations=1)

      # İşlenmiş ekran görüntüsünü kaydet
      cv2.imwrite("output.jpg", closing)
    except ValueError:
      print("Alan seciminde hata, tekrar alan seciniz.")
      print("-----------------------------------------")

def onPress(key):

  global X1, Y1
  global ocrString

  try:
      charKey = key.char
  except:
      charKey = None

  if key == keyboard.Key.shift:
    X1, Y1 = pyautogui.position()
  
  elif charKey in ["y", "Y"]:

    # Çıktı düzenleme
    # ocrString = ocrString.replace("-\n", "")
    # ocrString = ocrString.replace("\n", " ")
    # ocrString = ocrString.replace(".", ".\n")

    try:
        print(ocrString)
        print("-----------------------------------------")
    except:
      print("OCR yapilamadi!!!")
    
  elif charKey in ["o", "O"]:
    # Ekran görüntüsünü oku
    ocrImage = cv2.imread("output.jpg")

    # Tesseract OCR kullanarak görüntüden metni al
    custom_config1 = r'--oem 3 --psm 6'
    custom_config2 = r'--oem 2 --psm 4'
    ocrString = pytesseract.image_to_string(ocrImage, config=custom_config1)
     


keyboard.Listener(on_press=onPress, on_release=onRelease).start()

while True:
  sleep(3)
