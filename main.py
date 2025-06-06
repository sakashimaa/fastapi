from fastapi import FastAPI, Body
from pydantic import BaseModel, EmailStr
import uvicorn

app = FastAPI()

class CreateUser(BaseModel):
    email: EmailStr

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

@app.get("/items/")
def list_items():
    return [
        "Item1",
        "Item2",
        "Item3",
        "Item4",
    ]

@app.get("/items/latest/")
def get_latest_item():
    return {
        "item": {
            "id": 0,
            "name": "latest",
        }
    }

@app.post("/users/")
def create_user(user: CreateUser):
    return {
        "message": "success",
        "email": user.email,
    }

@app.get("/items/{item_id}/")
def get_item_by_id(item_id: int):
    return {
        "item": {
            "id": item_id,
        }
    }