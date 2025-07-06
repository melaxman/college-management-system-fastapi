from pydantic import BaseModel
from typing import Optional, List

class StudentBase(BaseModel):
    name: str
    email: str

class StudentCreate(StudentBase):
    pass

class StudentRead(StudentBase):
    id: int

    class Config:
        from_attributes = True

class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None

class CourseCreate(CourseBase):
    pass

class CourseRead(CourseBase):
    id: int

    class Config:
        from_attributes = True

class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int
