from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal, engine, Base
from utils import verify_password,get_password_hash


import models
import schemas

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="School Management System", version="1.0.0")

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

# ======== Login ===============
@app.post("/login/")
def login(username:str,password:str,db: Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.username == username).first()
    if not user and  not verify_password(password,user.hashed_password):
        raise HTTPException(status_code=401,detail="Invalid credentials")
    return{"success":True}

        
# =======================
#   User
# =======================
@app.post("/create_user/")
def create_user(user:schemas.UserCreate,db: Session=Depends(get_db)):
    exists=db.query(models.User).filter(models.User.username==user.username).first()
    if exists:
        raise HTTPException(status_code=401,detail="Username alredy exists")
    db_user=models.User(username=user.username,email=user.email,hashed_password=get_password_hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"success":True,"user_id":db_user.id}





# =====================
#  Students
# ===================
@app.post("/students/", response_model=schemas.StudentOut)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    exists = db.query(models.Student).filter_by(grade=student.grade, roll_no=student.roll_no).first()
    if exists:
        raise HTTPException(status_code=400, detail="Roll number already exists in this grade")
    db_student = models.Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@app.get("/students/", response_model=List[schemas.StudentOut])
def list_students(db: Session = Depends(get_db)):
    return db.query(models.Student).all()

@app.get("/students/{student_id}", response_model=schemas.StudentOut)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.put("/students/{student_id}", response_model=schemas.StudentOut)
def update_student(student_id: int, student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    exists = db.query(models.Student).filter_by(grade=student.grade, roll_no=student.roll_no).first()
    if exists and exists.id != student_id:
        raise HTTPException(status_code=400, detail="Roll number already exists in this grade")
    for key, value in student.dict().items():
        setattr(db_student, key, value)
    db.commit()
    db.refresh(db_student)
    return db_student

@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(student)
    db.commit()
    return {"message": "Student deleted successfully"}



#==========================
#         Teachers 
# ==========================

@app.post("/teachers/", response_model=schemas.TeacherOut)
def create_teacher(teacher: schemas.TeacherCreate, db: Session = Depends(get_db)):
    exists = db.query(models.Teacher).filter_by(email=teacher.email).first()
    if exists:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_teacher = models.Teacher(**teacher.dict())
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher

@app.get("/teachers/", response_model=List[schemas.TeacherOut])
def list_teachers(db: Session = Depends(get_db)):
    return db.query(models.Teacher).all()

@app.get("/teachers/{teacher_id}", response_model=schemas.TeacherOut)
def get_teacher(teacher_id: int, db: Session = Depends(get_db)):
    teacher = db.query(models.Teacher).filter(models.Teacher.id == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher

@app.put("/teachers/{teacher_id}", response_model=schemas.TeacherOut)
def update_teacher(teacher_id: int, teacher: schemas.TeacherCreate, db: Session = Depends(get_db)):
    db_teacher = db.query(models.Teacher).filter(models.Teacher.id == teacher_id).first()
    if not db_teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    exists = db.query(models.Teacher).filter_by(email=teacher.email).first()
    if exists and exists.id != teacher_id:
        raise HTTPException(status_code=400, detail="Email already registered")
    for key, value in teacher.dict().items():
        setattr(db_teacher, key, value)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher

@app.delete("/teachers/{teacher_id}")
def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
    teacher = db.query(models.Teacher).filter(models.Teacher.id == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    db.delete(teacher)
    db.commit()
    return {"message": "Teacher deleted successfully"}


# ======================
#  Courses
# ======================
@app.post("/courses/", response_model=schemas.CourseOut)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    exists = db.query(models.Course).filter_by(code=course.code).first()
    if exists:
        raise HTTPException(status_code=400, detail="Course code already exists")
    db_course = models.Course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@app.get("/courses/", response_model=List[schemas.CourseOut])
def list_courses(db: Session = Depends(get_db)):
    return db.query(models.Course).all()

@app.get("/courses/{course_id}", response_model=schemas.CourseOut)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@app.put("/courses/{course_id}", response_model=schemas.CourseOut)
def update_course(course_id: int, course: schemas.CourseCreate, db: Session = Depends(get_db)):
    db_course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    exists = db.query(models.Course).filter_by(code=course.code).first()
    if exists and exists.id != course_id:
        raise HTTPException(status_code=400, detail="Course code already exists")
    for key, value in course.dict().items():
        setattr(db_course, key, value)
    db.commit()
    db.refresh(db_course)
    return db_course

@app.delete("/courses/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    db.delete(course)
    db.commit()
    return {"message": "Course deleted successfully"}