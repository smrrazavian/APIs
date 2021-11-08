from fastapi import FastAPI, HTTPException, Depends
from starlette.responses import JSONResponse
from Sqlite_query import SessionLocal, engine
from sqlalchemy.orm import session, Session
import models
from models import Numbers
import crud
models.Base.metadata.create_all(bind=engine)

app  = FastAPI()

def get_db():
    try : 
        db = SessionLocal()
        yield db
    finally :
        db.close()

# END POINT NO 1
@app.get("/add/{a}/{b}")
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
    
    return JSONResponse({"Num1" : a, "Num2": b, "Reseult": c}, status_code=200)

# END POINT NO 2 #TODO Fix update End-point
@app.patch("/update/{id}/{a}/{b}")
async def updating_number(id : int, a: float, b: float, db: session = Depends(get_db)):

    numbers = Numbers()
    numbers.num1 = a
    numbers.num2 = b
    numbers.id = id

    db = session.put(Numbers, id)
    if not db:
        raise HTTPException(status_code=404, detail="Hero not found")

    hero_data = numbers.dict(exclude_unset=True)

    for key, value in hero_data.items():
        setattr(db, key, value)

    db.commit()
    db.refresh(numbers)
    return numbers

# END POINT NO 3 : READING ID
@app.get("/show/")
def read_numbers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    number = crud.get_numbers(db, skip=skip, limit=limit)
    return number

@app.get("/show/{id}")
def read_id(id: int, db: Session = Depends(get_db)):
    db_number = crud.get_number(db, id=id)
    if db_number is None:
        raise HTTPException(status_code=404, detail="number not found")
    return db_number
