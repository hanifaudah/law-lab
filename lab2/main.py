from typing import Optional

from fastapi import Body, FastAPI, Form
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.get("/soal1")
def soal1(a: str, b: str):
  return {"result": a + b}

class Model(BaseModel):
  a: str
  b: str

@app.post("/soal2")
async def soal2(a: str = Form(...), b: str = Form(...)):
  return {"result": a + b}

@app.post("/soal3")
async def soal3(model: Model):
  return {"result": model.a + model.b}