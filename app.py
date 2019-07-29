import os

from dotenv import load_dotenv
from marshmallow import fields

from sqlalchemy.ext.automap import automap_base
# from sqlalchemy.orm import Session
# from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

if os.path.exists('.env'):
    load_dotenv('.env')

app = Flask(__name__)


#################################################
# Database Setup
#################################################
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '')
# print(app.config['SQLALCHEMY_DATABASE_URI'])

db = SQLAlchemy(app)
ma = Marshmallow(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

# Save references to each table
Products = Base.classes.products
Purchases = Base.classes.purchases
Purchase_Items = Base.classes.purchase_items
Users = Base.classes.users

# Product Schema
class ProductSchema(ma.Schema):
    price = fields.Decimal(as_string=True)

    class Meta:
        model = Products
        fields = ('id', 'title', 'price', 'tags')

# Purchase Schema
class PurchaseSchema(ma.Schema):
    class Meta:
        model = Purchases
        # price = ma.fields.Decimal(as_string=True)
        fields = ('id', 'name', 'address', 'state', 'zipcode', 'user_id')

# Purchase_Item Schema
class PurchaseItemSchema(ma.Schema):
    price = fields.Decimal(as_string=True)

    class Meta:
        model = Purchase_Items
        fields = ('id', 'purchase_id', 'product_id', 'price', 'quantity', 'state')

# User Schema
class UserSchema(ma.Schema):
    class Meta:
        model = Users
        # price = ma.fields.Decimal(as_string=True)
        fields = ('id', 'email', 'details')

# Init schemas
product_schema = ProductSchema(strict=True)
products_schema = ProductSchema(many=True, strict=True)
purchase_schema = PurchaseSchema(strict=True)
purchases_schema = PurchaseSchema(many=True, strict=True)
purchase_item_schema = PurchaseItemSchema(strict=True)
purchase_items_schema = PurchaseItemSchema(many=True, strict=True)
user_schema = UserSchema(strict=True)
users_schema = UserSchema(many=True, strict=True)

@app.route("/")
def index():
    # """Return the homepage."""
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/products<br/>"
        f"/products/&lt;title&gt;<br/>"
        f"/purchase_items<br/>"
        f"/purchase_items/&lt;id&gt;<br/>"
        f"/purchases<br/>"
        f"/purchases/&lt;id>&gt;<br/>"
        f"/users<br/>"
        f"/users/&lt;id&gt;"
    )

@app.route("/products")
def products():
    """Return a list of products"""
    all_rows = db.session.query(Products).all()
    result = products_schema.dump(all_rows)

    return jsonify(result.data)

@app.route("/products/<id>")
def product(id):
    """Return a product by id"""
    product = db.session.query(Products).filter(Products.id == id).scalar()
    return product_schema.jsonify(product)

@app.route("/purchases")
def purchases():
    """Return a list of purchases"""
    all_rows = db.session.query(Purchases).all()
    result = purchases_schema.dump(all_rows)

    return jsonify(result.data)

@app.route("/purchases/<id>")
def purchase(id):
    """Return a purchase by id"""
    purchase = db.session.query(Purchases).filter(Purchases.id == id).scalar()
    return purchase_schema.jsonify(purchase)

@app.route("/purchase_items")
def purchase_items():
    """Return a list of purchase items"""
    all_rows = db.session.query(Purchase_Items).all()
    result = purchase_items_schema.dump(all_rows)

    return jsonify(result.data)

@app.route("/purchase_items/<id>")
def purchase_item(id):
    """Return a purchase item by id"""
    purchase_item = db.session.query(Purchase_Items).filter(Purchase_Items.id == id).scalar()
    return purchase_item_schema.jsonify(purchase_item)

@app.route("/users")
def users():
    """Return a list of users"""
    all_rows = db.session.query(Users).all()
    result = users_schema.dump(all_rows)

    return jsonify(result.data)

@app.route("/users/<id>")
def user(id):
    """Return a user by id"""
    user = db.session.query(Users).filter(Users.id == id).scalar()
    return user_schema.jsonify(user)

@app.route("/products2")
def get_products():
    """Return a list of products."""
    sel = [
        Products.id,
        Products.title,
        Products.price,
        Products.tags
    ]

    results = db.session.query(*sel).all()
    # Create a dictionary from the row data and append to a list of all_products
    all_products = []
    for id, title, price, tags in results:
        product = {}
        product["id"] = id
        product["title"] = title
        product["price"] = str(price)
        product["tags"] = tags
        all_products.append(product)

    return jsonify(all_products)


@app.route("/products2/<id>")
def get_product(id):
    """Return a product by id."""
    sel = [
        Products.id,
        Products.title,
        Products.price,
        Products.tags
    ]

    results = db.session.query(*sel).filter(Products.id == id).all()
  
    # Create a dictionary entry for each row of product information
    product = {}
    for id, title, price, tags in results:
        product["id"] = id
        product["title"] = title
        product["price"] = str(price)
        product["tags"] = tags

    return jsonify(product)


if __name__ == "__main__":
    app.run()
