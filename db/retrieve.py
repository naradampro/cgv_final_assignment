from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

# Create an SQLite database file
engine = create_engine('sqlite:///data.db', echo=True)

# Create a base class for declarative models
Base = declarative_base()

# Define a sample model for students


class Student(Base):
    __tablename__ = 'students'

    student_id = Column(Integer, primary_key=True)
    name = Column(String)


class Sessionclass(Base):
    __tablename__ = 'sessionclass'

    sessionclass_id = Column(Integer, primary_key=True)
    date = Column(String)
    topic = Column(String)


class Attendance(Base):
    __tablename__ = 'attendance'

    attendance_id = Column(Integer, primary_key=True)
    student_id = Column(String)
    sessionclass_id = Column(Integer)
    is_present = Column(Boolean, default=False)


# Create the tables in the database
Base.metadata.create_all(engine)

# Create a session factory
Session = sessionmaker(bind=engine)

# Create a session to interact with the database
session = Session()

# Query and print student information
# students = session.query(Student).all()
# for student in students:
#     print(student.student_id, student.name)

# # Query and print session class information
# sessionclass = session.query(Sessionclass).all()
# for sessionclass in sessionclass:
#     print(sessionclass.sessionclass_id, sessionclass.date, sessionclass.topic)

# # Query and print attendance records
attendance = session.query(Attendance).all()
for attendance in attendance:
    print(attendance.id, attendance.student_id,
          attendance.sessionclass_id, attendance.is_present)
