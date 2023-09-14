from student import StudentCollection

if __name__ == "__main__":
    collection = StudentCollection("info.xml")

    student_by_index = collection.find_by_student_no("10000409")
    if student_by_index:
        print(f"Student found by index number: {student_by_index.name}")
    else:
        print("Student not found by index number")

    student_by_name = collection.find_by_name("M S Dilshanika Perera")
    if student_by_name:
        print(f"Student found by name: {student_by_name.student_no}")
    else:
        print("Student not found by name")
