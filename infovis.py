import sys
import db.dbmodel as db
import display_utils.data_visualization as visualize
import matplotlib.pyplot as plt


def arguments():
    if len(sys.argv) != 2:
        print("Usage: python infovis.py <student_id>")
        return
    student_id = sys.argv[1]
    return student_id


if __name__ == "__main__":
    student_id = arguments()
    attendance_records = db.get_attendance_records_by_student_id(student_id)
    is_present_counts = {'Present': 0, 'Absent': 0}

    for record in attendance_records:
        if record.is_present:
            is_present_counts['Present'] += 1
        else:
            is_present_counts['Absent'] += 1

    # Create a pie chart
    labels = list(is_present_counts.keys())
    sizes = list(is_present_counts.values())
    colors = ['#74ed7c', '#ed7474']
    explode = (0.1, 0)  # explode the 'Present' slice

    plt.pie(sizes, labels=labels, colors=colors,
            autopct='%1.1f%%', startangle=140)
    # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.axis('equal')

    plt.title(f"Attendance Distribution for Student ID {student_id}")
    plt.show()
