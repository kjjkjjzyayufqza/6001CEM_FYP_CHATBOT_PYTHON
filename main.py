from typing import Union
from fastapi.responses import RedirectResponse
from fastapi import FastAPI

from pydantic import BaseModel


app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

@app.get("/")
async def docs_redirect():
    return RedirectResponse(url='/docs')

@app.post("/Chat")
def read_item(Message: str):
    return "hi"

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}