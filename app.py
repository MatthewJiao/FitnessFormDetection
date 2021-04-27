import cv2
import numpy as np
import time
import PoseModule as pm

cap = cv2.VideoCapture('PoseVideos/1.mp4')
detector = pm.poseDetector()


while True:

    success, img = cap.read()
    height, width, layers = img.shape
    new_h = int(height / 2)
    new_w = int(width / 2)
    img = cv2.resize(img, (new_w, new_h))

    #img = cv2.imread('PoseVideos/test.jpg')
    img = detector.findPose(img, False)

    lmList = detector.findPosition(img, False)
    if len(lmList) != 0:
        detector.findAngle(img, 12, 14, 16)

    cv2.imshow("Image", img)
    cv2.waitKey(1)