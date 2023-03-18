from fastapi import FastAPI

from typing import Optional

from pydantic import BaseModel

import uvicorn

app = FastAPI()

class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]

@app.get('/blog')
def index(limit=10, published:bool=True, sort:Optional[str]=None):   #query parameters in function parameter
    if published:
        return {'data':f'{limit} published blogs from the db'}
    else:
        return {'data':f'{limit} blogs from the db'}

@app.get('/blog/unpublished')
def unpublished():
    return {'data':'unpublished'}

@app.get('/blog/{id}')        #for dynamic routes
def show(id:int):
    return {'data':id}



@app.get('/blog/{id}/comments')
def comments(id:int, limit=10):
    return {'data':{'1','2'}}

@app.post('/blog')
def create(request: Blog):
    return {'data':f'blog created with title as {request.title}'}


# if __name__ == '__main__':
#     uvicorn.run()