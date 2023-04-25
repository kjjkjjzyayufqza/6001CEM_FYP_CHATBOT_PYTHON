from fastapi.middleware.cors import CORSMiddleware
from CPUinfo.CPUinfo import *
from Chat.chat import *
from ImageRecognition.Prediction_Pictures import *
from isHumanClassifier.isHumanClassifier import *
from typing import Union, Annotated
from fastapi.responses import RedirectResponse, FileResponse, Response
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import sys
sys.path.append(r'.\Chat')


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    response = ChatBot(Message.MessageStr)
    return {"result": True, "botMessage": response}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}


# @app.put("/items/{item_id}",
#          responses={
#              200: {
#                  "description": "Item requested by ID",
#                  "content": {
#                      "application/json": {
#                          "example": {"id": "bar", "value": "The bar tenders"}
#                      }
#                  },
#              },
#          },)
# async def update_item(item_id: int, item: Item):
#     results = {"item_id": item_id, "item": item}
#     return results


@app.post("/files")
async def create_file(image: Annotated[bytes, File()]):
    image_bytes: bytes = image
    isHuman = PredictionisHumanPictures(image_bytes)
    if(isHuman["isHuman"] == True):
        responseText = PredictionPictures(image_bytes)
    else:
        responseText = []
    return {"result": isHuman["isHuman"],
            "message": isHuman["message"],
            "top5Prediction": responseText}


@app.get("/getAllChatClass")
def getAllChatClassByChatBot():
    response = getAllChatClass()
    return {"result": True,  "AllChatClass": response}


@app.get("/SystemInfo")
async def get_SystemInfo():
    return GetCPUinfo()
