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
    student_id = Column(Integer)
    sessionclass_id = Column(Integer)
    is_present = Column(Boolean, default=False)

# Create the tables in the database
Base.metadata.create_all(engine)

# Create a session factory
Session = sessionmaker(bind=engine)

# Create a session to interact with the database
session = Session()

# Create a new student
new_student = Student(student_id=1, name='John Doe')
session.add(new_student)
session.commit()

# Create a new session 
new_sessionclass = Sessionclass(sessionclass_id=1, date='2023-08-16', topic='Some Topic')
session.add(new_sessionclass)
session.commit()

# Create a new attendance entry
new_attendance = Attendance(attendance_id=1, student_id=1, sessionclass_id=1, is_present=True)
session.add(new_attendance)
session.commit()

