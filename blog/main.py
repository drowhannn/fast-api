from fastapi import FastAPI,Depends,status,HTTPException
from . import schemas,models
from .database import engine,SessionLocal
from sqlalchemy.orm import Session
from typing import List

models.Base.metadata.create_all(engine)

app=FastAPI()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/blog',status_code=status.HTTP_200_OK)
def get_all_blogs(db:Session=Depends(get_db)):
    blogs=db.query(models.Blog).all()
    return blogs


@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create_blog(request:schemas.Blog,db:Session=Depends(get_db)):
    new_blog=models.Blog(title=request.title,body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blog/{id}', status_code=status.HTTP_200_OK)
def get_blog(id:int,db:Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with id {id} is not available")
    return blog

@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id:int,db:Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with id {id} is not available")
    blog.delete(synchronize_session=False)
    db.commit()
    return 'done'

@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(id:int,request:schemas.Blog,db:Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with id {id} is not available")
    blog.update(request.dict())
    db.commit()
    return 'updated'



