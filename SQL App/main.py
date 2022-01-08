from fastapi import FastAPI, HTTPException, Depends
from starlette.responses import JSONResponse
from Sqlite_query import SessionLocal, engine
from sqlalchemy.orm import session, Session
from models import Numbers
import crud


app = FastAPI()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# END POINT NO 1
# TODO Read Dependency-Injection
# TODO get input from model


@app.post("/add/{divided}/{factor}")
async def adding_to_db(divided: float, factor: float, db: session = Depends(get_db)):

    if factor == 0:
        raise HTTPException(
            status_code=417, detail="Factor cannot be 0 ")

    result = divided/factor

    Numbers.divided = divided
    Numbers.factor = factor
    Numbers.result = result

    # db.add(Numbers)
    # db.commit()
    # TODO Transaction In DB & Commit Rollback

    return JSONResponse({"Num1": divided, "Num2": factor, "Result": result}, status_code=200)
    # TODO Array in JSON

# END POINT NO 2 :


@app.put("/update/")
async def updating_number(numbers:Numbers, db: session = Depends(get_db)):

    q = db.put(Numbers, id)

    if not q:
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
