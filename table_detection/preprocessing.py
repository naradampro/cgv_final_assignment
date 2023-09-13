import cv2 as cv


def convert_image_to_grayscale(image):
    # Convert the image to grayscale
    grayscale_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    return grayscale_image

# Define the threshold_image function
def threshold_image(image):
    # Threshold the grayscale image using OTSU thresholding
    thresholded_image = cv.threshold(image, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)[1]
    return thresholded_image

# Define the invert_image function
def invert_image(image):
    inverted_image = cv.bitwise_not(image)
    return inverted_image

# Define the dilate_image function
def dilate_image(image):
    dilated_image = cv.dilate(image, None, iterations=5)
    return dilated_image