from fastapi import FastAPI

app  = FastAPI()

@app.get("/{a}/{b}")
async def root(
    a = 0,
    b = 1 
):
    if float(b) == 0 :
        return """The Second number cannot be 0, Please give another numbers"""
    c = float(a)/float(b)
    return "Num 1 =", float(a),"Num 2 =", float(b),"Reseult =", c