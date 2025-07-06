from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from datetime import timedelta

from auth import authenticate_user, create_access_token
from database import engine
from models import Base

from routers.students import router as students_router
from routers.courses import router as courses_router
from routers.enrollments import router as enrollments_router

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = create_access_token({"sub": user["username"]}, timedelta(minutes=30))
    return {"access_token": token, "token_type": "bearer"}

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(students_router, prefix="/students", tags=["students"])
app.include_router(courses_router, prefix="/courses", tags=["courses"])
app.include_router(enrollments_router, prefix="/enrollments", tags=["enrollments"])
