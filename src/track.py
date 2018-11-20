# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import cv2
import imutils
import time


def undistort(img, K, D, DIM=(1920, 1080), balance=1.0, dim2=None, dim3=None):
    dim1 = img.shape[:2][::-1]  # dim1 is the dimension of input image to un-distort
    assert dim1[0]/dim1[1] == DIM[0]/DIM[1], \
        "Image to undistort needs to have same aspect ratio as the ones used in calibration"
    if not dim2:
        dim2 = dim1
    if not dim3:
        dim3 = dim1
    scaled_K = K * dim1[0] / DIM[0]  # The values of K is to scale with image dimension.
    scaled_K[2][2] = 1.0  # Except that K[2][2] is always 1.0
    # This is how scaled_K, dim2 and balance are used to determine the final K used to un-distort image.
    new_K = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(scaled_K, D, dim2, np.eye(3), balance=balance)
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(scaled_K, D, np.eye(3), new_K, dim3, cv2.CV_16SC2)
    return cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)


def get_x_y(frame):
    # resize the frame, blur it, and convert it to the HSV
    # color space
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    center = None

    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # only proceed if the radius meets a minimum size
        if radius > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
                       (0, 255, 255), 2)
    cv2.circle(frame, center, 5, (0, 0, 255), -1)

    # update the points queue
    pts.appendleft(center)

    # loop over the set of tracked points
    for i in range(1, len(pts)):
        # if either of the tracked points are None, ignore
        #   them
        if pts[i - 1] is None or pts[i] is None:
            continue

        # otherwise, compute the thickness of the line and
        # draw the connecting lines
        thickness = int(np.sqrt(64 / float(i + 1)) * 2.5)
        cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
    return frame, center


if __name__ == "__main__":
    # define the lower and upper boundaries of the "green"
    # ball in the HSV color space, then initialize the
    # list of tracked points
    # greenLower = (29, 86, 6)
    # greenUpper = (64, 255, 255)
    K = np.array([[843.417665466078, 0.0, 890.9156601341177],
                  [0.0, 641.0593481957064, 520.9331642157647],
                  [0.0, 0.0, 1.0]])
    D = np.array([[0.06181130394396002],
                  [-0.11848215592005741],
                  [0.2823759330168743],
                  [-0.17975434137815827]])
    greenLower = (-13, 153, 125)
    greenUpper = (27, 193, 205)
    pts = deque(maxlen=64)

    # if a video path was not supplied, grab the reference
    # to the webcam
    vs = VideoStream(src=0).start()
    # allow the camera or video file to warm up
    time.sleep(2.0)

    # keep looping
    while True:
        # grab the current frame
        frame = vs.read()
        frame_time = time.time()
        # if we are viewing a video and we did not grab a frame,
        # then we have reached the end of the video
        #frame = undistort(frame, K=K, D=D)
        #frame, center = get_x_y(frame)
        # show the frame to our screen
        center = 0 
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        print(center)
        print(frame_time)
        # if the 'q' key is pressed, stop the loop
        if key == ord("q"):
            break
        vs.stop()
    # close all windows
    cv2.destroyAllWindows()
