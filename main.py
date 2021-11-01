from fastapi import FastAPI, HTTPException
import Sqlite_query

app  = FastAPI()

@app.get("/division/{a}/{b}")
async def adding_to_db(a: float, b: float):
    if b == 0 :
        raise HTTPException(status_code=417, detail="The second number cannot be 0 ")

    result = a/b

    Sqlite_query.cursor.execute("""
        INSERT INTO NUMBER(a, b, Result)
        VALUES({}, {}, {})
    """.format(a, b, result))
    
    return {"Num1" : a, "Num2": b, "Reseult": result}

