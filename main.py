import CPUinfo.CPUinfo
import Chat.chat
from typing import Union
from fastapi.responses import RedirectResponse
from fastapi import FastAPI
from pydantic import BaseModel
import sys
sys.path.append(r'.\Chat')
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def FirstStartFunc():
    CPUinfo.CPUinfo.GetCPUinfo()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
            }
        }


class MessageBody(BaseModel):
    MessageStr: str

    class Config:
        schema_extra = {
            "MessageStr": "string"
        }


@app.get("/")
async def docs_redirect():
    return RedirectResponse(url='/docs')


@app.post("/Chat")
def read_item(Message: MessageBody):
    response = Chat.chat.ChatBot(Message.MessageStr)
    return {"botMessage": response}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}",
         responses={
             200: {
                 "description": "Item requested by ID",
                 "content": {
                     "application/json": {
                         "example": {"id": "bar", "value": "The bar tenders"}
                     }
                 },
             },
         },)
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results


FirstStartFunc()
