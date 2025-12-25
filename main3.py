from fastapi import FastAPI,Depends
from pydantic import BaseModel,Field,ValidationError,computed_field,field_validator,model_validator
from typing import Annotated,Optional
from database import SessionLocal,get_db,engine
from sqlalchemy.orm import Session
from database_models import UserDetail
import database_models
from auth import get_password_hash,verify_password,pwd_context 

app=FastAPI()
database_models.Base.metadata.create_all(bind=engine)
class Credit(BaseModel):
    name:Annotated[str,...,Field(min_length=2,max_length=30)]
    password:Annotated[str,...,Field(min_length=2,max_length=14)]
    
    
@app.post("/newdata")
def user_details(user:Credit,db:Session=Depends(get_db)):
    
    new_info=UserDetail(
        name=user.name,
        password=user.password,
        hashed_password=get_password_hash(user.password)
    )
    print(new_info)
    db.add(new_info)
    db.commit()
    db.refresh(new_info)
    return {"message":"Here is the data"}

@app.get("/newdata/{user_id}")
def get_data(user_id:int,db:Session=Depends(get_db)):
    db_destiny=db.query(UserDetail).filter(UserDetail.id==user_id).first()
    info=db_destiny.__dict__
    result=verify_password(info['password'],info['hashed_password'])
    if result:
        print(f"Correct Password:{result}")
    else:
        print(f"Not correct password")
    
    if db_destiny:
        return db_destiny
    return {"message":"Cant Be Done"}

class Login(BaseModel):
    password:Annotated[str,...,Field(min_length=3,max_length=20)]

@app.post("/login")
def login_data(login:Login,db:Session=Depends(get_db)):
    db_destiny=db.query(UserDetail).all()
    for i in db_destiny:
        result = verify_password(login.password,i.hashed_password)
        print(f"Result {result}")
        if result:
            print(f"User Found {i.name}--{i.password}")
            return i
        else:
            print("User Not Found")
            
        

    
