from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException, status

def get_all(db:Session):
    blogs = db.query(models.Blog).all()
    return blogs

def create(request:schemas.Blog, db:Session):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def destroy(db:Session, blog_id:int):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).delete(synchronize_session=False)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Blog with id {blog_id} not available!')
    
    db.commit()
    return {'detail':"blog deleted!"}

def updateblog(request:schemas.Blog, db:Session, blog_id:int):
    title = request.title
    body = request.body
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).update({'title':title, 'body':body}, synchronize_session=False)
    db.commit()
    return {'detail':'blog updated successfully'}

def showone(db:Session, blog_id:int):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Blog with id {blog_id} not available!')
    return blog