from fastapi import FastAPI, Depends

from . import schemas, models

from .database import engine, SessionLocal

from sqlalchemy.orm import Session

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


models.Base.metadata.create_all(bind = engine)

@app.post('/blog')
def create(request: schemas.Blog, db: Session = Depends(get_db)): #Depends converts the parameter to pydantic, thsi is used to make interpreter know that it is not a parameter
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog
#{'title':request.title, 'body':request.body}