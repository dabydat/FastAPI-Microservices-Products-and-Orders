from urllib.request import Request

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from redis_om import get_redis_connection, HashModel
from starlette.requests import Request
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://127.0.0.1:9000'],
    allow_methods=['*'],
    allow_headers=['*']
)

redis = get_redis_connection(
    host="redis-13703.c16.us-east-1-2.ec2.cloud.redislabs.com",
    port=13703,
    password="EfD0TjlPKSkLDqAjjI8AUybhOMCcrMJU",
    decode_responses=True
)


class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str  # Pending, completed, refunded

    class Meta:
        database = redis


@app.post('/orders')
async def create(request: Request):
    body = await request.json()

    request = requests.get('http://127.0.0.1:8000/products/%s' % body['id'])

    product = request.json()

    order = Order(
        product_id=body['id'],
        price=product['price'],
        fee=0.2 * product['price'],
        total=1.2 * product['price'],
        quantity=body['quantity'],
        status='pending'
    )
    order.save

    return order
