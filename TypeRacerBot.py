from typing import final
import cv2
import pyautogui
import time
import pytesseract
from PIL import ImageGrab, Image
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def fixText(text):
    text = text.replace("\n", " ")
    text = text.replace("|", "I")
    text = text.replace("1", "I")
    text = text.replace("[", "T")

    text = text.replace("0", " o")
    text = text.replace("  ", " ")

    return text

def captcha():
    up = pyautogui.locateOnScreen('CaptchaTop.png', confidence = 0.7)
    bottom = pyautogui.locateOnScreen('CaptchaBottom.png', confidence = 0.7)

    img = np.array(ImageGrab.grab(bbox= (up[0], up[1] + up[3], bottom[0] + bottom[2], bottom[1])))
    cv2.imwrite('captcha.png', img)

    #img = cv2.imread('captcha.png')

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

                '''above = img[r][c + 2]
                isLetter = True
                for p in above:
                    if p < 40 or p > 160:
                        isLetter = False
                        break
                
                #Turning pixel white if its black
                if isLetter:
                    for i in range(-1, 1 + 1):
                        for j in range(-1, 1 + 1):
                            img[r + i][c + j] = np.array([60,60,60])

                below = img[r][c - 2]
                isLetter = True
                for p in below:
                    if p < 40 or p > 160:
                        isLetter = False
                        break
                
                #Turning pixel white if its black
                if isLetter:
                    for i in range(-1, 1 + 1):
                        for j in range(-1, 1 + 1):
                            img[r + i][c + j] = np.array([0,0,0])'''

    cv2.imwrite('captcha-inter1.png', img)
                        

    cv2.imwrite('captcha-inter2.png', img)


    #Thresholding so text is black and the rest is white
    ret, thresh = cv2.threshold(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 155, 255, cv2.THRESH_BINARY)
    cv2.imwrite('captcha-final.png', thresh)

    text =  fixText(str(pytesseract.image_to_string(thresh)))
    print(text)
    time.sleep(2)
    pyautogui.typewrite(text, interval=0.03)

    
def race():
    up = pyautogui.locateOnScreen('topEdge.png', confidence = 0.9)

    try:
        bottom = pyautogui.locateOnScreen('bottomEdge.png', confidence = 0.9)
    except:
        bottom = pyautogui.locateOnScreen('bottomEdge2.png', confidence = 0.9)

    img = ImageGrab.grab(bbox= (up[0] + 30, up[1] + up[3], bottom[0] + bottom[2], bottom[1]))
    img.save('text.png')

    text =  fixText(str(pytesseract.image_to_string(img)))

    time.sleep(5)
    pyautogui.typewrite(text, interval=0.03)

#race()
captcha()




