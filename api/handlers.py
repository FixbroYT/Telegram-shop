from typing import List

import stripe
from fastapi import APIRouter, HTTPException

from api.models.get_products import Product
from api.models.pay import PayRequest, PayResponse
from config import STRIPE_APIKEY, FRONTEND_URL
from database import requests as rq

router = APIRouter()

stripe.api_key = STRIPE_APIKEY

@router.get("/get_products", response_model=List[Product])
async def get_products():
    products = await rq.get_all_products()

    if not products:
        raise HTTPException(status_code=500, detail="There are no products in the database at the moment")

    return products

@router.post("/create-checkout-session", response_model=PayResponse)
async def create_checkout_session(data: PayRequest):
    products = await rq.get_products_from_db(data.products)

    if not products:
        raise HTTPException(status_code=500, detail="Payment failed, products not found in the database")

    line_items = []
    for product in products:
        line_items.append({
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": product.name.capitalize(),
                },
                "unit_amount": int(product.price * 100)
            },
            "quantity": 1,
        })

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=f'{FRONTEND_URL}/success',
        cancel_url=f'{FRONTEND_URL}/fail',
    )

    return {"url": session.url}