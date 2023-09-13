import matplotlib.pyplot as plt

# Sample data for student attendance
sample_data = [
    {"student_id": 1, "name": "John Doe", "present": 20, "absent": 5},
    {"student_id": 2, "name": "Jane Smith", "present": 18, "absent": 7},
    {"student_id": 3, "name": "Alice Johnson", "present": 22, "absent": 3},
]

# should retrieve from the database. For testing purposes, I have used the above sample data
def get_student_attendance_by_id(student_id):
    for data in sample_data:
        if data["student_id"] == student_id:
            return {
                "Present": data["present"],
                "Absent": data["absent"]
            }
    return None


def plot_student_attendance_pie(student_id):
    student_data = get_student_attendance_by_id(student_id)

    if student_data is not None:
        labels = ['Present', 'Absent']
        sizes = [student_data['Present'], student_data['Absent']]
        colors = ['#66b3ff', '#ff9999']
        plt.figure(figsize=(6, 6))
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        plt.title(f'Attendance for Student {student_id}')
        plt.axis('equal')
        plt.show()


student_id = 3
plot_student_attendance_pie(student_id)
