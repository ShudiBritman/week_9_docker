from fastapi import FastAPI
from pydantic import BaseModel
import os
import json


app = FastAPI()


DB_PATH = "db/shopping_list.json"
BIND_MOUNT_PATH = "data/backup_shopping_list.json"

class Item(BaseModel):
    name: str
    quantity: int


def check_database_exists(path) -> None:
    p = os.path.isdir(path)
    if not p:
        save_database(path, [])


def load_database(path):
    try:
        with open(path, "r") as f:
            return list(json.load(f))
    except json.JSONDecodeError:
        raise ValueError("Database file is not valid JSON.")
    

def save_database(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)



@app.on_event("startup")
async def startup_event():
    check_database_exists(DB_PATH)
    check_database_exists(BIND_MOUNT_PATH)



@app.get("/items/")
def get_all_items():
    data = load_database(DB_PATH)
    return data


@app.post("/items/")
def create_item(item: Item):
    data = load_database(DB_PATH)
    if not data:
        last_item_id = 0
    else:
        last_item_id = data[-1]["id"]
    new_item = {
        "id": int(last_item_id) + 1,
        "name": item.name,
        "quantity": item.quantity
    }
    data.append(new_item)
    save_database(DB_PATH, data)
    response = {
        "message":"The item has been successfully added"
    }
    return response


@app.get("/backup/")
def beckup_get_all_items():
    data = load_database(BIND_MOUNT_PATH)
    return data

@app.post("/backup/save/")
def copy_data():
    '''The func copies data from "db/shopping_list" to "data/backup_shopping_list'''
    db_data = load_database(DB_PATH)
    save_database(BIND_MOUNT_PATH, db_data)
    response = {
        "message": "The data was copied successfully."
    }
    return response


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)