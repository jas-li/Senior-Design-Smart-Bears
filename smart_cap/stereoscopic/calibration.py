import cv2
import numpy as np
import glob

# Chessboard parameters
chessboard_size = (10, 7)
square_size = 0.025  # meters

# Termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Prepare object points
objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)
objp *= square_size

# Arrays to store object points and image points from all images
objpoints = []  # 3D points in real world space
imgpoints_left = []  # 2D points in left image plane
imgpoints_right = []  # 2D points in right image plane

# Get list of calibration images
left_images = glob.glob('../../left/*.jpg')
right_images = glob.glob('../../right/*.jpg')

for left_img, right_img in zip(left_images, right_images):
    img_left = cv2.imread(left_img)
    img_right = cv2.imread(right_img)
    gray_left = cv2.cvtColor(img_left, cv2.COLOR_BGR2GRAY)
    gray_right = cv2.cvtColor(img_right, cv2.COLOR_BGR2GRAY)

    # Find chessboard corners
    ret_left, corners_left = cv2.findChessboardCorners(gray_left, chessboard_size, None)
    ret_right, corners_right = cv2.findChessboardCorners(gray_right, chessboard_size, None)

    if ret_left and ret_right:
        objpoints.append(objp)
        corners_left = cv2.cornerSubPix(gray_left, corners_left, (11, 11), (-1, -1), criteria)
        corners_right = cv2.cornerSubPix(gray_right, corners_right, (11, 11), (-1, -1), criteria)
        imgpoints_left.append(corners_left)
        imgpoints_right.append(corners_right)

# Calibrate each camera individually
ret_left, mtx_left, dist_left, rvecs_left, tvecs_left = cv2.calibrateCamera(objpoints, imgpoints_left, gray_left.shape[::-1], None, None)
ret_right, mtx_right, dist_right, rvecs_right, tvecs_right = cv2.calibrateCamera(objpoints, imgpoints_right, gray_right.shape[::-1], None, None)
print(f"LEFT calibration RMS error: {ret_left}")
print(f"RIGHT calibration RMS error: {ret_right}")

# Stereo calibration
# flags = cv2.CALIB_FIX_INTRINSIC
flags = cv2.CALIB_USE_INTRINSIC_GUESS | cv2.CALIB_FIX_PRINCIPAL_POINT
criteria_stereo = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, 1e-7)

retStereo, newCameraMatrixL, distL, newCameraMatrixR, distR, rot, trans, essentialMatrix, fundamentalMatrix = cv2.stereoCalibrate(
    objpoints, imgpoints_left, imgpoints_right,
    mtx_left, dist_left,
    mtx_right, dist_right,
    gray_left.shape[::-1],
    criteria=criteria_stereo,
    flags=0)

print(f"Stereo calibration RMS error: {retStereo}")

np.savez('stereo_calibration.npz',
    camera_matrix_left=newCameraMatrixL,
    dist_coeffs_left=distL,
    camera_matrix_right=newCameraMatrixR,
    dist_coeffs_right=distR,
    R=rot,
    T=trans
    )