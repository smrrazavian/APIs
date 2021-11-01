from fastapi import FastAPI, HTTPException

app  = FastAPI()

@app.get("/{a}/{b}")
async def root(a: float, b: float):
    if b == 0 :
        raise HTTPException(status_code=417, detail="The second number cannot be 0 ")

    c = a/b
    return {"Num1" : a, "Num2": b, "Reseult": c}
