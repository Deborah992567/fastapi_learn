from fastapi import FastAPI , HTTPException , Query , Depends
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy.orm import Session
from multiprocessing.resource_tracker import getfd
import models 
from database import engine , SessionLocal
models.Base.metadata.create_all(bind=engine) 

app = FastAPI()

class Books(BaseModel):
    
    title:str
    author:str
    year_published:int
    is_available:bool
    
def get_db():
        db = SessionLocal()
        try:
            yield db    
        finally:
            db.close()
            
db_dependency = Annotated[Session, Depends(get_db)]            
            
@app.get("/")
def read_books(book_id :int):
    return{"message": "welcome to Book System Management"}


@app.get("/get-books/{book_id}")
async def get_books(book_id:int , db:db_dependency):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book
            
            
@app.post("/create-books")
async def create_book(books:Books , db:db_dependency):
    db_book = models.Book(**books.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

from fastapi import HTTPException



@app.put("/update-books/{book_id}")
async def update_book(book_id: int, updated_book: Books, db: db_dependency):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    # Update the fields
    book.title = updated_book.title
    book.author = updated_book.author
    book.is_available = updated_book.is_available
    book.year_published = updated_book.year_published

    db.commit()
    db.refresh(book)
    
    return {"message": "Book updated successfully", "book": book}


@app.delete("/delete-books/{book_id}")
async def delete_book(book_id: int, db: db_dependency):
    books = db.query(models.Book).filter(models.Book.id==book_id).first()
    if not books:
        raise HTTPException(status_code=404 , detail="books not found")
    db.delete(books)
    db.commit()
    return {"message": "books deleted successfully"}
    
@app.get("/todos/", response_model=list[Books])
async def get_paginated_todos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    books = db.query(models.Book).offset(skip).limit(limit).all()
    return books
            
    

    