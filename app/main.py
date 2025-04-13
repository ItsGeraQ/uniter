from typing import Union

from fastapi import FastAPI
#from routers import uniter

app = FastAPI()

#app.include_router(uniter.router)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications! :)"}