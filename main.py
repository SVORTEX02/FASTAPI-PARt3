from fastapi import FastAPI,HTTPException,Depends
import json
from fastapi import status
from fastapi.responses import JSONResponse
from pydantic import BaseModel,EmailStr,AnyUrl,Field,ValidationError,computed_field
from typing import List,Annotated,Optional
import database_models
from database import engine
from database import SessionLocal
from sqlalchemy.orm import Session
database_models.Base.metadata.create_all(bind=engine)
app=FastAPI()


class Destination(BaseModel):
    id: Annotated[int,Field(...,description="ID of the Destination",examples=[1, 2, 3],strict=True)]
    title: Annotated[str,Field(...,description="Title Of Destination",example="Spiti")]
    content: Annotated[str,Field(...,description="About your destination",example="Spots, pricing and how to travel there")]
    comments: Annotated[List[str],Field(...,description="Comments about your destination",example=["Nice location to chill out"])]
    
    

class DestinationUpdate(BaseModel):
    id: Optional[int] = Field(None, description="ID of the Destination", examples=[1, 2, 3], strict=True)
    title: Optional[str] = Field(None, description="Title Of Destination", example="Spiti")
    content: Optional[str] = Field(None, description="About your destination", example="Spots, pricing and how to travel there")
    comments: Optional[List[str]] = Field(None, description="Comments about your destination", example=["Nice location to chill out"])

    class Config:
        orm_mode = True 

def load_data():
    with open("travel.json","r") as f:
        data = json.load(f)
        return data


def save_data(data):
    with open("travel.json","w") as f:
        json.dump(data, f, indent=4)
        


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# y jo bhi funciton isse hmne pehle toh session establish kia
# fir session k baad hmne db models m json file ko bheja ya toh pydatnic model ka object bhi pass kr skte h
# fir add comit kia 
# def init_db():
#     db=session()
#     data=load_data()
    
#     for d in data:
#         db_dest = database_models.DestinationDB(**d)
#         db.add(db_dest)

#     db.commit()  
#     db.close()
# init_db()
@app.get('/destinyDb')
def get_All_destinations(db: Session = Depends(get_db)):
    db_destinations = db.query(database_models.DestinationDB).all()
    return db_destinations


@app.get('/destiny_id/{destiny_id}')
def get_dest_by_id(destiny_id:int,db: Session = Depends(get_db)):
    db_destiny=db.query(database_models.DestinationDB).filter(database_models.DestinationDB.id==destiny_id).first()
    if db_destiny:
        return db_destiny
    return "Destination Not Found"



@app.post('/add_destiny')
def add_destiny(dest:Destination,db: Session = Depends(get_db)):
    db.add(database_models.DestinationDB(**dest.model_dump()))
    db.commit()
    return dest    


@app.put('/update_destiny/{destiny_id}')
def updating_destination(id:int,dest:DestinationUpdate,db: Session = Depends(get_db)):
    db_destiny=db.query(database_models.DestinationDB).filter(database_models.DestinationDB.id==id).first()
    if db_destiny:
        db_destiny.title=dest.title
        db_destiny.content=dest.content
        db_destiny.comments=dest.comments
        db.commit()
    else:
        return "Destination Not Found"


@app.delete('/delete_destiny/{id}')
def delete_destiny(id: int, db: Session = Depends(get_db)):
    db_destiny = db.query(database_models.DestinationDB).filter(database_models.DestinationDB.id == id).first()
    
    if not db_destiny:
        raise HTTPException(status_code=404, detail="Destination not found")
    
    db.delete(db_destiny)
    db.commit()




















# ----------------------------------SIMPLE JSON FILE CURD -------------------------------------
@app.get("/")
def welcome():
    return {'message':'Welcome TO Travel APIs'}

@app.get('/destinations')
def dest():
    data=load_data()
    formatted = [
        f"{item['id']} - {item['title']} - {item['content']} - {item['comments']}"
        for item in data
    ]

    return {"destinations": formatted}



@app.post('/add_dest',status_code=201)
def create(dest:Destination):
    data=load_data()
    
    for i in data:
        if i['id'] == dest.id:
            raise HTTPException(status_code=409, detail="Destination already exists")
        
    new_data=dest.model_dump()
    data.append(new_data)
    save_data(data)
    
    return {"message": "Destination added successfully", "data": new_data}
    


@app.put('/edit-dest/{dest_id}')
def update_dest(dest_id:int,dest:DestinationUpdate):
    data=load_data()
    
    for item in data:
        if item['id'] == dest_id:
            new_data = dest.model_dump(exclude_unset=True)
            
            
            for key, value in new_data.items():
                item[key] = value

            save_data(data)
            return {"message": "Destination Updated", "updated": item}

    raise HTTPException(status_code=404, detail="Destination not found")


@app.delete('/del-dest/{dest_id}')
def delete_destination(dest_id:int,):
    data = load_data()  

    for i, item in enumerate(data):
        if item["id"] == dest_id:
            data.pop(i)           
            save_data(data)      
            return JSONResponse(status_code=200, content={"message": "Destination deleted"})
    
    # If no item found
    raise HTTPException(status_code=404, detail="Destination not found")