from fastapi import APIRouter, Depends, status, Response,  HTTPException
from .. import schemas, models, database
from typing import List
from sqlalchemy.orm import Session
from ..repository import blog

router = APIRouter(
    prefix = '/blog',
    tags = ['Blogs']
)
get_db = database.get_db

@router.get('',response_model=List[schemas.ShowBlog])
def all(db:Session = Depends(get_db)):
    return blog.get_all(db)

@router.post('', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)): #Depends converts the parameter to pydantic, thsi is used to make interpreter know that it is not a parameter
    return blog.create(request, db)

@router.get('/{blog_id}', status_code=status.HTTP_200_OK,response_model=schemas.ShowBlog, tags=['Blogs'])
def show(blog_id:int, response:Response, db:Session = Depends(get_db)):
    return blog.showone(db, blog_id)

@router.delete('/{blog_id}')
def deleteblog(blog_id:int,response:Response, db:Session = Depends(get_db)):
    #data = db.query(models.Blog).filter(models.Blog.id == blog_id)
    return blog.destroy(db, blog_id)
    

@router.put('/{blog_id}', status_code=status.HTTP_202_ACCEPTED)
def update(blog_id:int, request:schemas.Blog, response:Response, db:Session = Depends(get_db)):
    return blog.updateblog(request, db, blog_id)