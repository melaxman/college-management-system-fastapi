from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Course
from schemas import CourseCreate, CourseRead
from database import get_db

router = APIRouter()

@router.post("/", response_model=CourseRead)
async def create_course(course: CourseCreate, db: AsyncSession = Depends(get_db)):
    db_course = Course(title=course.title, description=course.description)
    db.add(db_course)
    await db.commit()
    await db.refresh(db_course)
    return db_course

@router.get("/", response_model=list[CourseRead])
async def read_courses(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course))
    courses = result.scalars().all()
    return courses
