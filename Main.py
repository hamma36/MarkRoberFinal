import RPi.GPIO as GPIO
import time
from pydub import AudioSegment
from pydub.playback import play
import cv2
import os
from PIL import Image
import pytesseract
import chardet
from gtts import gTTS
from random import *
import math
import operator


# Start Variables
run = False
# End Variables

# Setup Start
GPIO.setmode(GPIO.BCM)

GPIO_SENSOR = 18

GPIO.setup(GPIO_SENSOR, GPIO.IN)
# Setup End

def GetText():
    img = Image.open("capture.jpg")
    #imgBW = img.convert('1')
    #text = pytesseract.image_to_string(img, config='-l eng --oem 3 --psm 12')
    text = pytesseract.image_to_data(img, config='-l eng --oem 3 --psm 12')
    #print(text)

    print(pytesseract.image_to_string(Image.open("capture.jpg")))


def SensorInput():
    sensorValue = GPIO.input(GPIO_SENSOR)
    # print(sensorValue)

    return sensorValue;


def ReadImage():
    image = cv2.imread('capture.jpg')

    #while True:
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    return image


def TakePhoto():
    cap = cv2.VideoCapture(0)

    while (True):
        ret, frame = cap.read()
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

        cv2.imshow('frame', rgb)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            out = cv2.imwrite('capture.jpg', frame)
            shutter = AudioSegment.from_wav("shutter.wav")
            play(shutter)
            print("\n\n")
            break

    cap.release()
    cv2.destroyAllWindows()


def DeleteCapture():
    while True:
        print("Deleting last captured file: ")
        cont = input("Continue Y/N:")
        cont = cont.lower()
        if cont == "n":
            print("Canceled\n\n")
            break
        elif cont == "y":
            print("Deleting...")
            os.remove("capture.jpg")
            print("Capture Deleted\n\n")
            break
        else:
            print("Invalid input\n")


def TextToSpeach(text, speed):
    readText = text
    language = 'en'
    if speed == 0:
        myobj = gTTS(text=readText, lang=language, slow=False)

    elif speed == 1:
        myobj = gTTS(text=readText, lang=language, slow=True)

    else:
        myobj = gTTS(text=readText, lang=language, slow=False)

    myobj.save("savedText.mp3")

    readText = AudioSegment.from_mp3("savedText.mp3")
    play(readText)
    return


def Math():

    num = []
    opp = []
    operatorsTextWords = ["plus", "minus", "times", "divided by"]
    operatorsText = ["+", "-", "*", "/"]

    operators = {
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: a / b,
    }

    textV = []
    answer = 0
    notComplete = True

    for x in range(4):
        n = randint(1, 100)
        num.append(n)

        o = randint(0, 3)
        opp.append(o)

        text = f"{num[x]} {operatorsTextWords[opp[x]]}"
        textV.append(text)


    nExtra = randint(1,100)
    num.append(nExtra)
    text = f"{nExtra} equals"
    textV.append(text)

    for x in range(5):
        
        if x == 0:
            answer = num[x]

            #print(answer)
        
        elif x == 25:
            n = num[x]
    
            o = opp[x]
    
            o = operatorsText[o]
    
            print(o)
    
            answer = operators[o](answer, n)
    
            print(answer)

        elif x != 0:
            n = num[x]
            x = x-1
            o1 = opp[x]
            o = operatorsText[o1]
            print(f"{o}\n")

            answer = operators[o](answer, n)
            print(answer)



    textN = f"{textV[0]} {textV[1]} {textV[2]} {textV[3]} {textV[4]}"

    print(textN)
    print(answer)

    answer = round(answer, 2)
    print(answer)

    TextToSpeach(textN, 1)
    TextToSpeach("R to Repeat", 0)
    TextToSpeach("E to Continue with Answer", 0)

    while notComplete:
        menu = input()
        if menu.lower() == "r":
            TextToSpeach(textN, 1)
        elif menu.lower() == "e":
            TextToSpeach("Type Your answer to 2 decimal place", 0)

            userResponse = input()
            userResponse = float(userResponse)
            userResponse = round(userResponse, 2)

            if userResponse == answer:
                TextToSpeach("That is Correct!", 0)
                notComplete = False

            elif userResponse != answer:
                TextToSpeach("That is incorrect", 0)

    TextToSpeach("Complete, You May Return to the computer", 0)






if __name__ == '__main__':
    try:
        while True:
            print("Menu:")
            print("start to start")
            print("capture to take an image")
            print("read to read image")
            print("delete to delete last image")
            print("text to get text from image")

            print("quit to stop program")
            uInput = input("Your Input: ")
            uInput = uInput.lower()
            if uInput == "start":
                #alarm = AudioSegment.from_wav("alarm.wav")
                #play(alarm)
                text = "Press enter to continue"
                TextToSpeach(text, 0)
                run = True
                while run:
                    if input() == "":
                        print("succes")

                        Math()
                        run = False

                    else:
                        text = "Press enter to continue"
                        TextToSpeach(text)





            elif uInput == "read":
                while True:
                    image = ReadImage()
                    cv2.imshow('image', image)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        print("\n\n")
                        break
                cv2.destroyAllWindows()

            elif uInput == "capture":
                TakePhoto()

            elif uInput == "delete":
                DeleteCapture()

            elif uInput == "text":
                GetText()

            elif uInput == "quit":
                quit()

            else:
                print("Invalid")
                error = AudioSegment.from_wav("error.wav")
                play(error)

    except KeyboardInterrupt:
        print("\nEnded By User")
        GPIO.cleanup()
