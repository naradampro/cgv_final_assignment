import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

image = cv.imread("sign_sheets/4.jpeg")
ht, wd = image.shape[:2]

imgray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
ret, thresh = cv.threshold(imgray, 127, 255, 0)
contours, hierarchy = cv.findContours(
    thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

cnts = sorted(contours, key=cv.contourArea, reverse=True)

big_contour = cnts[1]

# get perimeter and approximate a polygon
peri = cv.arcLength(big_contour, True)
corners = cv.approxPolyDP(big_contour, 0.04 * peri, True)

# Define the input corners of the quadrilateral 'corners'
icorners = np.float32(corners)

# Define the corresponding output corners for the rectangle
ocorners = np.float32([[wd, 0], [wd, ht], [0, ht], [0, 0]])

# get perspective tranformation matrix
M = cv.getPerspectiveTransform(icorners, ocorners)

# do perspective
warped = cv.warpPerspective(image, M, (wd, ht))


result = warped

fig, axes = plt.subplots(1, 2)

axes[0].set_title("Original Image")
axes[0].imshow(image)

axes[1].set_title("Result")
axes[1].imshow(result, cmap=plt.cm.gray)

# plt.tight_layout()
plt.show()
