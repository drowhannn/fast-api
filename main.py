from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]

@app.get('/')
def index():
    return {'message': 'Hello World'}

@app.post('/blog',response_model=Blog,status_code=201)
def create_blog(request: Blog):
    return request
