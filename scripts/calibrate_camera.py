import numpy as np
import glob
import sys
import cv2
assert cv2.__version__[0] == '3', 'The fisheye module requires opencv version >= 3.0.0'


def ImageProcessing(_img_shape):
    images = glob.glob('calibration_images/*.png')
    for fname in images:
        img = cv2.imread(fname)
        if _img_shape is None:
            _img_shape = img.shape[:2]
        else:
            assert _img_shape == img.shape[:2], "All images must share the same size."
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD,
                                                 cv2.CALIB_CB_ADAPTIVE_THRESH+cv2.CALIB_CB_FAST_CHECK
                                                 + cv2.CALIB_CB_NORMALIZE_IMAGE)
        # If found, add object points, image points (after refining them)
        if ret:
            objpoints.append(objp)
            cv2.cornerSubPix(gray, corners, (3, 3), (-1, -1), subpix_criteria)
            imgpoints.append(corners)
    N_OK = len(objpoints)
    K = np.zeros((3, 3))
    D = np.zeros((4, 1))
    rvecs = [np.zeros((1, 1, 3), dtype=np.float64) for i in range(N_OK)]
    tvecs = [np.zeros((1, 1, 3), dtype=np.float64) for i in range(N_OK)]
    rms, _, _, _, _ = \
        cv2.fisheye.calibrate(
            objpoints,
            imgpoints,
            gray.shape[::-1],
            K,
            D,
            rvecs,
            tvecs,
            calibration_flags,
            (cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER, 30, 1e-6)
        )
    print("Found " + str(N_OK) + " valid images for calibration")
    print("DIM=" + str(_img_shape[::-1]))
    print("K=np.array(" + str(K.tolist()) + ")")
    print("D=np.array(" + str(D.tolist()) + ")")


def ImageCollect(filename, n_boards):
    # Collect Calibration Images
    print('-----------------------------------------------------------------')
    print('Loading video...')

    # Load the file given to the function
    video = cv2.VideoCapture(filename)
    # Checks to see if a the video was properly imported
    status = video.isOpened()

    if status is True:

        # Collect metadata about the file.
        FPS = video.get(cv2.CAP_PROP_FPS)
        FrameDuration = 1/(FPS/1000)
        total_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)

        # Initializes the frame counter and collected_image counter
        current_frame = 0
        collected_images = 0

        # Video loop.  Press spacebar to collect images.  ESC terminates the function.
        while current_frame < total_frames:
            success, image = video.read()
            current_frame = video.get(cv2.CAP_PROP_POS_FRAMES)
            cv2.imshow('Video', image)
            k = cv2.waitKey(int(FrameDuration))  # You can change the playback speed here
            if collected_images == n_boards:
                break
            if k == 32:
                collected_images += 1
                cv2.imwrite('calibration_images/calibration_image' + str(collected_images) + '.png', image)
                print(str(collected_images) + ' images collected.')
            if k == 27:
                break

        # Clean up
        video.release()
        cv2.destroyAllWindows()
    else:
        print('Error: Could not load video')
        sys.exit()


if __name__ == "__main__":
    CHECKERBOARD = (6, 9)
    n_boards = 20
    subpix_criteria = (cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER, 30, 0.1)
    calibration_flags = cv2.fisheye.CALIB_RECOMPUTE_EXTRINSIC+cv2.fisheye.CALIB_CHECK_COND+cv2.fisheye.CALIB_FIX_SKEW
    objp = np.zeros((1, CHECKERBOARD[0]*CHECKERBOARD[1], 3), np.float32)
    objp[0, :, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
    _img_shape = None
    objpoints = []  # 3d point in real world space
    imgpoints = []  # 2d points in image plane.
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "calibrate.mp4"

    print("Starting camera calibration....")
    print("Step 1: Image Collection")
    print("We will playback the calibration video.  Press the spacebar to save")
    print("calibration images.")
    print(" ")
    print('We will collect ' + str(n_boards) + ' calibration images.')
    ImageCollect(filename, n_boards)
    print("Calibration images collected, starting analysis")
    ImageProcessing(_img_shape)
