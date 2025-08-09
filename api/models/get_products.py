from pydantic import BaseModel, Field


class Product(BaseModel):
    name: str = Field(..., description="Name of new product.", examples=["pizza", "burger"])
    price: float = Field(..., description="Price of new product.", examples=[3.99, 45.0])
    image: str = Field(..., description="Product preview link.", examples=["./assets/burger.svg", "./assets/pizza.svg"])
