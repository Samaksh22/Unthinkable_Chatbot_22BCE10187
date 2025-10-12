from pydantic import BaseModel
from fastapi import FastAPI

class Item(BaseModel):
    name: str
    price: float

    is_offer: bool | None = None
    tax: float | None = 10.5
    description: str | None = None

class User(BaseModel):
    username: str
    full_name: str | None = None

app = FastAPI()

@app.put("/items/")
def create_item(item: Item):
    item_dict = item.model_dump()

    if item.tax:
        price_with_tax = item.price * item.tax / 100 + item.price
        item_dict.update({"price_with_tax": price_with_tax})

    return item_dict

@app.put("/items/")
def update_item(item_id: int, item: Item):
    return {"item_id":item, **item.model_dump()}