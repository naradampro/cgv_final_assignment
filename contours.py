import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np


def crop_image_to_table_area(image):
    imgray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    blurred_image = cv.GaussianBlur(imgray, (21, 21), sigmaX=15)

    ret, thresh = cv.threshold(blurred_image, 127, 255, 0)
    contours, hierarchy = cv.findContours(
        thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    kernel = np.ones((30, 30), np.uint8)

    eroded_image = cv.erode(thresh, kernel, iterations=15)

    contours, hierarchy = cv.findContours(
        eroded_image, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    big_cont = contours[1]

    x, y, w, h = cv.boundingRect(big_cont)

    return image[y:y+h, x:x+w]


def extract_table_lines(img):
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    kernel = cv.getStructuringElement(cv.MORPH_RECT, (1, 1))
    img_gray = cv.morphologyEx(img_gray, cv.MORPH_CLOSE, kernel)

    (_, img_bin) = cv.threshold(img_gray,
                                128, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    img_bin = cv.bitwise_not(img_bin)

    kernel_length_v = (np.array(img_gray).shape[1]) // 120
    vertical_kernel = cv.getStructuringElement(
        cv.MORPH_RECT, (1, kernel_length_v))
    im_temp1 = cv.erode(img_bin, vertical_kernel, iterations=3)

    vertical_lines_img = cv.dilate(im_temp1, vertical_kernel, iterations=3)

    kernel_length_h = (np.array(img_gray).shape[1]) // 120
    horizontal_kernel = cv.getStructuringElement(
        cv.MORPH_RECT, (kernel_length_h, 1))
    im_temp2 = cv.erode(img_bin, horizontal_kernel, iterations=3)
    horizontal_lines_img = cv.dilate(im_temp2, horizontal_kernel, iterations=3)

    kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
    table_segment = cv.addWeighted(
        vertical_lines_img, 0.5, horizontal_lines_img, 0.5, 0.0)
    table_segment = cv.erode(cv.bitwise_not(
        table_segment), kernel, iterations=2)
    _, table_segment = cv.threshold(table_segment, 0, 255, cv.THRESH_OTSU)

    return table_segment


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
    (_, _), (w, h), _ = cv.minAreaRect(contour)

    # Get perimeter and approximate a polygon
    peri = cv.arcLength(contour, True)
    corners = cv.approxPolyDP(contour, 0.04 * peri, True)

    # Define the input corners of the quadrilateral 'corners'
    icorners = np.float32(corners)

    # Calculate the bounding rectangle of the contour
    x, y, wd, ht = cv.boundingRect(icorners)

    if w > h:
        ocorners = np.float32([[0, 0], [wd, 0], [wd, ht], [0, ht]])
    else:
        ocorners = np.float32([[wd, 0], [wd, ht], [0, ht], [0, 0]])

    # Get perspective transformation matrix
    M = cv.getPerspectiveTransform(icorners, ocorners)

    return cv.warpPerspective(image, M, (wd, ht))


def plot_2img_compare(original_image, result):
    fig, axes = plt.subplots(1, 2)

    axes[0].set_title("Original Image")
    axes[0].imshow(original_image, cmap=plt.cm.gray)

    axes[1].set_title("Result")
    axes[1].imshow(result, cmap=plt.cm.gray)

    plt.tight_layout()
    plt.show()


def plot_img(image, title="Image Title"):
    plt.imshow(image, cmap=plt.cm.gray)
    plt.title(title)
    plt.show()


def extract_sign_table(image):
    cropped_image = crop_image_to_table_area(image)
    table_line_image = extract_table_lines(cropped_image)

    contours, hierarchy = cv.findContours(
        table_line_image, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    biggest_contour = contours[1]

    return perspective_transform(cropped_image, biggest_contour)


image = cv.imread("sign_sheets/4.jpeg")

extracted_table = extract_sign_table(image)

plot_img(extracted_table)

# cv.imwrite("extracted5.jpeg", extracted_table)
