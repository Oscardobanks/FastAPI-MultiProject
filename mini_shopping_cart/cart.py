import json
import os
from pydantic import BaseModel
from typing import List
import math

PRODUCTS_FILE = "products.json"
CART_FILE = "cart.json"


class Product(BaseModel):
    id: int
    name: str
    price: float


class CartItem(BaseModel):
    product_id: int
    name: str
    price: float
    quantity: int
    total: str

    @staticmethod
    def calculate_total(qty: int, price: float) -> float:
        if not qty or not price:
            return 0.0
        return math.ceil(qty * price)

    @classmethod
    def from_cart(cls, product: Product, qty: int):
        total_price = cls.calculate_total(qty, product.price)
        return cls(product_id=product.id, name=product.name, price=product.price, quantity=qty, total=(f"${total_price}"))

# Save cart item data to JSON file


def save_cart(cart: List[CartItem]):
    with open(CART_FILE, "w") as file:
        json.dump([item.model_dump() for item in cart], file, indent=2)

# Load product & cart data from JSON


def load_products() -> List[Product]:
    if os.path.exists(PRODUCTS_FILE):
        with open(PRODUCTS_FILE, "r") as file:
            content = file.read().strip()
            if not content:
                return []
            try:
                data = json.loads(content)
                return [Product(**d) for d in data]
            except json.JSONDecodeError:
                return []
    return []


def load_cart() -> List[CartItem]:
    if os.path.exists(CART_FILE):
        with open(CART_FILE, "r") as file:
            content = file.read().strip()
            if not content:
                return []
            try:
                data = json.loads(content)
                return [CartItem(**d) for d in data]
            except json.JSONDecodeError:
                return []
    return []
