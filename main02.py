from fastapi import FastAPI,Path,Query,HTTPException
import json
from pydantic import BaseModel,Field,ValidationError,computed_field,field_validator,model_validator
from typing import Annotated,Optional,List
from fastapi.responses import JSONResponse
app=FastAPI()


def load_data():
    with open('student.json','r') as f:
        data = json.load(f)
        return data
    
def save_data(data):
    with open('student.json','w') as f:
        json.dump(data,f,indent=5)
        
        
@app.get("/")
def home():
    return {"Message":"Welcome To Our Student System"}

@app.get("/students")
def studentsList():
    data=load_data()
    return {"data":data}


@app.get("/student/{stud_id}")
def getStudentById(stud_id:int=Path(...,title="Get particular Student Detail",description="Enter Student Id given by the School",example='1 or 2 or 3 ',gt=0)):
    data = load_data()
    
    for i in data:
        if i['id']==stud_id:
            return {'Student Found':i}
    raise HTTPException(status_code=404,detail="Student Not Found")


class NewStudent(BaseModel):
    id:Annotated[int,...,Field(gt=0,description="Enter the Id of the student",examples=["1","2","or can be anything except a string value"],strict=True)]
    name:Annotated[str,...,Field(min_length=2,max_length=20,description="Enter the Name of New Student",examples=["Shyam Soni","Mehul Gohel"],strict=True)]
    age:Annotated[int,...,Field(gt=0,description="Enter Age of the Student",examples=["2","7"],strict=True)]
    grade:Annotated[str,...,Field(max_length=1,description="Enter Age of the Student",examples=["A","B","C","D"],strict=True)]
    subjects:Annotated[List[str],...,Field(description="Enter the Subjects of the student Want to Study For",examples=["Science","Coding","Cuilanary"])]
    
    
    @field_validator("age",mode="before")
    @classmethod
    def check_Age(cls,v):
        if v<4:
            raise ValueError("School Bhejn ki Zarurat Nhi h ")
        return v
    
    
    
   
@app.post("/createNew")
def createStudent(newStud:NewStudent):
    data=load_data()
    for i in data:
        if i['id']==newStud.id:
            raise HTTPException(status_code=404,detail="Student Not Found")
    new_info=newStud.model_dump()
    data.append(new_info)
    save_data(data)
    return JSONResponse(
        content={
            "message": "Data Added Successfully"
        }
    )
    
class UpStudent(BaseModel):
    name:Optional[Annotated[str,...,Field(min_length=2,max_length=20,description="Enter the Name of New Student",examples=["Shyam Soni","Mehul Gohel"],strict=True)]]
    age:Optional[Annotated[int,...,Field(gt=0,description="Enter Age of the Student",examples=["2","7"],strict=True)]]
    grade:Optional[Annotated[str,...,Field(max_length=1,description="Enter Age of the Student",examples=["A","B","C","D"],strict=True)]]
    subjects:Optional[Annotated[List[str],...,Field(description="Enter the Subjects of the student Want to Study For",examples=["Science","Coding","Cuilanary"])]]
    
    
@app.put("/updateStudent/{stud_id}")
def updateStu(stud:UpStudent,stud_id:int=Path(...,title="Enter id",description="Id of Student To be Updated")):
    data=load_data()
    for i in data:
        if i['id']==stud_id:
            new_info=stud.model_dump(exclude_unset=True)
            for key, value in new_info.items(): 
                i[key] = value
            save_data(data)
            return {"message": "Student Detail Updated"}
    raise HTTPException(status_code=404, detail="Book Not found")
            
            
@app.delete("/deleteStudent/{stud_id}")
def deleteStudent(stud_id:int=Path(...,title="Enter id",description="Id of Student To be Updated")):
    data=load_data()
    for i in data:
        if i['id']==stud_id:
            data.remove(i)
            save_data(data)
            return JSONResponse(status_code=200, content={"message": "Book Deleted"})
    
    raise HTTPException(status_code=404, detail="Book Not Found")

    
    