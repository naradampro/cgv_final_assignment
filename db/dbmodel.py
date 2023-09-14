from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class Attendance(Base):
    __tablename__ = 'attendance'

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer)
    sessionclass_id = Column(Integer)
    is_present = Column(Boolean, default=False)


def create_session():
    engine = create_engine('sqlite:///attendance.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    return session, engine


def create_attendance_record(session_id, student_id, is_present):
    session, engine = create_session()
    try:
        # Create the table if it doesn't exist
        Base.metadata.create_all(engine)

        # Create a new Attendance record
        attendance_record = Attendance(
            sessionclass_id=session_id, student_id=student_id, is_present=is_present)

        # Add the record to the session and commit it to the database
        session.add(attendance_record)
        session.commit()

        print("Attendance record created successfully with ID:",
              attendance_record.id)
    except Exception as e:
        session.rollback()
        print("Error:", str(e))
    finally:
        session.close()


def session_id_exists(session_id):
    session, _ = create_session()

    try:
        # Check if a record with the same session_id exists
        existing_record = session.query(Attendance).filter_by(
            sessionclass_id=session_id).first()

        return existing_record is not None
    except Exception as e:
        print("Error:", str(e))
    finally:
        session.close()
