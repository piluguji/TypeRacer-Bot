from typing import Text, final
import cv2
import pyautogui
import time
import pytesseract
from PIL import ImageGrab, Image
import numpy as np
from pytesseract.pytesseract import main
from textblob import TextBlob

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def fixText(text, spellCheck = True):
    text = text.replace("\n", " ")
    text = text.replace("|", "I")
    text = text.replace("1", "I")
    text = text.replace("[", "T")

    text = text.replace("0", " o")
    text = text.replace("  ", " ")

    if spellCheck:
        c = TextBlob(text)
        text = c.correct()

    return text

def captcha():
    up = pyautogui.locateOnScreen('CaptchaTop.png', confidence = 0.7)
    bottom = pyautogui.locateOnScreen('CaptchaBottom.png', confidence = 0.7)

    img = np.array(ImageGrab.grab(bbox= (up[0] + 30, up[1] + up[3], bottom[0] + bottom[2], bottom[1])))
    cv2.imwrite('captcha.png', img)

    #Turns black streaks into white streaks
    for r in range(1, len(img) - 1):
        for c in range(1, len(img[r]) - 1):
            isBlack = True
            Currentpixel = img[r][c]

            #finds if pixel is close to being black 
            for p in Currentpixel:
                if p > 50:
                    isBlack = False
                    break
            
            #Turning pixel white if its black
            if isBlack:
                for i in range(-1, 1 + 1):
                    for j in range(-1, 1 + 1):
                        img[r + i][c + j] = np.array([255,255,255])                    

    #Thresholding so text is black and the rest is white
    ret, thresh = cv2.threshold(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 155, 255, cv2.THRESH_BINARY)
    thresh = cv2.GaussianBlur(thresh, (5, 5), 0)
    cv2.imwrite('captcha-final.png', thresh)

    text =  fixText(str(pytesseract.image_to_string(thresh)))
    print(text)
    time.sleep(0.5)
    pyautogui.typewrite(text, interval=0)

    
def race():
    up = pyautogui.locateOnScreen('topEdge.png', confidence = 0.85)

    try:
        bottom = pyautogui.locateOnScreen('bottomEdge.png', confidence = 0.7)
    except:
        bottom = pyautogui.locateOnScreen('bottomEdge2.png', confidence = 0.7)

    print(up is None, bottom is None)

    img = ImageGrab.grab(bbox= (up[0] + 30, up[1] + up[3], bottom[0] + bottom[2], bottom[1]))
    img.save('text.png')

    text =  fixText(str(pytesseract.image_to_string(img)), False)

    print(text)

    time.sleep(5)
    text = text[0].upper() + text[1:]
    pyautogui.typewrite(text, interval=0.02)

def main():
    race() 
    #captcha()

if __name__ == "__main__":
    main()
