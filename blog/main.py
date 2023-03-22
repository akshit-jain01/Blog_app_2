from fastapi import FastAPI, Depends, status, Response, HTTPException #for custom response statuses

from . import schemas, models

from .database import engine, SessionLocal

from sqlalchemy.orm import Session

from typing import List

from .hashing import Hash

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


models.Base.metadata.create_all(bind = engine)

@app.post('/blog', status_code=status.HTTP_201_CREATED, tags=['Blogs'])
def create(request: schemas.Blog, db: Session = Depends(get_db)): #Depends converts the parameter to pydantic, thsi is used to make interpreter know that it is not a parameter
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blog',response_model=List[schemas.ShowBlog], tags=['Blogs'])
def all(db:Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{blog_id}', status_code=status.HTTP_200_OK, tags=['Blogs'])
def show(blog_id:int, response:Response, db:Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {'message':f'Blog with id {blog_id} not available!'}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Blog with id {blog_id} not available!')
    return blog

@app.delete('/blog/{blog_id}', tags=['Blogs'])
def deleteblog(blog_id:int,response:Response, db:Session = Depends(get_db)):
    #data = db.query(models.Blog).filter(models.Blog.id == blog_id)
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).delete(synchronize_session=False)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Blog with id {blog_id} not available!')
    db.commit()
    return {'detail':"blog deleted!"}

@app.put('/blog/{blog_id}', status_code=status.HTTP_202_ACCEPTED, tags=['Blogs'])
def update(blog_id:int, request:schemas.Blog, response:Response, db:Session = Depends(get_db)):
    title = request.title
    body = request.body
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).update({'title':title, 'body':body}, synchronize_session=False)
    db.commit()
    return {'detail':'blog updated successfully'}




@app.post('/user', tags=['User'])
def create_user(request: schemas.User, db:Session = Depends(get_db)):
    hashed_pwd = Hash.bcrypt(request.password)
    new_user = models.User(name = request.name, email = request.email, password = hashed_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/user',response_model=List[schemas.ShowUser], tags=['User'])
def all(db:Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@app.get('/user/{user_id}', response_model=schemas.ShowUser, tags=['User'])
def get_user(user_id:int, db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found!!')
    return user