from flask_login import UserMixin
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db import db


### ------------------------------ Users Table ------------------------------ ###
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)

    order = relationship("Order", back_populates="user")


class Product(db.Model):
    __tablename__ = 'products'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    order_details = relationship("OrderDetails", back_populates="product")


### ------------------------------ Users Table ------------------------------ ###
class Order(db.Model):
    __tablename__ = 'orders'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, db.ForeignKey('users.id'), nullable=False)
    order_complete: Mapped[bool] = mapped_column(Boolean, default=False)

    user = relationship("User", back_populates="order")
    order_details = relationship("OrderDetails", back_populates="order")


class OrderDetails(db.Model):
    __tablename__ = 'order_details'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[int] = mapped_column(Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, db.ForeignKey('products.id'), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    order = relationship("Order", back_populates="order_details")
    product = relationship("Product", back_populates="order_details")











### ------------------------------ User Feedback Table ------------------------------ ###
# !!!  It is completely independent table  !!! #
class UserFeedback(db.Model):
    __tablename__ = 'user_feedback'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(String(100))
    feedback: Mapped[str] = mapped_column(String(500))






