from fastapi import APIRouter, Depends, status, Response,  HTTPException
from .. import schemas, models, database, hashing
from typing import List
from sqlalchemy.orm import Session

router = APIRouter(
    prefix = '/user',
    tags= ['User']
)
get_db = database.get_db


@router.post('', tags=['User'])
def create_user(request: schemas.User, db:Session = Depends(get_db)):
    hashed_pwd = hashing.Hash.bcrypt(request.password)
    new_user = models.User(name = request.name, email = request.email, password = hashed_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('',response_model=List[schemas.ShowUser], tags=['User'])
def all(db:Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@router.get('/{user_id}', response_model=schemas.ShowUser, tags=['User'])
def get_user(user_id:int, db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found!!')
    return user