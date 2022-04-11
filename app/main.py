"""Main module for division API."""
import os
from pathlib import Path

from typing import List
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

numbers = sqlalchemy.Table(
    "numbers",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("divided", sqlalchemy.Integer),
    sqlalchemy.Column("factor", sqlalchemy.Integer),
    sqlalchemy.Column("result", sqlalchemy.Integer),
)

engine = sqlalchemy.create_engine(
    CONNECTION_PATH, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)


class NumberIn(BaseModel):
    """Model for storing numbers."""
    divided: int
    factor: int


class Number(BaseModel):
    """Model for storing numbers."""
    id: int
    divided: int
    factor: int
    result: int


class NumberRead(Number):
    id : int


app = FastAPI()


@app.on_event("startup")
async def startup():
    """Connecting to database"""
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    """Disconnecting database"""
    await database.disconnect()


@app.get("/numbers/", response_model=List[Number])
async def read_numbers():
    """"""
    query = numbers.select()
    return await database.fetch_all(query)


@app.post("/div/", response_model=Number)
async def division(number: NumberIn):
    """"""
    # --------------------End Point 1--------------------
    
    divided = number.divided
    factor = number.factor
    # result = number.result
    if factor == 0:
        raise HTTPException(status_code=417, detail="Factor cannot be 0 ")
    result = divided / factor
    query = numbers.insert().values(divided=divided, factor=factor, result=result)
    last_record_id = await database.execute(query)
    return JSONResponse(
        {"id": last_record_id, "divided": divided, "factor": factor, "result": result},
        status_code=200,
    )


# @app.put("/update/", response_model = NumberRead)
# async def updating_number(numberUpdate: NumberUpdate):
#     # --------------------End Point 2--------------------
#     pass

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
