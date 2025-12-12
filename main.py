from fastapi import FastAPI,HTTPException
import json
from fastapi import status
from fastapi.responses import JSONResponse
from pydantic import BaseModel,EmailStr,AnyUrl,Field,ValidationError,computed_field
from typing import List,Annotated,Optional
import database_models
from database import engine,session
database_models.Base.metadata.create_all(bind=engine)
app=FastAPI()

def load_data():
    with open("travel.json","r") as f:
        data = json.load(f)
        return data


def save_data(data):
    with open("travel.json","w") as f:
        json.dump(data, f, indent=4)
        


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
        
def init_db():
    db=session()
    data=load_data()
    
    for d in data:
        db_dest = database_models.DestinationDB(**d)
        db.add(db_dest)

    db.commit()  # save all changes
    db.close()
init_db()
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



 
class Destination(BaseModel):
    id: Annotated[int,Field(...,description="ID of the Destination",examples=[1, 2, 3],strict=True)]
    title: Annotated[str,Field(...,description="Title Of Destination",example="Spiti")]
    content: Annotated[str,Field(...,description="About your destination",example="Spots, pricing and how to travel there")]
    comments: Annotated[List[str],Field(...,description="Comments about your destination",example=["Nice location to chill out"])]

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
    
class DestinationUpdate(BaseModel):
    id: Optional[int] = Field(None, description="ID of the Destination", examples=[1, 2, 3], strict=True)
    title: Optional[str] = Field(None, description="Title Of Destination", example="Spiti")
    content: Optional[str] = Field(None, description="About your destination", example="Spots, pricing and how to travel there")
    comments: Optional[List[str]] = Field(None, description="Comments about your destination", example=["Nice location to chill out"])


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