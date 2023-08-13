import xml.etree.ElementTree as ET

class Student:
    def __init__(self, index_no, name, age):
        self.index_no = index_no
        self.name = name
        self.age = age

class StudentCollection:
    def __init__(self, xml_file):
        self.students = []
        self.load_students(xml_file)

    def load_students(self, xml_file):
        tree = ET.parse(xml_file)
        root = tree.getroot()

        for student_element in root.findall('student'):
            index_no = student_element.find('index_no').text
            name = student_element.find('name').text
            age = student_element.find('age').text

            student = Student(index_no, name, age)
            self.students.append(student)

    def find_by_index_no(self, index_no):
        for student in self.students:
            if student.index_no == index_no:
                return student
        return None

    def find_by_name(self, name):
        for student in self.students:
            if student.name == name:
                return student
        return None
