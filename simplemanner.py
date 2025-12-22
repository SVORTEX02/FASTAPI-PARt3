
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
