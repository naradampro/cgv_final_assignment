from student import StudentCollection

if __name__ == "__main__":
    collection = StudentCollection("info.xml")
    
    student_by_index = collection.find_by_index_no("001")
    if student_by_index:
        print(f"Student found by index number: {student_by_index.name}")
    else:
        print("Student not found by index number")

    student_by_name = collection.find_by_name("John Snow")
    if student_by_name:
        print(f"Student found by name: {student_by_name.index_no}")
    else:
        print("Student not found by name")
