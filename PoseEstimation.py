import cv2

cap = cv2.VideoCapture("PoseVideos/1.mp4")


while True:
    success, image = cap.read()
    height, width, layers = image.shape
    new_h = int(height / 2)
    new_w = int(width / 2)
    resize = cv2.resize(image, (new_w, new_h))
    cv2.imshow("Image", resize)
    cv2.waitKey(1)
