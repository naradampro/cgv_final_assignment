import cv2
import matplotlib.pyplot as plt
import imutils
import perspective

image = cv2.imread("sign_sheets/sudoku.jpeg")

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (7, 7), 3)
# apply adaptive thresholding and then invert the threshold map
thresh = cv2.adaptiveThreshold(blurred, 255,
                               cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
thresh = cv2.bitwise_not(thresh)

# find contours in the thresholded image and sort them by size in
# descending order
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

# initialize a contour that corresponds to the puzzle outline
puzzleCnt = None
# loop over the contours
for c in cnts:
    # approximate the contour
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    # if our approximated contour has four points, then we can
    # assume we have found the outline of the puzzle
    if len(approx) == 4:
        puzzleCnt = approx
        break

# apply a four point perspective transform to both the original
# image and grayscale image to obtain a top-down bird's eye view
# of the puzzle
puzzle = perspective.four_point_transform(image, puzzleCnt.reshape(4, 2))
warped = perspective.four_point_transform(gray, puzzleCnt.reshape(4, 2))

# Display the image

fig, axes = plt.subplots(1, 2, figsize=(15, 5))

axes[0].set_title("Original Image")
axes[0].imshow(image)

axes[1].set_title("Perspective Corrected")
axes[1].imshow(warped, cmap=plt.cm.gray)

plt.tight_layout()
plt.show()
