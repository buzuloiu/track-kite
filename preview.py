import numpy as np
import cv2

cap = cv2.VideoCapture("5.mp4")

npz_calib_file = np.load('calibration_data.npz')
distCoeff = npz_calib_file['distCoeff']
intrinsic_matrix = npz_calib_file['intrinsic_matrix']
npz_calib_file.close()

width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
size = (int(width), int(height))
crop = 1
newMat, ROI = cv2.getOptimalNewCameraMatrix(intrinsic_matrix, distCoeff, size, alpha=crop, centerPrincipalPoint=1)
mapx, mapy = cv2.initUndistortRectifyMap(intrinsic_matrix, distCoeff, None, newMat, size, m1type=cv2.CV_32FC1)
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here

    gray = cv2.remap(frame, mapx, mapy, cv2.INTER_LINEAR)

    # Display the resulting frame
    cv2.imshow('frame',frame)
    cv2.imshow('gray',gray)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
