import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

image = cv.imread("sign_sheets/3.jpeg")

imgray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

blurred_image = cv.GaussianBlur(imgray, (21, 21), sigmaX=51)


ret, thresh = cv.threshold(imgray, 127, 255, 0)
contours, hierarchy = cv.findContours(
    thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

# cv.drawContours(image, contours, -1, (0, 255, 0), 3)

for c in contours:
    x, y, w, h = cv.boundingRect(c)
    cv.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)

result = thresh

fig, axes = plt.subplots(1, 2)

axes[0].set_title("Original Image")
axes[0].imshow(image)

axes[1].set_title("Result")
axes[1].imshow(result, cmap=plt.cm.gray)

# plt.tight_layout()
plt.show()
