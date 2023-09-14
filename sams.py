import sys
import cv2 as cv
import attendance_processor as attendace
from xml_processor.student import StudentCollection

SIGN_SHEETS_PATH = "sign_sheets/"


def sign_sheet_image(file_name):
    return "{}{}".format(SIGN_SHEETS_PATH, file_name)


def print_attendace(attendance_report):
    for item in attendance_report:
        print(
            f"ID: {item['id']} is {'present' if item['is_present'] else 'absent'}")


def attendace_report(image_file):
    image = cv.imread(sign_sheet_image(image_file))

    return attendace.get_attendance_report(image)


def arguments():
    if len(sys.argv) != 3:
        print("Usage: python sams.py <info.xml> <image.jpeg>")
        return
    info_file = sys.argv[1]
    image_file = sys.argv[2]

    return info_file, image_file


if __name__ == "__main__":
    info_file, image_file = arguments()
    attendace_rep = attendace_report(image_file)
    print_attendace(attendace_rep)
