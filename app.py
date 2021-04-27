import cv2
import numpy as np
import time
import PoseModule as pm
import winsound

def main():
    cap = cv2.VideoCapture('PoseVideos/1.mp4')
    #cap = cv2.VideoCapture(0)

    detector = pm.poseDetector()
    count = 0
    dir = 0
    pTime = 0

    foul_count = 0
    prev_per = -1

    while True:

        success, img = cap.read()
        height, width, layers = img.shape
        new_h = int(height/2)
        new_w = int(width/2)
        img = cv2.resize(img, (new_w, new_h))

        #img = cv2.imread('PoseVideos/test.jpg')
        img = detector.findPose(img)

        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            #angle = detector.findAngle(img, 12, 14, 16)
            angle = detector.findAngle(img, 11, 13, 15)

            per = np.interp(angle, (210, 310), (0, 100))
            bar = np.interp(angle, (210, 310), (new_h - 20, 50))

            frequency = 2500  # Set Frequency To 2500 Hertz
            duration = 1000  # Set Duration To 1000 ms == 1 second
            if dir == 0:
                if per < prev_per:
                    foul_count += 1
                    #winsound.Beep(frequency, duration)
            else:
                if per > prev_per:
                    foul_count += 1
                    #winsound.Beep(frequency, duration)

            prev_per = per

            color = (0, 0, 255)
            if per == 100:
                color = (0, 255, 0)
                if dir == 0:
                    count += 0.5
                    dir = 1
            if per == 0:
                color = (0, 255, 0)
                if dir == 1:
                    count += 0.5
                    dir = 0

            if new_h > new_w:
                marker = new_w
            else:
                marker = new_h

            marker2 = 40
            #bar check
            cv2.rectangle(img, (new_w - marker2, 50), (new_w - marker2 + int(marker/20), new_h - 20), color, 1)
            cv2.rectangle(img, (new_w - marker2,  int(bar)), (new_w - marker2 + int(marker/20), new_h - 20), color, cv2.FILLED)
            cv2.putText(img, f'{int(per)}%', (new_w - 40, 40), cv2.FONT_HERSHEY_PLAIN, 1, color, 1)


            #count
            #cv2.rectangle(img, (20, new_h - 20), (20 + int(marker/6), new_h - 20 - int(marker/6)), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, str(int(count)), (10, new_h - 10), cv2.FONT_HERSHEY_PLAIN, marker/80, (255, 255, 255), 1)
            cv2.putText(img, str(int(foul_count)), (100, new_h - 10), cv2.FONT_HERSHEY_PLAIN, marker/80, (255, 255, 255), 1)
            cv2.putText(img, str(int(dir)), (200, new_h - 10), cv2.FONT_HERSHEY_PLAIN, marker/80, (255, 255, 255), 1)

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(img, f'{int(fps)}fps', (10, 40), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)

        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()