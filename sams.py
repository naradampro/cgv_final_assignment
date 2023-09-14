import sys
import cv2 as cv
import attendance_processor as attendace
from xml_processor.student import StudentCollection
from prettytable import PrettyTable
import db.dbmodel as db
import re

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


def get_session_id(filename):
    match = re.search(r'(\d+)', filename)

    if match:
        numeric_part = match.group(1)
        return int(numeric_part)
    else:
        return None


def arguments():
    if len(sys.argv) != 3:
        print("Usage: python sams.py <info.xml> <image.jpeg>")
        return
    info_file = sys.argv[1]
    image_file = sys.argv[2]

    return info_file, image_file


def save_to_db(attendance_report, students_info, session_id):
    for item in attendance_report:
        student = students_info.find_by_student_no(item['id'])
        if student:
            student_id = item['id']
            is_present = item['is_present']
            db.create_attendance_record(session_id, student_id, is_present)


if __name__ == "__main__":
    info_file, image_file = arguments()
    attendance_rep = attendace_report(image_file)
    student_info = StudentCollection(info_file)
    session_id = get_session_id(image_file)
    session_saved = db.session_id_exists(session_id)
    if session_saved:
        print("Attendance record with session ID", session_id,
              "already exists. Not saving duplicate data.")
    else:
        save_to_db(attendance_rep, student_info, session_id)

    print_attendance(attendance_rep, student_info)
