from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

from items_views import router as items_router
from users.views import router as users_router

app = FastAPI()

app.include_router(items_router)
app.include_router(users_router)

@app.get("/")
def hello_index():
    return {
        "message": "Hello, Index!",
    }

@app.get("/hello/")
def hello(name: str = "world"):
    name = name.strip().title()
    return {
        "message": f"Hello, {name}"
    }

@app.post("/calc/add/")
def add(a: int, b: int):
    return {
        "a": a,
        "b": b,
        "result": a + b,
    }