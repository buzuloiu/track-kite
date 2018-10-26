import numpy as np
import cv2

cap = cv2.VideoCapture(0)

npz_calib_file = np.load('calibration_data.npz')
distCoeff = npz_calib_file['distCoeff']
intrinsic_matrix = npz_calib_file['intrinsic_matrix']
npz_calib_file.close()

width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
size = (int(width), int(height))
crop = 1.0

newMat, ROI = cv2.getOptimalNewCameraMatrix(intrinsic_matrix, distCoeff,
                                            imageSize=size, alpha=crop, newImgSize=size,
                                            centerPrincipalPoint=True)
mapx, mapy = cv2.fisheye.initUndistortRectifyMap(intrinsic_matrix, distCoeff, None,
                                         newMat, size=size, m1type=cv2.CV_32FC1)
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here

    gray = cv2.remap(frame, mapx, mapy, cv2.INTER_NEAREST)

    # Display the resulting frame
    cv2.imshow('distorted', frame)
    cv2.imshow('undistorted', gray)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
