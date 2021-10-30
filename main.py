from fastapi import FastAPI

a = 1000
b = 25
c = a/b
resp = """  The fist number is : {}
            The Second Number is : {} 
            Finaly the devision is : {}""".format(a, b, c)

app  = FastAPI()

@app.get("/")
async def root():
    return resp