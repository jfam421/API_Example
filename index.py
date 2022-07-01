from typing import Optional
from fastapi import FastAPI, Path
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    
class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None

app = FastAPI()

@app.get("/")
def home():
    return{"DATA": "Testing"}

@app.get("/about")
def about():
    return {"DATA": "About"}

inventory = {}
@app.get("/get-item/{item_id}/{name}")
def get_item(item_id: int, name: str):
    return inventory[item_id][f"{name}"]

@app.get("/get-item/{item_id}")
def get_item(item_id: int = Path(None, description="The id of the item you would like to order", gt=0)):
    return inventory[item_id]

@app.get("/get-by-name")
def get_item(*, name: Optional[str] = None):
    for id in inventory:
        if inventory[id].name == name:
            return inventory[id]
        return{"DATA": "Not found!"}

@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        return{"Error":"Item already exist"}

    inventory[item_id] = item
    return inventory[item_id]

@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        return {"Error": "Item does not exist"}

    if item.name != None:
        inventory[item_id].name = item.name
    if item.price != None:
        inventory[item_id].price = item.price
    return inventory[item_id]

@app.delete("/delete-item")
def delete_item(item_id: int):
    if item_id not in inventory:
        return {"Error": "Item does not exist"}
    del inventory[item_id]
