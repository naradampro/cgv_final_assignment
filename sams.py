import cv2 as cv
import numpy as np
from table_detection.find_contours import filter_contours_and_keep_rectangles, find_and_draw_contours, find_largest_contour_by_area  

SIGN_SHEETS_PATH = "sign_sheets/"

def sign_sheet_image(name):
    return "{}{}.{}".format(SIGN_SHEETS_PATH, name, "jpeg")

# Load the image
img = cv.imread(sign_sheet_image(1)) 

#  Draw contours on the original image
contour = find_and_draw_contours(img)

# Draw the filtered contours on the image
rectangular_contours, image_with_rectangles = filter_contours_and_keep_rectangles(img, contour)

find_largest_contour_by_area_in_img = find_largest_contour_by_area(img, rectangular_contours)

# Resize the image with contours (not the contours themselves)
new_width = 800
new_height = 600
resized_img = cv.resize(find_largest_contour_by_area_in_img, (new_width, new_height))

# Display the resized image
cv.imshow('Resized Image with Contours', resized_img)

# Wait for a key event and close the window when any key is pressed
cv.waitKey(0)
cv.destroyAllWindows()
