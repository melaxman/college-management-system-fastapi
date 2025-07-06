from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert, delete
from models import enrollments_table, Student, Course
from schemas import EnrollmentCreate
from database import get_db

router = APIRouter()

@router.post("/")
async def enroll_student(enrollment: EnrollmentCreate, db: AsyncSession = Depends(get_db)):
    # Check student exists
    student = await db.get(Student, enrollment.student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Check course exists
    course = await db.get(Course, enrollment.course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Insert enrollment (avoid duplicates)
    stmt = insert(enrollments_table).values(student_id=enrollment.student_id, course_id=enrollment.course_id)
    try:
        await db.execute(stmt)
        await db.commit()
    except Exception:
        raise HTTPException(status_code=400, detail="Enrollment already exists or error")

    return {"message": "Student enrolled successfully"}

@router.get("/")
async def get_enrollments(db: AsyncSession = Depends(get_db)):
    query = (
        select(Student.id, Student.name, Course.id, Course.title)
        .select_from(enrollments_table)
        .join(Student, enrollments_table.c.student_id == Student.id)
        .join(Course, enrollments_table.c.course_id == Course.id)
    )
    result = await db.execute(query)
    data = result.all()
    return [
        {
            "student_id": s_id,
            "student_name": s_name,
            "course_id": c_id,
            "course_title": c_title,
        } for s_id, s_name, c_id, c_title in data
    ]
