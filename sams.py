import sys
import cv2 as cv
import attendance_processor as attendace
from xml_processor.student import StudentCollection
from prettytable import PrettyTable

SIGN_SHEETS_PATH = "sign_sheets/"


def sign_sheet_image(file_name):
    return "{}{}".format(SIGN_SHEETS_PATH, file_name)


def print_attendance(attendance_report, students_info):
    table = PrettyTable()
    table.field_names = ["Student ID", "Student Name", "Attendance Status"]

    for item in attendance_report:
        student = students_info.find_by_student_no(item['id'])
        if student:
            student_name = student.name
            attendance_status = 'Present' if item['is_present'] else 'Absent'
            table.add_row([item['id'], student_name, attendance_status])

    print(table)


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
    attendance_rep = attendace_report(image_file)
    student_info = StudentCollection(info_file)
    print_attendance(attendance_rep, student_info)
