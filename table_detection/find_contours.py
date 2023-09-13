import cv2 as cv
import numpy as np

from table_detection.preprocessing import convert_image_to_grayscale, dilate_image, invert_image, threshold_image


# Define a function to find contours
def find_and_draw_contours(image):
   img_gray = convert_image_to_grayscale(image)

    # Threshold the grayscale image
   img_thresholded = threshold_image(img_gray)

# Invert the thresholded image
   image_inverted = invert_image(img_thresholded)

# Dilate the inverted image
   img_dilation = dilate_image(image_inverted) 

   contours, _ = cv.findContours(img_dilation, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

# Draw contours on the original image
   contour_image = image.copy()
   cv.drawContours(contour_image, contours, -1, (0, 255, 0), 2)

   return contour_image

# Define a function to filter contours and keep only rectangles
def filter_contours_and_keep_rectangles(image, contours):
    rectangular_contours = []

    for contour in contours:
        peri = cv.arcLength(contour, True)
        approx = cv.approxPolyDP(contour, 0.02 * peri, True)
        if len(approx) == 4:
            rectangular_contours.append(approx)

    # Create an image copy to draw the rectangular contours
    image_with_only_rectangular_contours = image.copy()
    cv.drawContours(image_with_only_rectangular_contours, rectangular_contours, -1, (0, 255, 0), 3)

    return rectangular_contours, image_with_only_rectangular_contours

# Define a function to find the largest contour by area
def find_largest_contour_by_area(image,rectangular_contours):
    max_area = 0
    contour_with_max_area = None
    for contour in rectangular_contours:
        area = cv.contourArea(contour)
        if area > max_area:
            max_area = area
            contour_with_max_area = contour
    image_with_contour_with_max_area = image.copy()
    cv.drawContours(image_with_contour_with_max_area, [contour_with_max_area], -1, (0, 255, 0), 3)
    return contour_with_max_area