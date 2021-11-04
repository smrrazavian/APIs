from fastapi import FastAPI, HTTPException, Depends
import models
from Sqlite_query import SessionLocal, engine
from sqlalchemy.orm import Session, session
from models import Numbers

models.Base.metadata.create_all(bind=engine)

app  = FastAPI()

def get_db():
    try : 
        db = SessionLocal()
        yield db
    finally :
        db.close()

@app.get("/adding/{a}/{b}")
async def adding_to_db(a: float, b: float, db: session = Depends(get_db)):

    if b == 0 :
        raise HTTPException(status_code=417, detail="The second number cannot be 0 ")

    c = a/b

    numbers = Numbers()
    numbers.num1 = a
    numbers.num2 = b
    numbers.result = c

    db.add(numbers)
    db.commit()
    
    return {"Num1" : a, "Num2": b, "Reseult": c}