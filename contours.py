import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np


def extract_contours(image):
    imgray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    ret, thresh = cv.threshold(imgray, 127, 255, 0)
    contours, hierarchy = cv.findContours(
        thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    return sorted(contours, key=cv.contourArea, reverse=True)


def extract_biggest_contour(image):

    contours = extract_contours(image)

    # return max(cnts, key=cv.contourArea)
    return contours[1]


def perspective_transform(image, contour):
    # get perimeter and approximate a polygon
    peri = cv.arcLength(contour, True)
    corners = cv.approxPolyDP(contour, 0.04 * peri, True)

    # Define the input corners of the quadrilateral 'corners'
    icorners = np.float32(corners)

    x, y, wd, ht = cv.boundingRect(icorners)

    # Define the corresponding output corners for the rectangle
    ocorners = np.float32([[wd, 0], [wd, ht], [0, ht], [0, 0]])

    # get perspective tranformation matrix
    M = cv.getPerspectiveTransform(icorners, ocorners)

    # do perspective
    return cv.warpPerspective(image, M, (wd, ht))


def plot_2img_compare(original_image, result):
    fig, axes = plt.subplots(1, 2)

    axes[0].set_title("Original Image")
    axes[0].imshow(original_image)

    axes[1].set_title("Result")
    axes[1].imshow(result, cmap=plt.cm.gray)

    plt.tight_layout()
    plt.show()


def plot_img(image, title="Image Title"):
    plt.imshow(image)
    plt.title(title)
    plt.show()


image = cv.imread("sign_sheets/1.jpeg")
# biggest_contour = extract_biggest_contour(image)

# result = perspective_transform(image, biggest_contour)

contours = extract_contours(image)
cv.drawContours(image, contours, -1, (0, 255, 0), 3)

plot_img(image)
