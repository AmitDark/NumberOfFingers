import cv2
import time
import os
import handtrackingMin as htm
import webbrowser

timeout = time.time() + 20

res = []

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

folderPath = "Finger numbers"
myList = os.listdir(folderPath)
print(myList)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    # print(f'{folderPath}/{imPath}')
    overlayList.append(image)

print(len(overlayList))
pTime = 0

detector = htm.handDetector(detectionCon=0.75)

tipIds = [4, 8, 12, 16, 20]

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    # print(lmList)

    if len(lmList) != 0:
        fingers = []

        # Thumb
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # 4 Fingers
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        # print(fingers)
        totalFingers = fingers.count(1)
        ##print(totalFingers)

        h, w, c = overlayList[totalFingers - 1].shape
        img[0:h, 0:w] = overlayList[totalFingers - 1]

        res.append(totalFingers)


        def most_frequent(List):
            counter = 0
            num = List[0]

            for i in List:
                curr_frequency = List.count(i)
                if (curr_frequency > counter):
                    counter = curr_frequency
                    num = i

            return num


        if timeout < time.time():
            if most_frequent(res) == 1:
                webbrowser.open('http://youtube.com')
                cv2.destroyWindow("img")

            if most_frequent(res) == 2:
                webbrowser.open('http://google.com')
                cv2.destroyWindow("img")

            if most_frequent(res) == 3:
                webbrowser.open('https://youtube.com/playlist?list=PLIafxHRSL6qiPFJEyz1H7m3sDZ4u0fcsA')
                cv2.destroyWindow("img")

            if most_frequent(res) == 4:
                webbrowser.open('http://amazon.in')
                cv2.destroyWindow("img")

            if most_frequent(res) == 5:
                webbrowser.open('https://news.google.com/')
                cv2.destroyWindow("img")

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN,
                3, (255, 0, 0), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)





