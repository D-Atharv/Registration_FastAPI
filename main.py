from fastapi import FastAPI
from routes.registration import registrationRouter

app = FastAPI()

app.include_router(registrationRouter, prefix='/api/registrations')

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"{name} bewafa hai."}
