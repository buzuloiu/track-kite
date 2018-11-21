# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import cv2
import imutils
import time


class Camera(object):
    def __init__(self):
        self.stream = VideoStream(src=0).start()
        self.K = np.array([[843.417665466078, 0.0, 890.9156601341177],
                           [0.0, 641.0593481957064, 520.9331642157647],
                           [0.0, 0.0, 1.0]])
        self.D = np.array([[0.06181130394396002],
                           [-0.11848215592005741],
                           [0.2823759330168743],
                           [-0.17975434137815827]])
        self.pts = deque(maxlen=64)
        self.greenLower = (-13, 153, 125)
        self.greenUpper = (27, 193, 205)

    def move_origin(self, point):
        return (point[1]-540, point[0]-250)


class Frame(object):
    def __init__(self, image):
        self.time = time.time()
        self.center = None
        self.image = image

    def set_center(self, center):
        self.center = center


def undistort(frame, camera, DIM=(1920, 1080), balance=1.0, dim2=None, dim3=None):
    dim1 = frame.image.shape[:2][::-1]  # dim1 is the dimension of input image to un-distort
    assert dim1[0]/dim1[1] == DIM[0]/DIM[1], \
        "Image to undistort needs to have same aspect ratio as the ones used in calibration"
    if not dim2:
        dim2 = dim1
    if not dim3:
        dim3 = dim1
    scaled_K = camera.K * dim1[0] / DIM[0]  # The values of K is to scale with image dimension.
    scaled_K[2][2] = 1.0  # Except that K[2][2] is always 1.0
    # This is how scaled_K, dim2 and balance are used to determine the final K used to un-distort image.
    new_K = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(scaled_K, camera.D, dim2, np.eye(3), balance=balance)
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(scaled_K, camera.D, np.eye(3), new_K, dim3, cv2.CV_16SC2)
    frame.image = cv2.remap(frame.image, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    frame.image = imutils.rotate_bound(frame.image, 270)
    return frame


def get_x_y(frame, camera):
    blurred = cv2.GaussianBlur(frame.image, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # construct a mask for the color "green"
    mask = cv2.inRange(hsv, camera.greenLower, camera.greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

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
        if center:
            frame.set_center(camera.move_origin(center))

        if radius > 10:
            cv2.circle(frame.image, (int(x), int(y)), int(radius),
                       (0, 255, 255), 2)
    cv2.circle(frame.image, center, 5, (0, 0, 255), -1)
    camera.pts.appendleft(center)

    # draw a red line on the frame following the points
    for i in range(1, len(camera.pts)):
        if camera.pts[i - 1] is None or camera.pts[i] is None:
            continue
        thickness = int(np.sqrt(64 / float(i + 1)) * 2.5)
        cv2.line(frame.image, camera.pts[i - 1], camera.pts[i], (0, 0, 255), thickness)
    return frame

# example
if __name__ == "__main__":
    camera = Camera()
    # keep looping
    while True:
        frame = Frame(camera.stream.read())
        frame = get_x_y(frame, camera)
        frame = undistort(frame, camera)
        cv2.imshow("Frame", frame.image)
        key = cv2.waitKey(1) & 0xFF
        print(frame.center)
        print(frame.time)

        # if the 'q' key is pressed, stop the loop
        if key == ord("q"):
            break
    camera.stream.stop()
    cv2.destroyAllWindows()
