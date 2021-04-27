import cv2
import numpy as np
import time
import PoseModule as pm

cap = cv2.VideoCapture('PoseVideos/1.mp4')
detector = pm.poseDetector()
count = 0
dir = 0
pTime = 0

while True:

    success, img = cap.read()
    height, width, layers = img.shape
    new_h = int(height/2)
    new_w = int(width/2)
    img = cv2.resize(img, (new_w, new_h))

    #img = cv2.imread('PoseVideos/test.jpg')
    img = detector.findPose(img, False)

    lmList = detector.findPosition(img, False)
    if len(lmList) != 0:
        #angle = detector.findAngle(img, 12, 14, 16)
        angle = detector.findAngle(img, 11, 13, 15)

        per = np.interp(angle, (210, 310), (0, 100))

        if per == 100:
            if dir == 0:
                count += 0.5
                dir = 1
        if per == 0:
            if dir == 1:
                count += 0.5
                dir = 0

        cv2.rectangle(img, (0, new_h), (180, new_h - 180), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (0, new_h), cv2.FONT_HERSHEY_PLAIN, 15, (255, 0, 0), 25)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)

    cv2.imshow("Image", img)
    cv2.waitKey(1)