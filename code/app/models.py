from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db
from . import login_manager


# class Customer(db.Model):
#     __tablename__ = 'customers'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64), unique=True)
#     orders = db.relationship('Order', backref='customer') # 一个顾客对应多个订单
#
#     def __repr__(self):
#         return '<Customer {}[{}]'.format(self.name, self.order_id)


# # Order和Dish是多对多关系, orderdishs作为联结表
# orderdishs = db.Table('orderdishs',
#                       db.Column('order_id', db.Integer, db.ForeignKey('orders.id')),
#                       db.Column('dish_id', db.Integer, db.ForeignKey('dishs.id')))


class OrderDish(db.Model):
    __tablename__ = 'orderdishes'
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), primary_key=True)
    dish_id = db.Column(db.Integer, db.ForeignKey('dishs.id'), primary_key=True)
    dish_count = db.Column(db.Integer, default=1)


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    table_id = db.Column(db.Integer, default=0)
    # customer_id = db.Column(db.Integer, db.ForeignKey('customers.id')) # 订单和顾客是多对一关系
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), default=1) # 订单和餐厅是多对一关系
    dishs = db.relationship('OrderDish',
                            foreign_keys=[OrderDish.order_id],
                            backref=db.backref('order', lazy='joined'),
                            lazy='dynamic',
                            cascade='all, delete-orphan')
    state = db.Column(db.Integer, default=0) # 0未支付 1已支付 2可取餐
    price = db.Column(db.Float, nullable=False)
    note = db.Column(db.Text) # 顾客的备注
    time = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Order id:{}\tcustomer:{}\ttime:{}>'.format(self.id, self.customer_id, self.time)

    def add_dish(self, dish, dish_count=1):
        if not self.has_include(dish):
            od = OrderDish(order_id=self.id, dish_id=dish.id, dish_count=dish_count)
            db.session.add(od)

    def has_include(self, dish):
        return self.dishs.filter_by(dish_id=dish.id).first() is not None


class Dish(db.Model):
    __tablename__ = 'dishs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(64))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), default=1) # 菜品和餐厅是多对一关系
    orders = db.relationship('OrderDish',
                             foreign_keys=[OrderDish.dish_id],
                             backref=db.backref('dish', lazy='joined'),
                             lazy='dynamic',
                             cascade='all, delete-orphan')

    def __repr__(self):
        return '<Dish id:{}\tname:{}>'.format(self.id, self.name)


class RecommendDish(db.Model):
    __tablename__ = 'recommenddishs'
    id = db.Column(db.Integer, primary_key=True)
    dish_id = db.Column(db.Integer, db.ForeignKey('dishs.id')) # 推荐菜品和菜品是一对一关系
    description = db.Column(db.Text)

    def __repr__(self):
        return '<Recommend id:{}\tdish_id:{}>'.format(self.id, self.name)


class Restaurant(UserMixin, db.Model):
    __tablename__ = 'restaurants'
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(11), unique=True)
    password_hash = db.Column(db.String(64))
    name = db.Column(db.String, unique=True)
    description = db.Column(db.Text)
    dishs = db.relationship('Dish', backref='restaurant')
    orders = db.relationship('Order', backref='restaurant')
    image_url = db.Column(db.String(64))

    def __repr__(self):
        return '<Restaurant id:{}\tname:{}>'.format(self.id, self.name)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password) # 加密餐厅密码

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password) # 确认密码


# 为Flask-Login实现的回调函数
@login_manager.user_loader
def load_user(id):
    restaurant = Restaurant.query.filter_by(id=id).first()
    return restaurant

