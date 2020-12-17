from crud import fetch_job_data, create_job_curd
from models import Job
from schemas import JobCreate
from fastapi.templating import Jinja2Templates
from database import SessionLocal, engine
from typing import List
from fastapi.staticfiles import StaticFiles
from fastapi import Depends, FastAPI, HTTPException, Request, BackgroundTasks
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
import database
import crud
import schemas
import models
models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Todo App",
    description="This is a basic project, with update, delete and create methods.",
    version="2.5.0",
)

# app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(user_id: int,
                         item: schemas.ItemCreate,
                         db: Session = Depends(get_db)):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    jobs = db.query(Job).all()
    # jobs = crud.get_jobs(db, skip=skip, limit=limit)
    return templates.TemplateResponse("home.html", {
        "request": request,
        "jobs": jobs
    })


@app.get("/add_job", response_class=HTMLResponse)
async def create_job(request: Request):
    return templates.TemplateResponse("addo.html", {"request": request})


@app.post("/add_job")
async def create_jobo(job_request: JobCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    add one or more tickers to the database
    """

    job = Job()
    job.title = job_request.title
    job.description = job_request.description
    db.add(job)
    db.commit()

    background_tasks.add_task(fetch_job_data, job.id)

    return {
        "code": "success",
        "message": "stock was added to the database"
    }
