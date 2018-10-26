import numpy as np
import cv2

# You should replace these 3 lines with the output in calibration step
DIM = (1920, 1080)
K = np.array([[843.417665466078, 0.0, 890.9156601341177], [0.0, 641.0593481957064, 520.9331642157647], [0.0, 0.0, 1.0]])
D = np.array([[0.06181130394396002], [-0.11848215592005741], [0.2823759330168743], [-0.17975434137815827]])
cap = cv2.VideoCapture(0)
balance = 1.0
dim2 = None
dim3 = None


while(True):
    ret, img = cap.read()
    dim1 = img.shape[:2][::-1]  #dim1 is the dimension of input image to un-distort
    assert dim1[0]/dim1[1] == DIM[0]/DIM[1], "Image to undistort needs to have same aspect ratio as the ones used in calibration"
    if not dim2:
        dim2 = dim1
    if not dim3:
        dim3 = dim1
    scaled_K = K * dim1[0] / DIM[0]  # The values of K is to scale with image dimension.
    scaled_K[2][2] = 1.0  # Except that K[2][2] is always 1.0
    # This is how scaled_K, dim2 and balance are used to determine the final K used to un-distort image. OpenCV document failed to make this clear!
    new_K = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(scaled_K, D, dim2, np.eye(3), balance=balance)
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(scaled_K, D, np.eye(3), new_K, dim3, cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)


    cv2.imshow("undistorted", undistorted_img)
    cv2.imshow('distorted', img)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
