from fastapi import FastAPI, Path, Query, HTTPException, status, Request, Depends
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Optional
from pydantic import BaseModel
from app import app
import fast_models
from fastDataBase import engine, SessionLocal
from sqlalchemy.orm import Session
from flask import session, redirect, url_for

apps = FastAPI()

fast_models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Userapi(BaseModel):
    name: str
    age: int
    surname: Optional[str] = None
    info: Optional[str] = None


class UpdateUser(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    surname: Optional[str] = None
    info: Optional[str] = None


userlist = {}

templates = Jinja2Templates(directory='templates')


@apps.get('/', response_class=HTMLResponse)
async def doc_page(request: Request):
    return templates.TemplateResponse('fast.html', {'request': request})


@apps.get("/get-user")
def get_user(user_id: int = Query(None, description='Pass id here'), db: Session = Depends(get_db)):
    user_model = db.query(fast_models.Users).filter(fast_models.Users.id == user_id).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail="User ID not found")
    return db.query(fast_models.Users).filter(fast_models.Users.id).first()


@apps.get('/get-all-users')
def get_all(db: Session = Depends(get_db)):
    return db.query(fast_models.Users).all()


@apps.get("/get-by-name")
def get_item(name: str = Query(None, description='Input name here', min_length=2, max_length=20),
             db: Session = Depends(get_db)):
    user_model = db.query(fast_models.Users).filter(fast_models.Users.name == name)
    if user_model:
        return db.query(fast_models.Users).all()
    raise HTTPException(status_code=404, detail="User name not found.")


@apps.post("/create_user")
def create_user(user: Userapi, db: Session = Depends(get_db)):
    user_model = fast_models.Users()
    user_model.name = user.name
    user_model.surname = user.surname
    user_model.age = user.age
    user_model.info = user.info

    db.add(user_model)
    db.commit()
    return user


@apps.put("/update-user/{user_id}")
def update_user(user_id: int, user: UpdateUser, db: Session = Depends(get_db)):
    user_model = db.query(fast_models.Users).filter(fast_models.Users.id == user_id).first()

    if user_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User ID not found")

    user_model.name = user.name

    user_model.age = user.age

    user_model.surname = user.surname

    user_model.info = user.info

    db.add(user_model)
    db.commit()
    return user


@app.route('/logout')
def logout():
    session.pop('username',None)
    return redirect(url_for('index'))


@apps.delete("/delete-user")
def delete_user(user_id: int = Query(..., description="The ID for deleting user", gt=0), db: Session = Depends(get_db)):
    user_model = db.query(fast_models.Users).filter(fast_models.Users.id == user_id).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail="User ID not found")

    db.query(fast_models.Users).filter(fast_models.Users.id == user_id).delete()

    db.commit()
    return {"Success": "User was deleted"}


apps.mount('/hh', WSGIMiddleware(app))
