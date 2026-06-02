from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
db = SQLAlchemy()
# =====================================
# USER MODEL
# =====================================
class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(100),
        nullable=False
    )
    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )
    password = db.Column(
        db.String(255),
        nullable=False
    )
    role = db.Column(
        db.String(20),
        default="customer"
    )
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
    products = db.relationship(
        "Product",
        backref="vendor",
        lazy=True
    )
    orders = db.relationship(
        "Order",
        backref="customer",
        lazy=True
    )
    cart_items = db.relationship(
        "Cart",
        backref="user",
        lazy=True
    )
    reviews = db.relationship(
        "Review",
        backref="review_user",
        lazy=True
    )
    def __repr__(self):
        return f"<User {self.name}>"
# =====================================
# PRODUCT MODEL
# =====================================
class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(200),
        nullable=False
    )
    category = db.Column(
        db.String(100),
        nullable=False
    )
    description = db.Column(
        db.Text,
        nullable=False
    )
    price = db.Column(
        db.Float,
        nullable=False
    )
    stock = db.Column(
        db.Integer,
        default=0
    )
    image_url = db.Column(
        db.String(500),
        nullable=False
    )
    average_rating = db.Column(
        db.Float,
        default=0
    )
    total_reviews = db.Column(
        db.Integer,
        default=0
    )
    vendor_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
    reviews = db.relationship(
        "Review",
        backref="product",
        lazy=True,
        cascade="all, delete"
    )
    cart_items = db.relationship(
        "Cart",
        backref="product",
        lazy=True
    )
    order_items = db.relationship(
        "OrderItem",
        backref="product",
        lazy=True
    )
    def __repr__(self):
        return f"<Product {self.name}>"
# =====================================
# CART MODEL
# =====================================
class Cart(db.Model):
    __tablename__ = "cart"
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )
    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False
    )
    quantity = db.Column(
        db.Integer,
        default=1
    )
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
    def subtotal(self):
        return self.quantity * self.product.price
# =====================================
# ORDER MODEL
# =====================================
class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    order_number = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )
    total_amount = db.Column(
        db.Float,
        nullable=False
    )
    status = db.Column(
        db.String(50),
        default="Processing"
    )
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
    order_items = db.relationship(
        "OrderItem",
        backref="order",
        lazy=True,
        cascade="all, delete"
    )
    def __repr__(self):
        return f"<Order {self.order_number}>"
# =====================================
# ORDER ITEM MODEL
# =====================================
class OrderItem(db.Model):
    __tablename__ = "order_items"
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    order_id = db.Column(
        db.Integer,
        db.ForeignKey("orders.id"),
        nullable=False
    )
    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False
    )
    quantity = db.Column(
        db.Integer,
        default=1
    )
    price = db.Column(
        db.Float,
        nullable=False
    )
    def item_total(self):
        return self.quantity * self.price
# =====================================
# REVIEW MODEL
# =====================================
class Review(db.Model):
    __tablename__ = "reviews"
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )
    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False
    )
    rating = db.Column(
        db.Integer,
        nullable=False
    )
    comment = db.Column(
        db.Text
    )
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
    def __repr__(self):
        return f"<Review {self.rating}>"