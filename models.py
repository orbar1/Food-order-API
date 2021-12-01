# some models are defined here
from pydantic import BaseModel, Field
from typing import List

# a generic class item for pizza, dessert and drinks
class Item(BaseModel):
    name: str
    description: str
    id: int
    price: int

# class for an order item
class OrderItem(BaseModel):
    id: int
    quantity: int = Field(..., gt=0) # quantity should be greater than zero