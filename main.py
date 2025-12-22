from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI training!"}

@app.get("/hello/{name}")
async def read_hello(name: str):
    return {"message": f"Hello, {name}!"}
