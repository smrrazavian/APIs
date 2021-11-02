from fastapi import FastAPI, HTTPException
import models
from Sqlite_query import SessionLocal, engine
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)

app  = FastAPI()

@app.get("/division/{a}/{b}")
async def adding_to_db(a: float, b: float):
    if b == 0 :
        raise HTTPException(status_code=417, detail="The second number cannot be 0 ")

    result = a/b
    
    return {"Num1" : a, "Num2": b, "Reseult": result}

