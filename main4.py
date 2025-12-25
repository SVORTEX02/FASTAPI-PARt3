from fastapi import FastAPI,Depends,HTTPException,File,UploadFile
from pydantic import Field,ValidationError,computed_field,field_validator,model_validator, BaseModel
from typing import Annotated,Optional
from database import SessionLocal,get_db,engine
from sqlalchemy.orm import Session
import database_models
from database_models import Task
from enum import Enum
from datetime import date
from pathlib import Path
from fastapi.responses import FileResponse

app=FastAPI()
database_models.Base.metadata.create_all(bind=engine)

class TaskStatusEnum(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class Note(BaseModel):
    title: Annotated[str,Field(..., min_length=3, max_length=100)]
    description: Optional[Annotated[str,Field(min_length=3,max_length=100)]]
    priority: Annotated[int,...,Field(..., ge=1, le=5)]
    status: TaskStatusEnum = TaskStatusEnum.PENDING
    due_date: date
    attachment: Optional[Annotated[str,Field(min_length=2,max_length=200)]]
    

    @field_validator("attachment")
    @classmethod
    def validate_file_extension(cls, v):
        if v and not v.endswith((".pdf", ".png", ".jpg")):
            raise ValueError("Attachment must be pdf, png or jpg")
        return v
    
    
    @model_validator(mode="after")
    def check_due_date(self):
        if self.due_date < date.today():
            raise ValueError("Due date cannot be in the past")
        return self
    
class ResponseNote(BaseModel):
    id:int
    title:str
    description:str
    priority:int
    status:TaskStatusEnum 
    
    class Config:
        orm_mode=True
        

@app.get("/")
def home():
    return {"message":"TODO SYSTEM"}

@app.post("/newToDo",response_model=ResponseNote)
def add_todo(task:Note,db:Session=Depends(get_db)):
    new_task=Task(**task.model_dump())
    db.add(new_task)
    print(task)
    print(type(task))
    db.commit()
    db.refresh(new_task)
    return task


@app.get("/getFile/{id}")
def getFile(id:int,db:Session=Depends(get_db)):
    db_file=db.query(Task).filter(Task.id==id).first()
    if db_file.attachment:
            return FileResponse(
                        path=db_file.attachment,
                        media_type="image/png",
                        filename="task_image.jpg"
                    )
    else:
        return {"Message":"Cant BE done"}

    
    

    

