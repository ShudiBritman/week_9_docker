from fastapi import FastAPI
from pydantic import BaseModel
import os
import uvicorn
import json


app = FastAPI()


DB_PATH = "db/shopping_list.json"


class Item(BaseModel):
    name: str
    quantity: int

def check_database_exists() -> None:
    p = os.path.isdir(DB_PATH)
    if not p:
        save_database([])


def load_database() -> list[dict]:
    try:
        with open(DB_PATH, "r") as f:
            return list(json.load(f))
    except json.JSONDecodeError:
        raise ValueError("Database file is not valid JSON.")
    

def save_database(data):
    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=2)



@app.on_event("startup")
async def startup_event():
    check_database_exists()



@app.get("/items/")
def get_all_items():
    data = load_database()
    return data


@app.post("/items/")
def create_item(item: Item):
    data = load_database()
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
    save_database(data)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)