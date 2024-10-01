"""
Main entrypoint to the api
"""

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello from fastapi101/main"}
