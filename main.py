from fastapi import FastAPI

a = int(input("First Num :"))
b = int(input("second Num :"))
c = a/b

app  = FastAPI()

@app.get("/")
async def root():
    return c