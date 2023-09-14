import sys
import db.dbmodel as db


def arguments():
    if len(sys.argv) != 2:
        print("Usage: python infovis.py <student_id>")
        return
    student_id = sys.argv[1]
    return student_id


if __name__ == "__main__":
    student_id = arguments()
    print(student_id)
    attendance = db.get_attendance_records_by_student_id(student_id)
    print(attendance)
