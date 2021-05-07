from flask import session

from app import app
from models import Food


@app.context_processor
def amount_cart():
    foods = Food.query.filter(Food.id.in_(session['cart']))
    amount = sum(sub.price for sub in foods)
    return dict(foods=foods, amount=amount)
