import cv2 as cv
import numpy as np


def order_points_in_the_contour_with_max_area(self):
    self.contour_with_max_area_ordered = self.order_points(self.contour_with_max_area)
    # The code below is to plot the points on the image
    # it is not required for the perspective transform
    # it will help you to understand and debug the code
    self.image_with_points_plotted = self.image.copy()
    for point in self.contour_with_max_area_ordered:
        point_coordinates = (int(point[0]), int(point[1]))
        self.image_with_points_plotted = cv.circle(self.image_with_points_plotted, point_coordinates, 10, (0, 0, 255), -1)

def calculate_new_width_and_height_of_image(self):
    existing_image_width = self.image.shape[1]
    existing_image_width_reduced_by_10_percent = int(existing_image_width * 0.9)
    
    distance_between_top_left_and_top_right = self.calculateDistanceBetween2Points(self.contour_with_max_area_ordered[0], self.contour_with_max_area_ordered[1])
    distance_between_top_left_and_bottom_left = self.calculateDistanceBetween2Points(self.contour_with_max_area_ordered[0], self.contour_with_max_area_ordered[3])

    aspect_ratio = distance_between_top_left_and_bottom_left / distance_between_top_left_and_top_right

    self.new_image_width = existing_image_width_reduced_by_10_percent
    self.new_image_height = int(self.new_image_width * aspect_ratio)

def apply_perspective_transform(self):
    pts1 = np.float32(self.contour_with_max_area_ordered)
    pts2 = np.float32([[0, 0], [self.new_image_width, 0], [self.new_image_width, self.new_image_height], [0, self.new_image_height]])
    matrix = cv.getPerspectiveTransform(pts1, pts2)
    self.perspective_corrected_image = cv.warpPerspective(self.image, matrix, (self.new_image_width, self.new_image_height))

# Below are helper functions
def calculateDistanceBetween2Points(self, p1, p2):
    dis = ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5
    return dis

def order_points(self, pts):
    # initialzie a list of coordinates that will be ordered
    # such that the first entry in the list is the top-left,
    # the second entry is the top-right, the third is the
    # bottom-right, and the fourth is the bottom-left
    pts = pts.reshape(4, 2)
    rect = np.zeros((4, 2), dtype="float32")

    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # now, compute the difference between the points, the
    # top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    # return the ordered coordinates
    return rect