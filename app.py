from flask import Flask, render_template, Response

import cv2
import numpy as np
import PoseModule as pm
import time
import winsound

app = Flask(__name__)

camera = cv2.VideoCapture(0)

def gen_frames():
    detector = pm.poseDetector()
    count = 0
    dirRight = 0
    dirLeft = 0
    pTime = 0

    foul_count = 0
    prev_per = -1
    perListLeft = []
    perListRight = []
    while True:
        success, img = camera.read()
        height, width, layers = img.shape
        new_h = int(height)
        new_w = int(width)
        img = cv2.resize(img, (new_w, new_h))

        #img = cv2.imread('PoseVideos/test.jpg')
        img = detector.findPose(img)

        lmList, visibilityList = detector.findPosition(img)
        if len(lmList) != 0:
            angleLeft = detector.findAngle(img, 11, 13, 15)
            angleRight = detector.findAngle(img, 12, 14, 16)

            perLeft = np.interp(angleLeft, (220, 300), (0, 100))
            perRight = np.interp(angleRight, (220, 300), (0, 100))
            # print("right", perRight, visibilityList[16][1])
            print("left", perLeft, visibilityList[13])

            perListLeft.append(perLeft)
            perListRight.append(perRight)

            # bar = np.interp(angleLeft, (210, 320), (new_h - 20, 50))

            frequency = 2500  # Set Frequency To 2500 Hertz
            duration = 1000  # Set Duration To 1000 ms == 1 second
            s_frequency = 3000
            s_duration = 200
            adj = 2
            vis_fac = 0.9
            if len(perListLeft) >= 4:
                if dirLeft == 0:
                    if (visibilityList[11][1] > vis_fac and visibilityList[13][1] > vis_fac and visibilityList[15][
                        1] > vis_fac):
                        if perLeft < perListLeft[len(perListLeft) - adj] and perListLeft[len(perListLeft) - 2] < \
                                perListLeft[len(perListLeft) - adj - 1] \
                                and perListLeft[len(perListLeft) - 3] < perListLeft[len(perListLeft) - adj - 2]:
                            winsound.Beep(frequency, duration)
                            dirLeft = 1
                else:
                    if (visibilityList[11][1] > vis_fac and visibilityList[13][1] > vis_fac and visibilityList[15][
                        1] > vis_fac):
                        if perLeft > perListLeft[len(perListLeft) - adj] and perListLeft[len(perListLeft) - 2] > \
                                perListLeft[len(perListLeft) - adj - 1] \
                                and perListLeft[len(perListLeft) - 3] > perListLeft[len(perListLeft) - adj - 2]:
                            winsound.Beep(frequency, duration)
                            dirLeft = 0

            if len(perListRight) >= adj:
                if dirRight == 0:
                    if (visibilityList[12][1] > vis_fac and visibilityList[14][1] > vis_fac and visibilityList[16][
                        1] > vis_fac):
                        if perRight < perListRight[len(perListRight) - adj]:
                            foul_count += 1
                            winsound.Beep(frequency, duration)
                            dirRight = 1
                else:
                    if (visibilityList[12][1] > vis_fac and visibilityList[14][1] > vis_fac and visibilityList[16][
                        1] > vis_fac):
                        if perRight > perListRight[len(perListRight) - adj]:
                            foul_count += 1
                            winsound.Beep(frequency, duration)
                            dirRight = 0

            color = (0, 0, 255)
            if perLeft == 100:
                color = (0, 255, 0)
                if dirLeft == 0:
                    count += 0.5
                    dirLeft = 1
                    winsound.Beep(s_frequency, s_duration)

            if perLeft == 0:
                color = (0, 255, 0)
                if dirLeft == 1:
                    count += 0.5
                    dirLeft = 0

            if perRight == 100:
                if dirRight == 0:
                    count += 0.5
                    dirRight = 1
                    winsound.Beep(s_frequency, s_duration)

            if perRight == 0:
                if dirRight == 1:
                    count += 0.5
                    dirRight = 0

            if new_h > new_w:
                marker = new_w
            else:
                marker = new_h

            marker2 = 40
            # bar check
            # cv2.rectangle(img, (new_w - marker2, 50), (new_w - marker2 + int(marker/20), new_h - 20), color, 1)
            # cv2.rectangle(img, (new_w - marker2,  int(bar)), (new_w - marker2 + int(marker/20), new_h - 20), color, cv2.FILLED)
            # cv2.putText(img, f'{int(perLeft)}%', (new_w - 40, 40), cv2.FONT_HERSHEY_PLAIN, 1, color, 1)

            # count
            # cv2.rectangle(img, (20, new_h - 20), (20 + int(marker/6), new_h - 20 - int(marker/6)), (0, 255, 0), cv2.FILLED)
            # adjusted_count = int(foul_count / 5)
            # cv2.putText(img, str(int(foul_count)), (100, new_h - 10), cv2.FONT_HERSHEY_PLAIN, marker/80, (255, 255, 255), 1)
            # cv2.putText(img, str(int(dir)), (200, new_h - 10), cv2.FONT_HERSHEY_PLAIN, marker/80, (255, 255, 255), 1)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, f'{int(fps)}fps', (10, 40), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)

        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', img)
            img = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')  # concat frame one by one and show result


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)
