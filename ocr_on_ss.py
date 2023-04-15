import pyscreenshot
import pytesseract
import pyautogui
import cv2 
from time import sleep
from  pynput import keyboard

pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract"

X1, Y1, X2, Y2 = 0, 0, 1, 1
tempX1, tempY1, tempX2, tempY2 = 0, 0, 0, 0

def onRelease(key):

  global tempX2, tempY2

  if key == keyboard.Key.shift:
    tempX2, tempY2 = pyautogui.position()

def onPress(key):

  global X1, Y1, X2, Y2
  global tempX1, tempY1, tempX2, tempY2

  try:
      charKey = key.char
  except:
      charKey = None

  if key == keyboard.Key.shift:
    tempX1, tempY1 = pyautogui.position()
  elif charKey in ["y", "Y"]:
    X1, Y1, X2, Y2 = tempX1, tempY1, tempX2, tempY2

    try:
      # Ekran görüntüsünü al
      pyscreenshot.grab(bbox=(X1, Y1, X2, Y2)).save("clip.jpg")

      # Ekran görüntüsünü oku
      image = cv2.imread("clip.jpg")

      # Görüntüyü %200 oranında büyüt
      resized = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

      # Ekran görüntüsünü gri tonlamaya dönüştür
      gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

      # Gürültüyü azaltmak için görüntüyü bulanıklaştır
      blur = cv2.GaussianBlur(gray, (3, 3), 0)

      # Adaptive threshold uygula
      thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 15, 15)

      # Dil işlemleri ile karakterleri birleştir
      kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
      dilation = cv2.dilate(thresh, kernel, iterations=1)
      closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel, iterations=1)

      # İşlenmiş ekran görüntüsünü kaydet
      cv2.imwrite("output.jpg", closing)

      # Tesseract OCR kullanarak görüntüden metni al
      custom_config = r'--oem 3 --psm 6'
      ocrString = pytesseract.image_to_string(closing, config=custom_config)

      # Çıktı düzenleme
      # ocrString = ocrString.replace("-\n", "")
      # ocrString = ocrString.replace("\n", " ")
      # ocrString = ocrString.replace(".", ".\n")

      try:
        result = ""
        if("_" in ocrString):
          result += "Aşağıdaki '_' olan yere ne gelmelidir?\n"
        else:
          result += "Aşağıdaki soruyu yanıtlar mısın?\n"
        result += '"' + ocrString + '"'

        print(result)
        print("-----------------------------------------")

      except:
        pass
    except ValueError:
      print("Alan seciminde hata, tekrar alan seciniz.")
      print("-----------------------------------------")


keyboard.Listener(on_press=onPress, on_release=onRelease).start()

while True:
  sleep(3)
