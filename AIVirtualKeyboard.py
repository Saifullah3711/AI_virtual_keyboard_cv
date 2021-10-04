import cv2
from time import sleep
import cvzone
from cvzone.HandTrackingModule import HandDetector


cap = cv2.VideoCapture(0) # from webcam
cap.set(3,1280)
cap.set(4,720)

handTracker = HandDetector(detectionCon=0.8)


class Button_data():
    def __init__(self, pos, text, size=[85,85]):
        self.pos = pos
        self.text = text
        self.size = size


        
all_keys = [
    ["Q","W","E","R","T","Y","U","I","O","P"],
    ["A","S","D","F","G","H","J","K","L",";"],
    ["Z","X","C","V","B","N","M",".",",","/"] ]

all_text1 = ""
all_text2 = ""

# This empty list store the keys with position and sizes
all_button_info = []
for i in range(len(all_keys)):
    for j, key in enumerate(all_keys[i]):
        all_button_info.append(Button_data([100 * j+50, 100 * i + 30],key))
  



def draw_keyboard_on_image(keys_info,img):
    for keys in keys_info:
        x, y = keys.pos
        w, h = keys.size
        cvzone.cornerRect(img, (x,y,w,h),20, rt=0)  # Drawing rectangular border around keys

        cv2.rectangle(img, (x,y),(x+w, y+h),(0, 100, 255),cv2.FILLED)
        cv2.putText(img, keys.text, (x+20, y+65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4 )

    # Space Bar
    cvzone.cornerRect(img, (300,340,500,90),20, rt=0)
    cv2.rectangle(img, (300,340),(800, 430),(0, 100, 255),cv2.FILLED)
    cv2.putText(img, "SPACE BAR", (375,410), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4 )

    # Backspace
    cvzone.cornerRect(img, (1050,30,130,85),20, rt=0)
    cv2.rectangle(img, (1050,30),(1180,115),(0, 100, 255),cv2.FILLED)
    cv2.putText(img, "<--",(1050,95),cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255),4)

    # Enter Button
    cvzone.cornerRect(img, (1050,130,130,85),20, rt=0)
    cv2.rectangle(img, (1050,130),(1180,215),(0, 100, 255),cv2.FILLED)
    cv2.putText(img, "ENT",(1060,190),cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255),4)

    return img

enter_var = 0

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = handTracker.findHands(img)
    lmList, bboxInfo = handTracker.findPosition(img)
    img = draw_keyboard_on_image(all_button_info,img)

    # To Check if Hand is detected or not
    if lmList:
        for keys in all_button_info:
            x, y = keys.pos
            w, h = keys.size
            # If the finger is in the region of text, change the color of button
            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                cv2.rectangle(img, (x,y),(x+w, y+h),(255, 0, 255),cv2.FILLED)
                cv2.putText(img, keys.text, (x+20, y+65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4 )
                # This measure the distance between index 8 and 12 fingers
                # Check out mediapipe documentation for more detail
                # We use it to select or click the button
                l, _, _ = handTracker.findDistance(8,12,img,draw = False)
                if l<35:
                    cv2.rectangle(img, (x,y), (x+w, y+h), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, keys.text, (x+20, y+65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                    if enter_var == 0:
                        all_text1 += keys.text
                        sleep(0.20)
                    else:
                        all_text2 += keys.text
                        sleep(0.20)

            
        # Check for SpaceBar
        if 300 < lmList[8][0] < 800 and 340 < lmList[8][1] < 430:
            cv2.rectangle(img, (300,340),(800, 430),(255, 0, 255),cv2.FILLED)
            cv2.putText(img, "SPACE BAR", (375,410), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4 )

            l, _, _ = handTracker.findDistance(8,12,img,draw = False)
               
            if l<35:

                cv2.rectangle(img, (300,340),(800, 430),(0, 255, 0),cv2.FILLED)
                cv2.putText(img, "SPACE BAR", (375,410), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4 )
                if enter_var == 0:
                    all_text1 += " "
                    sleep(0.20)
                else:
                    all_text2 += " "
                    sleep(0.20)


        # Check for Backspace
        elif 1050 < lmList[8][0] < 1180 and 30 < lmList[8][1] < 115:
            cv2.rectangle(img, (1050,30),(1180,115),(255, 0, 255),cv2.FILLED)
            cv2.putText(img, "<--",(1050,95),cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255),4)

            l, _, _ = handTracker.findDistance(8,12,img,draw = False)
               
            if l<35:

                cv2.rectangle(img, (1050,30),(1180,115),(0, 255, 0),cv2.FILLED)
                cv2.putText(img, "<--", (1050,95), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4 )
                if enter_var == 0:
                    all_text1 = all_text1[:-1]
                    sleep(0.20)
                else:
                    all_text2 = all_text2[:-1]
                    sleep(0.20)

        # Check for enter
        elif 1050 < lmList[8][0] < 1180  and 130 < lmList[8][1] < 215: 
            cv2.rectangle(img, (1050,130),(1180,215),(255, 0, 255),cv2.FILLED)
            cv2.putText(img, "ENT",(1060,190),cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255),4)
            
            l, _, _ = handTracker.findDistance(8,12,img,draw = False)
               
            if l<35:

                cv2.rectangle(img, (1050,130),(1180,215),(0, 255, 0),cv2.FILLED)
                cv2.putText(img, "ENT",(1060,190),cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255),4)
            
                enter_var += 1 
                sleep(0.20)





    if enter_var==0:
        cv2.rectangle(img, (50,450), (700,530), (255, 25, 0), cv2.FILLED)
        cv2.putText(img, all_text1, (60,520), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

    else:
        cv2.rectangle(img, (50,450), (700,530), (255, 25, 0), cv2.FILLED)
        cv2.putText(img, all_text1, (60,520), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

        cv2.rectangle(img, (50,550), (700,630), (255, 25, 0), cv2.FILLED)
        cv2.putText(img, all_text2, (60,610), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)







    cv2.imshow("AI-Keyboard",img)
    cv2.waitKey(1)
