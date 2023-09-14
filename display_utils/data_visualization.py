import matplotlib.pyplot as plt


def get_student_attendance_by_id(student_id, data_records):
    for data in data_records:
        if data["student_id"] == student_id:
            return {
                "Present": data["present"],
                "Absent": data["absent"]
            }
    return None


def get_all_students_attendance(data_records):
    attendance_data = []
    for data in data_records:
        attendance_data.append({
            "student_id": data["student_id"],
            "present": data["present"],
            "total": data["present"] + data["absent"]
        })
    return attendance_data


def plot_student_attendance_pie(student_id):
    student_data = get_student_attendance_by_id(student_id)

    if student_data is not None:
        labels = ['Present', 'Absent']
        sizes = [student_data['Present'], student_data['Absent']]
        colors = ['#66b3ff', '#ff9999']
        plt.figure(figsize=(6, 6))
        plt.pie(sizes, labels=labels, colors=colors,
                autopct='%1.1f%%', startangle=140)
        plt.title(f'Attendance for Student {student_id}')
        plt.axis('equal')
        plt.show()


def plot_all_students_attendance_bar():
    all_students_data = get_all_students_attendance()

    student_ids = [data["student_id"] for data in all_students_data]
    present_counts = [data["present"] for data in all_students_data]
    absent_counts = [data["total"] - data["present"]
                     for data in all_students_data]

    colors = ['#66b3ff', '#ff9999']

    plt.figure(figsize=(10, 6))
    plt.bar(student_ids, present_counts, label='Present', color=colors[0])
    plt.bar(student_ids, absent_counts, bottom=present_counts,
            label='Absent', color=colors[1])
    plt.title('Attendance Summary for All Students')
    plt.xlabel('Student ID')
    plt.ylabel('Attendance Count')
    plt.legend()
    plt.xticks(student_ids)
    plt.tight_layout()
    plt.show()


def plot_attendance_chart(student_id, is_present_counts):
    labels = list(is_present_counts.keys())
    sizes = list(is_present_counts.values())
    title = f"Attendance Distribution for Student ID {student_id}"
    plt.figure(title)
    colors = ['#74ed7c', '#ed7474']

    plt.pie(sizes, labels=labels, colors=colors,
            autopct='%1.1f%%', startangle=0)
    plt.axis('equal')
    plt.title(title)
    plt.show()
