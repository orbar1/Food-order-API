# importing all the required libraries
from typing import List
from fastapi import FastAPI, HTTPException, Request
import uvicorn
from helpers import build_data
from datetime import datetime, timedelta
from time import sleep
import logging
from models import Item, OrderItem

# time to update data
TIME_TO_UPDATE_DATA = timedelta(days=1)
LAST_UPDATE = datetime.now()

data = build_data()

#function to update data
def update_data():
    global data
    data = build_data()
    print("Updated Data")

# initializing the App
app = FastAPI()

# updating data time to time
@app.middleware("http")
async def updating_data_if_needed(request: Request, call_next):
    global LAST_UPDATE
    if datetime.now() - LAST_UPDATE > TIME_TO_UPDATE_DATA:
        update_data()
        LAST_UPDATE = datetime.now()
    response = await call_next(request)
    return response

# defining routes

# route for fetching all items in the given category
@app.get("/drinks")
def get_drinks():
    response = list(data["drinks"].values())
    return {"drinks" : response}

# route for fetching by ID
@app.get("/drink/{id}")
def get_drink_by_id(id: int):
    if not data["drinks"].get(id):
        return HTTPException(404, "No drinks with that ID found")
    return data["drinks"].get(id)

# route for fetching all items in the given category
@app.get("/desserts")
def get_desserts():
    response = list(data["desserts"].values())
    return {"desserts" : response}

# route for fetching by ID
@app.get("/dessert/{id}")
def get_dessert_by_id(id: int):
    if not data["desserts"].get(id):
        return HTTPException(404, "No dessert with that ID found")
    return data["desserts"].get(id)

# route for fetching all items in the given category
@app.get("/pizzas")
def get_pizzas():
    response = list(data["pizzas"].values())
    return {"pizzas" : response}

# route for fetching by ID
@app.get("/pizza/{id}")
def get_pizza_by_id(id: int):
    if not data["pizzas"].get(id):
        return HTTPException(404, "No pizza with that ID found")
    return data["pizzas"].get(id)

# route for placing an order and getting a price
@app.post("/orders")
def place_order(drinks: List[OrderItem], desserts: List[OrderItem], pizzas: List[OrderItem]):
    
    # checking if valid info is provided or not
    for drink in drinks:
        if not data["drinks"].get(drink.id):
            return HTTPException(404, "item(s) not found")
    for dessert in desserts:
        if not data["desserts"].get(dessert.id):
            return HTTPException(404, "item(s) not found")
    for pizza in pizzas:
        if not data["pizzas"].get(pizza.id):
            return HTTPException(404, "item(s) not found")


    total_price = 0

    # calculating the price
    for drink in drinks:
        total_price += data["drinks"][drink.id]["price"] * drink.quantity
    for dessert in desserts:
        total_price += data["desserts"][dessert.id]["price"] * dessert.quantity
    for pizza in pizzas:
        total_price += data["pizzas"][pizza.id]["price"] * pizza.quantity

    return {"price": total_price}


if __name__ == "__main__":
    uvicorn.run(f"{__name__}:app", reload=True)