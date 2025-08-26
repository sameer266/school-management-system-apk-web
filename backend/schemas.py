from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
    username:str
    email:str
    password:str
    
 
    
    
class StudentBase(BaseModel):
    first_name: str
    last_name: str
    grade: int
    roll_no: int

class StudentCreate(StudentBase):
    pass

class StudentOut(StudentBase):
    id: int

    class Config:
        orm_mode = True

class TeacherBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    subject: str

class TeacherCreate(TeacherBase):
    pass

class TeacherOut(TeacherBase):
    id: int

    class Config:
        orm_mode = True

class CourseBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None

class CourseCreate(CourseBase):
    pass

class CourseOut(CourseBase):
    id: int

    class Config:
        orm_mode = True