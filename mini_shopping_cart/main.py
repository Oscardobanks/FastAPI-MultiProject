from fastapi import FastAPI, HTTPException, Query
from typing import List
import math

from cart import Product, CartItem, load_products, load_cart, save_cart

app = FastAPI()


@app.post("/cart/add", response_model=CartItem)
def add_to_cart(product_id: int = Query(gt=-1), qty: int = Query(gt=0)):
    products = load_products()
    cart = load_cart()
    product = next((p for p in products if p.id == product_id), None)
    if not product:
        raise HTTPException(
            status_code=404, detail="Product not found in catalog.")

    # Check if already in cart
    cart_item = next(
        (item for item in cart if item.product_id == product_id), None)
    if cart_item:
        cart_item.quantity += qty
        total_price = math.ceil(cart_item.quantity * cart_item.price)
        cart_item.total = f"${total_price}"
    else:
        cart_item = CartItem.from_cart(product, qty)
        cart.append(cart_item)
    save_cart(cart)
    return cart_item


# Checkout cart items
@app.get("/cart/checkout", response_model=List[CartItem])
def view_cart():
    cart = load_cart()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart is empty")
    return cart

# Get all Products


@app.get("/products/", response_model=List[Product])
def view_products():
    products = load_products()
    if not products:
        raise HTTPException(status_code=404, detail="There are no products")
    return products
