import cv2 as cv
from matplotlib import pyplot as plt
import numpy as np


file = r'../sign_sheets/1.jpeg'
table_image_contour = cv.imread(file, 0)
table_image = cv.imread(file)

# Inverse Image Thresholding which enhances the data present in the given image
ret, thresh_value = cv.threshold(
    table_image_contour, 180, 255, cv.THRESH_BINARY_INV)

#image dilation
kernel = np.ones((5,5),np.uint8)
dilated_value = cv.dilate(thresh_value,kernel,iterations = 1)

#Use findContours to obtain the contours in the present image
contours, hierarchy = cv.findContours(
    dilated_value, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

for cnt in contours:
    x, y, w, h = cv.boundingRect(cnt)
    # bounding the images
    if y < 300:
        table_image = cv.rectangle(table_image, (x, y), (x + w, y + h), (0, 0, 255), 1)

plt.imshow(table_image)
plt.show()
cv.namedWindow('detecttable', cv.WINDOW_NORMAL)


