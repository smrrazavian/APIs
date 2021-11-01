from fastapi import FastAPI, HTTPException

app  = FastAPI()

@app.get("/{a}/{b}")
async def root(
    a,b
):
    if float(b) == 0 :
        raise HTTPException(status_code=417, detail="The second number cannot be 0 ")

    c = float(a)/float(b)
    return {"Num1" : float(a), "Num2": float(b), "Reseult": c}