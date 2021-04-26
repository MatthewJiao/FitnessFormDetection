import cv2
import time
cap = cv2.VideoCapture("PoseVideos/1.mp4")
pTime = 0

while True:
    success, img = cap.read()
    height, width, layers = img.shape
    new_h = int(height / 2)
    new_w = int(width / 2)
    img = cv2.resize(img, (new_w, new_h))

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv2.imshow("Image", img)

    cv2.waitKey(1)
