import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import contours as utils

image = cv.imread("sign_sheets/1.jpeg")
cropped_image = utils.crop_image_to_table_area(image)

utils.plot_2img_compare(image, cropped_image)
