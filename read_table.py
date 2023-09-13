import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import pytesseract


def extract_contours(image):
    imgray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    ret, thresh = cv.threshold(imgray, 127, 255, 0)
    contours, hierarchy = cv.findContours(
        thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    return sorted(contours, key=cv.contourArea, reverse=True)


def plot_img(image, title="Image Title"):
    plt.imshow(image, cmap=plt.cm.gray)
    plt.title(title)
    plt.show()


def read_data(image):
    contours = extract_contours(image)
    cv.drawContours(image, contours, -1, (0, 255, 0), 3)
    return image


image = cv.imread("outputs/extracted1.jpeg")

plot_img(read_data(image))
