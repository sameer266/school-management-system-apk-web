from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Enum, Boolean, Float
from sqlalchemy.orm import relationship
from database import Base
import enum
from datetime import datetime

# -------------------------
# Enums
# -------------------------
class GenderEnum(enum.Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"

class UserRoleEnum(enum.Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    PRINCIPAL = "principal"
    ADMIN = "admin"

class AttendanceStatusEnum(enum.Enum):
    PRESENT = "present"
    ABSENT = "absent"
    LEAVE = "leave"

# -------------------------
# Users & Authentication
# -------------------------
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(UserRoleEnum), default=UserRoleEnum.STUDENT)

    student = relationship("Student", back_populates="user", uselist=False)
    teacher = relationship("Teacher", back_populates="user", uselist=False)
    principal = relationship("Principal", back_populates="user", uselist=False)


# -------------------------
# Students
# -------------------------
class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    grade = Column(Integer)
    roll_no = Column(Integer, unique=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="student")
    results = relationship("Result", back_populates="student")
    attendance_records = relationship("Attendance", back_populates="student")
    payments = relationship("Payment", back_populates="student")


# -------------------------
# Teachers
# -------------------------
class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    subject = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="teacher")
    courses = relationship("Course", back_populates="teacher")
    notifications_sent = relationship("Notification", back_populates="teacher")


# -------------------------
# Principal
# -------------------------
class Principal(Base):
    __tablename__ = "principals"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="principal")


# -------------------------
# Courses
# -------------------------
class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    code = Column(String, unique=True, index=True)
    description = Column(String)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))

    teacher = relationship("Teacher", back_populates="courses")


# -------------------------
# Results
# -------------------------
class Result(Base):
    __tablename__ = "results"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    score = Column(Float)
    grade = Column(String)

    student = relationship("Student", back_populates="results")
    course = relationship("Course")


# -------------------------
# Attendance
# -------------------------
class Attendance(Base):
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    date = Column(Date, default=datetime.utcnow)
    status = Column(Enum(AttendanceStatusEnum), default=AttendanceStatusEnum.PRESENT)

    student = relationship("Student", back_populates="attendance_records")


# -------------------------
# Notifications
# -------------------------
class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    message = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=True)

    student = relationship("Student")
    teacher = relationship("Teacher", back_populates="notifications_sent")


# -------------------------
# Payments
# -------------------------
class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    amount = Column(Float)
    paid_on = Column(DateTime, default=datetime.utcnow)
    method = Column(String)  # e.g., "Cash", "Bank", "eSewa"
    status = Column(String, default="completed")

    student = relationship("Student", back_populates="payments")
