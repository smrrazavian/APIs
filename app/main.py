"""Main module for division API."""
import os
from pathlib import Path

from typing import List, Optional
import sqlalchemy
import databases
from fastapi import FastAPI, HTTPException
from starlette.responses import JSONResponse
from pydantic import BaseModel

cwd = Path.cwd()
DB_PATH = os.path.join((cwd / "./db/").resolve(), "sample.db")
CONNECTION_PATH = "sqlite:///{DB_PATH}"
database = databases.Database(CONNECTION_PATH)
metadata = sqlalchemy.MetaData()
fractions = sqlalchemy.Table(
    "fractions",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("divided", sqlalchemy.Integer),
    sqlalchemy.Column("factor", sqlalchemy.Integer),
    sqlalchemy.Column("result", sqlalchemy.Float),
)

engine = sqlalchemy.create_engine(
    CONNECTION_PATH, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)


class Fraction(BaseModel):
    """Model for fraction."""
    divided: int
    factor: int = 1


class FractionDetails(Fraction):
    """Model for storing numbers."""
    id: int
    result: int


class FractionRecord(Fraction):
    """"""
    id: int


class FractionUpdate(Fraction):
    """"""
    divided: Optional[int] = None
    factor: Optional[int] = 1


app = FastAPI()


@app.on_event("startup")
async def startup():
    """Connecting to database"""
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    """Disconnecting database"""
    await database.disconnect()


@app.get("/fractions/", response_model=List[FractionDetails])
async def read_fractions():
    """"""
    query = fractions.select()
    return await database.fetch_all(query)


@app.post("/fraction/", response_model=List[Fraction])
async def division(fraction: Fraction):
    """"""
    # --------------------End Point 1--------------------
    factor = fraction.factor
    divided = fraction.divided
    if factor == 0:
        raise HTTPException(status_code=417, detail="Factor cannot be 0 ")
    result = divided / factor
    query = fractions.insert().values(divided=divided, factor=factor, result=result)
    last_record_id = await database.execute(query)
    return JSONResponse(
        {"id": last_record_id, "divided": divided,
            "factor": factor, "result": result},
        status_code=200,
    )


@app.patch("/update/", response_model=List[FractionRecord])
async def updating_number(id: int, numberUpdate: FractionUpdate):
    """"""
    # --------------------End Point 2--------------------
    with Session(engine) as session:
        db_fraction = session.get(FractionRecord, id)
        if not db_fraction:
            raise HTTPException(status_code=404, detail="Fraction not found")
        fraction_data = db_fraction.dict(exclude_unset=True)
        for key, value in db_fraction.items():
            setattr(db_fraction, key, value)
        session.add

# # END POINT NO 3 : READING ID


# @app.get("/show/")
# def read_numbers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     number = crud.get_numbers(db, skip=skip, limit=limit)
#     return number


# @app.get("/show/{id}")
# def read_id(id: int, db: Session = Depends(get_db)):
#     db_number = crud.get_number(db, id=id)
#     if db_number is None:
#         raise HTTPException(status_code=404, detail="number not found")
#     return db_number
