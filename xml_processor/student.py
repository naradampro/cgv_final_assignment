import xml.etree.ElementTree as ET


class Student:
    def __init__(self, student_no, title, name):
        self.student_no = student_no
        self.name = name
        self.title = title


class StudentCollection:
    def __init__(self, xml_file):
        self.students = []
        self.load_students(xml_file)

    def load_students(self, xml_file):
        tree = ET.parse(xml_file)
        root = tree.getroot()

        for student_element in root.findall('student'):
            student_no = student_element.find('student_no').text.strip()
            title = student_element.find('title').text.strip()
            name = student_element.find('name').text.strip()

            student = Student(student_no, title, name)
            self.students.append(student)

    def find_by_student_no(self, student_no):
        for student in self.students:
            if student.student_no == student_no:
                return student
        return None

    def find_by_name(self, name):
        for student in self.students:
            if student.name == name:
                return student
        return None
