import numpy as np
import cv2

from imutils.video import VideoStream
v=VideoStream(1).start()

cv2.startWindowThread()
cv2.namedWindow("video_feed")

while True:
    gray = cv2.cvtColor(v.read(), cv2.COLOR_BGR2GRAY)
    cv2.imshow('video_feed', gray)
    print 'yo'
    if cv2.waitKey(1) == 27:
        break  # esc to quit
