from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Student
from schemas import StudentCreate, StudentRead
from database import get_db

router = APIRouter()

@router.post("/", response_model=StudentRead)
async def create_student(student: StudentCreate, db: AsyncSession = Depends(get_db)):
    db_student = Student(name=student.name, email=student.email)
    db.add(db_student)
    await db.commit()
    await db.refresh(db_student)
    return db_student

@router.get("/", response_model=list[StudentRead])
async def read_students(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Student))
    students = result.scalars().all()
    return students
