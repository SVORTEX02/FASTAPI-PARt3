from fastapi import FastAPI,HTTPException,Depends, Path, Query,Request
import json
from pydantic import BaseModel,Field,ValidationError,computed_field,field_validator,model_validator
from typing import Annotated,Optional
from datetime import date
from fastapi import status
from fastapi.responses import JSONResponse
from db import engine,SessionLocal
from dbmodels import Base
import dbmodels

from sqlalchemy.orm import Session

dbmodels.Base.metadata.create_all(bind=engine)

app=FastAPI()

class BookStore(BaseModel):
    id:Annotated[int,...,Field(gt=0,description="Enter ID of our Book",examples=["1 or 2 or which u want "])]
    title:Annotated[str,...,Field(min_length=4,description="Title of the Book",examples=["Brick To RIck"])]
    author:Annotated[str,...,Field(min_length=2,description="Name of The authro",examples=["Robin"])]
    price:Annotated[float,...,Field(description="Price of the Book",examples=["90","230"])]
    stock:Annotated[int,...,Field(description="Avialable Stock updation")]
    publish_year:Optional[Annotated[int,Field(description="When did this book has published",examples=["2013","2004"])]]
    category:Annotated[str,...,Field(min_length=5,description="Is the fictional or hypothetical",examples=["Ola"])]
    
    class Config:
        orm_mode = True 
        
    @field_validator("price",mode="before")
    @classmethod
    def check_price(cls,v):
        if int(v)<=0:
            raise ValueError("Price Must be Greater Than zero")
        return v
        
    @field_validator("stock",mode="before")
    @classmethod
    def check_stock(cls,v):
        if int(v)<=0:
            raise ValueError("Stock Must be Greater Than Zero")
        return v

    @model_validator(mode="after")
    def category_price_rule(self):
        if self.category.lower() == "programming" and self.price < 300:
            raise ValueError("Programming books must cost at least 300")
        return self
    
    @computed_field
    @property
    def is_available(self) -> bool:
        return self.stock > 0

    @computed_field
    @property
    def is_expensive(self) -> bool:
        return self.price > 700
        
    @computed_field
    @property
    def is_address(self) -> str:
        year = self.publish_year if self.publish_year is not None else "NA"
        return f"{self.author}-{year}-{self.category}"


class BookStoreUpdate(BaseModel):
    id: Optional[int] = Field(None, gt=0, description="Unique ID of the book", examples=[1])
    title: Optional[str] = Field(None, min_length=4, description="Title of the book", examples=["Atomic Habits"])
    author: Optional[str] = Field(None, min_length=2, description="Author name", examples=["James Clear"])
    price: Optional[float] = Field(None, gt=0, description="Price of the book", examples=[299.99])
    stock: Optional[int] = Field(None, ge=0, description="Available stock")
    publish_year: Optional[int] = Field(None, ge=1000, le=2100, description="Year the book was published", examples=[2018])
    category: Optional[str] = Field(None, min_length=3, description="Book category", examples=["Programming"])

    class Config:
        orm_mode=True
        
    @field_validator("price")
    @classmethod
    def validate_price(cls, v):
        if v is not None and v <= 0:
            raise ValueError("Price must be greater than 0")
        return v

    @field_validator("stock")
    @classmethod
    def validate_stock(cls, v):
        if v is not None and v < 0:
            raise ValueError("Stock cannot be negative")
        return v
    



def load_data():
    with open("book_store.json",'r') as f:
        data=json.load(f)
        return data

def save_data(data):
    with open("book_store.json",'w') as f:
        json.dump(data,f,indent=5)


def init_DB():
    db = SessionLocal()
    data=load_data()
    
    for d in data:
        db_dest = dbmodels.Book(**d)
        db.add(db_dest)

    db.commit()  
    db.close()

init_DB()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
@app.get('/bookFromDb')
def get_all_books(db:Session=Depends(get_db)):
    db_books=db.query(dbmodels.Book).all()
    return db_books
        
@app.post('/addBookToDB')
def add_book(book:BookStore,db:Session=Depends(get_db)):
    new_book_data = book.model_dump(exclude={"is_available", "is_expensive", "is_address"})
    new_book_data["full_address"] = book.is_address
    db.add(dbmodels.Book(**new_book_data))
    db.commit()
    return book
        
        

@app.put("/updateBook/{book_id}")
def update_book(book_id: int, book_data: BookStoreUpdate, db: Session = Depends(get_db)):
    db_book = db.query(dbmodels.Book).filter(dbmodels.Book.id == book_id).first()
    if db_book:
        if book_data.title is not None:
            db_book.title = book_data.title
        if book_data.author is not None:
            db_book.author = book_data.author
        if book_data.price is not None:
            db_book.price = book_data.price
        if book_data.stock is not None:
            db_book.stock = book_data.stock
        if book_data.publish_year is not None:
            db_book.publish_year = book_data.publish_year
        if book_data.category is not None:
            db_book.category = book_data.category
        
        db.commit()
        return {"message": "Book updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Book not found")
    
@app.delete("/deleteBook/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(dbmodels.Book).filter(dbmodels.Book.id == book_id).first()
    if db_book:
        db.delete(db_book)
        db.commit()
        return {"message": "Book deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Book not found")
        
        
@app.get("/")
def welcome():
    return {'message':'------------Welcome To Our Book Store API practice-----------'}

@app.get('/initialStaticDb')
def ourData():
    data=load_data()
    return {'OUR DATA':data}


    
   

@app.post("/addbook",status_code=201)
def add_Book(newBook:BookStore):
    data=load_data()
    
    for i in data:
        if i['id']==newBook.id:
            raise HTTPException(status_code=409, detail="Destination already exists")
    new_data=newBook.model_dump()
    data.append(new_data)
    save_data(data)
    return JSONResponse(
        content={
            "message": "Data Added Successfully"
        }
    )

    
@app.put("/updateBook/{book_id}")
def upDate_BooK(book_id:int,upBook:BookStoreUpdate):
    data=load_data()
    
    for i in data:
        if i['id']==book_id:
            new_data=upBook.model_dump(exclude_unset=True)
            
            for key, value in new_data.items(): 
                i[key] = value
            save_data(data)
            return {"message": "book Store Updated"}
    raise HTTPException(status_code=404, detail="Book Not found")

            
@app.delete('/deleteBook/{book_id}')
def deleteBook(book_id:int):
    data=load_data()
    
    for i, book in enumerate(data):
        if book['id'] == book_id:
            data.pop(i) 
            save_data(data)
            return JSONResponse(status_code=200, content={"message": "Book Deleted"})
    
    raise HTTPException(status_code=404, detail="Book Not Found")


@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {
        "received_from": "path",
        "user_id": user_id,
        "type": str(type(user_id))
    }


@app.get("/products")
def get_products(
    name: str | None = None,
    min_price: int | None = None,
    max_price: int | None = None
):
    return {
        "name": name,
        "min_price": min_price,
        "max_price": max_price
    }








# --------------------------------------------------------------
@app.get("/getBook/{book_id}")
def getBoo(book_id:int=Path(...,title="Book Id of Book in my Store",description="Give me in integer value",example='1 or 2 or 3',gt=1)):
    data = load_data()
    for i in data:
        if i['id']==book_id:
            return {"Book Details":i}
        else:
            raise HTTPException(status_code=404,detail="Book ID Not FOund")
        
        
@app.get('/getDetails')
def getDetail(book_id:int=Query(...,title="Book Id of Book in my Store",description="Give me in integer value",example='1 or 2 or 3',gt=0),
            title:str=Query(...,title="Title of the book to given here",description="Give me the title of book",example='The Pragmatic Programmer')
            ):
    
    data = load_data()
    for i in data:
        if i["id"] == book_id and i["title"] == title:
            return {"Book Details": i}

    # raise AFTER loop
    raise HTTPException(status_code=404, detail="Book not found")



@app.post("/text")
async def read_text(request: Request):
    body = await request.body()   
    return {
        "text": body.decode()
    }
