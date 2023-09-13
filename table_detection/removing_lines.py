import subprocess
import cv2 as cv
import numpy as np

# Preprocessing
def grayscale_image(self):
    self.grey = cv.cvtColor(self.image, cv.COLOR_BGR2GRAY)

def threshold_image(self):
    self.thresholded_image = cv.threshold(self.grey, 127, 255, cv.THRESH_BINARY)[1]

def invert_image(self):
    self.inverted_image = cv.bitwise_not(self.thresholded_image)

# Eroding Vertical Lines
def erode_vertical_lines(self):
    hor = np.array([[1,1,1,1,1,1]])
    self.vertical_lines_eroded_image = cv.erode(self.inverted_image, hor, iterations=10)
    self.vertical_lines_eroded_image = cv.dilate(self.vertical_lines_eroded_image, hor, iterations=10)


# Eroding Horizontal Lines
def erode_horizontal_lines(self):
    ver = np.array([[1],
            [1],
            [1],
            [1],
            [1],
            [1],
            [1]])
    self.horizontal_lines_eroded_image = cv.erode(self.inverted_image, ver, iterations=10)
    self.horizontal_lines_eroded_image = cv.dilate(self.horizontal_lines_eroded_image, ver, iterations=10)

# Combining Vertical And Horizontal Lines
def combine_eroded_images(self):
    self.combined_image = cv.add(self.vertical_lines_eroded_image, self.horizontal_lines_eroded_image)

def dilate_combined_image_to_make_lines_thicker(self):
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (2, 2))
    self.combined_image_dilated = cv.dilate(self.combined_image, kernel, iterations=5)

# Removing The Lines
def subtract_combined_and_dilated_image_from_original_image(self):
    self.image_without_lines = cv.subtract(self.inverted_image, self.combined_image_dilated)

def remove_noise_with_erode_and_dilate(self):
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (2, 2))
    self.image_without_lines_noise_removed = cv.erode(self.image_without_lines, kernel, iterations=1)
    self.image_without_lines_noise_removed = cv.dilate(self.image_without_lines_noise_removed, kernel, iterations=1)

# Finding the cells & extracting the text using OCR
#  Use Dilation To Convert The Words Into Blobs
def dilate_image(self):
    kernel_to_remove_gaps_between_words = np.array([
            [1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1]
    ])
    self.dilated_image = cv.dilate(self.thresholded_image, kernel_to_remove_gaps_between_words, iterations=5)
    simple_kernel = np.ones((5,5), np.uint8)
    self.dilated_image = cv.dilate(self.dilated_image, simple_kernel, iterations=2)

# Find The Contours Of The Blobs
def find_contours(self):
    result = cv.findContours(self.dilated_image, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    self.contours = result[0]
    # The code below is for visualization purposes only.
    # It is not necessary for the OCR to work.
    self.image_with_contours_drawn = self.original_image.copy()
    cv.drawContours(self.image_with_contours_drawn, self.contours, -1, (0, 255, 0), 3)


# Convert The Blobs Into Bounding Boxes
def convert_contours_to_bounding_boxes(self):
    self.bounding_boxes = []
    self.image_with_all_bounding_boxes = self.original_image.copy()
    for contour in self.contours:
        x, y, w, h = cv.boundingRect(contour)
        self.bounding_boxes.append((x, y, w, h))
        # This line below is about
        # drawing a rectangle on the image with the shape of
        # the bounding box. Its not needed for the OCR.
        # Its just added for debugging purposes.
        self.image_with_all_bounding_boxes = cv.rectangle(self.image_with_all_bounding_boxes, (x, y), (x + w, y + h), (0, 255, 0), 5)

# Sorting The Bounding Boxes By X And Y Coordinates To Make Rows And Columns
def get_mean_height_of_bounding_boxes(self):
    heights = []
    for bounding_box in self.bounding_boxes:
        x, y, w, h = bounding_box
        heights.append(h)
    return np.mean(heights)

def sort_bounding_boxes_by_y_coordinate(self):
    self.bounding_boxes = sorted(self.bounding_boxes, key=lambda x: x[1])

def club_all_bounding_boxes_by_similar_y_coordinates_into_rows(self):
    self.rows = []
    half_of_mean_height = self.mean_height / 2
    current_row = [ self.bounding_boxes[0] ]
    for bounding_box in self.bounding_boxes[1:]:
        current_bounding_box_y = bounding_box[1]
        previous_bounding_box_y = current_row[-1][1]
        distance_between_bounding_boxes = abs(current_bounding_box_y - previous_bounding_box_y)
        if distance_between_bounding_boxes <= half_of_mean_height:
            current_row.append(bounding_box)
        else:
            self.rows.append(current_row)
            current_row = [ bounding_box ]
    self.rows.append(current_row)

def sort_all_rows_by_x_coordinate(self):
    for row in self.rows:
        row.sort(key=lambda x: x[0])

# Extracting The Text From The Bounding Boxes Using OCR
def crop_each_bounding_box_and_ocr(self):
    self.table = []
    current_row = []
    image_number = 0
    for row in self.rows:
        for bounding_box in row:
            x, y, w, h = bounding_box
            y = y - 5
            cropped_image = self.original_image[y:y+h, x:x+w]
            image_slice_path = "./ocr_slices/img_" + str(image_number) + ".jpg"
            cv.imwrite(image_slice_path, cropped_image)
            results_from_ocr = self.get_result_from_tersseract(image_slice_path)
            current_row.append(results_from_ocr)
            image_number += 1
        self.table.append(current_row)
        current_row = []

def get_result_from_tersseract(self, image_path):
    output = subprocess.getoutput('tesseract ' + image_path + ' - -l eng --oem 3 --psm 7 --dpi 72 -c tessedit_char_whitelist="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789().calmg* "')
    output = output.strip()
    return output

# Generating The CSV
def generate_csv_file(self):
    with open("output.csv", "w") as f:
        for row in self.table:
            f.write(",".join(row) + "\n")


