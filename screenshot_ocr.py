import pyscreenshot
import pytesseract
import pyautogui
import cv2 
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract"

class ScreenshotOCR:
    def __init__(self):
        self._X1, self._Y1 = 0, 0
        self.ocrString = ""
        self._processedImage = np.zeros([100,100,3],dtype=np.uint8)
        self._clip = np.zeros([100,100,3],dtype=np.uint8)

        self._clip.fill(255)
        self._processedImage.fill(255)

    def first_corner_process(self):
        self._X1, self._Y1 = pyautogui.position()

    def second_corner_process(self):
        self._X2, self._Y2 = pyautogui.position()

        try:
            # Ekran görüntüsünü al
            self._clip = np.array(pyscreenshot.grab(bbox=(self._X1, self._Y1, self._X2, self._Y2))) 

            # Görüntüyü işle
            self.process_image()
        except ValueError:
            print("Alan seciminde hata, tekrar alan seciniz.")
            print("-----------------------------------------")

    def print_ocr(self):
      # Çıktı düzenleme
      # ocrString = ocrString.replace("-\n", "")
      # ocrString = ocrString.replace("\n", " ")
      # ocrString = ocrString.replace(".", ".\n")

      try:
        print(self.ocrString)
        print("-----------------------------------------")
      except:
        print("OCR yapilamadi!!!")

    def perform_ocr(self):
        # Tesseract OCR kullanarak görüntüden metni al
        custom_config = r'--oem 3 --psm 6'
        # custom_config = r'--oem 2 --psm 4'
        self.ocrString = pytesseract.image_to_string(self._processedImage, config=custom_config)
        # self.ocrString = pytesseract.image_to_string(ocrImage)

        self.print_ocr()

    def process_image(self):
        try:
            # Ekran görüntüsünü oku
            image = self._clip

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
            self._processedImage = np.array(closing)
            cv2.imwrite("output.jpg", closing)
        except ValueError:
            print("Alan seçiminde hata, tekrar alan seçiniz.")
            print("-----------------------------------------")

    def process_f(self):
        self.first_corner_process()

    def process_s(self):
        self.second_corner_process()

    def process_o(self):
        self.perform_ocr()

    def process_p(self):
        self.print_ocr()


# if __name__ == "__main__":
#     ocr = ScreenshotOCR()
#     ocr.run()
