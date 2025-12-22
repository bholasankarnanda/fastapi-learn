from fastapi import FastAPI
app = FastAPI()

items = {}

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI training!"}

# GET - all items
@app.get("/items/")
def get_items():
    return {"items": items}

# GET - single item by ID
@app.get("/items/{item_id}")
def get_item(item_id: int): 
    item = items.get(item_id)
    if item:
        return {"item": item}
    return {"error": "Item not found"}

# POST - create a new item
@app.post("/items/{item_id}")
def create_item(item_id: int, name: str):
    if item_id in items:
        return {"error": "Item already exists"}
    items[item_id] = name
    return {"message": "Item created", "item": {item_id: name}}

# PUT - update an existing item
@app.put("/items/{item_id}")
def update_item(item_id: int, name: str):
    if item_id not in items:
        return {"error": "Item not found"}
    items[item_id] = name
    return {"message": "Item updated", "item": {item_id: name}}

# DELETE - delete an item
@app.delete("/items/{item_id}")
def delete_item(item_id: int):  
    if item_id not in items:
        return {"error": "Item not found"}
    del items[item_id]
    return {"message": "Item deleted"}

# Query parameter
@app.get("/search")
def search_items(q: str):
    return {"query": q, "type": "query parameter"}
