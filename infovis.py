import sys
import db.dbmodel as db
import display_utils.data_visualization as visualize
import matplotlib.pyplot as plt


def display_attendance_chart(student_id):
    attendance_records = db.get_attendance_records_by_student_id(student_id)
    is_present_counts = {'Present': 0, 'Absent': 0}

    for record in attendance_records:
        if record.is_present:
            is_present_counts['Present'] += 1
        else:
            is_present_counts['Absent'] += 1

    visualize.plot_attendance_chart(student_id, is_present_counts)


def arguments():
    if len(sys.argv) != 2:
        print("Usage: python infovis.py <student_id>")
        return
    student_id = sys.argv[1]
    return student_id


if __name__ == "__main__":
    student_id = arguments()
    display_attendance_chart(student_id)
