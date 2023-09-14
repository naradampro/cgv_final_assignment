import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import pytesseract
import re
import custom_processors.custom_processors as custom_algos


def crop_image_to_table_area(image):
    imgray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    gaussian_kernal = custom_algos.gaussian_kernel(21, 15)

    blurred_image = custom_algos.gaussian_filter(imgray, gaussian_kernal)

    thresh = custom_algos.custom_threshold(blurred_image, 40)

    contours, hierarchy = cv.findContours(
        thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    kernel = np.ones((30, 30), np.uint8)

    eroded_image = cv.erode(thresh, kernel, iterations=10)

    plot_img(eroded_image)

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


def warp_image_to_fixed_size(image, target_width=2200, target_height=630):
    # Resize the image to the target dimensions without maintaining the aspect ratio
    warped_image = cv.resize(image, (target_width, target_height))

    return warped_image


def horizontally_divide_image(image, no_of_segments=7):
    segment_height = 630 // no_of_segments
    height, width = image.shape[:2]

    image_segments = []

    num_segments = height // segment_height

    for i in range(num_segments):
        start_y = i * segment_height
        end_y = (i + 1) * segment_height

        segment = image[start_y:end_y, :]
        image_segments.append(segment)

    return image_segments


def extract_table_rows(image):
    extracted_table = extract_sign_table(image)
    fixed_size_image = warp_image_to_fixed_size(extracted_table)
    return horizontally_divide_image(fixed_size_image)


def removeSpecialChars(type, string):

    if type == 'name':
        string = re.sub(r'^.*?\n', '', string)

    string = string.split("\n")
    print(string[0])
    return string[0]


def read_id(row):
    imgray = cv.cvtColor(row, cv.COLOR_BGR2GRAY)
    _, thresh = cv.threshold(imgray, 127, 255, 0)
    text = pytesseract.image_to_string(thresh)
    pattern = r'\b\d{8}\b'
    matches = re.findall(pattern, text)
    if matches:
        student_id = matches[0]
    else:
        student_id = None

    return student_id


def crop_signature_cell(image, crop_width=475):
    height, width = image.shape[:2]
    start_x = max(width - crop_width, 0)
    end_x = width
    cropped_segment = image[:, start_x:end_x]
    return cropped_segment


def count_black_pixels(thresholded_image):
    black_pixel_count = np.count_nonzero(thresholded_image == 0)
    return black_pixel_count


def is_present(row):
    signature_cell = crop_signature_cell(row)
    cell_gray = cv.cvtColor(signature_cell, cv.COLOR_BGR2GRAY)
    _, thresh = cv.threshold(cell_gray, 127, 255, 0)

    black_pixels_count = count_black_pixels(thresh)

    if (black_pixels_count > 4000):
        attendance_status = True
    else:
        attendance_status = False

    return attendance_status


def get_attendance_report(image):
    rows = extract_table_rows(image)
    row = rows[5]

    result = []

    for row in rows:
        id = read_id(row)
        if id is not None:
            is_present_value = is_present(row)
            result.append({"id": id, "is_present": is_present_value})

    return result


image = cv.imread("sign_sheets/1.jpeg")

attendance_report = get_attendance_report(image)
for item in attendance_report:
    print(
        f"ID: {item['id']} is {'present' if item['is_present'] else 'absent'}")
