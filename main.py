import json

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Home_work.db'
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    age = db.Column(db.Column)
    email = db.Column(db.String(100))
    role = db.Column(db.String(100))
    phone = db.Column(db.String(100))


class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Order(db.Model):
    __tablename__ = 'order'
    d = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))
    star_date = db.Column(db.String(100))
    end_date = db.Column(db.String(100))
    address = db.Column(db.String(100))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))


with app.app_context():
    db.create_all()


with open('user.json', 'r', encoding='UTF-8') as users:
    for user in json.load(users):
        us = User(**user)
        db.session.add(us)
        db.session.commit()


with open('order.json', 'r', encoding='UTF-8') as orders:
    for order in json.load(orders):
        orde = Order(**order)
        db.session.add(orde)
        db.session.commit()


with open('offers.json', 'r', encoding='UTF-8') as offers:
    for offer in json.load(offers):
        of = Offer(**offer)
        db.session.add(of)
        db.session.commit()


@app.route("/users", method=['GET', 'POST'])
def get_all():
    if request.method == 'GET':
        returned = []
        for i in db.session.query(User).all:
            returned.append({
                "first_name": user.first_name,
                "last_name": user.last_name,
                "age": user.age,
                "email": user.email,
                "role": user.role,
                "phone": user.phone
            })
    elif request.method == 'POST':
        datas = request.json
        for data in datas:
            dat = User(**data)
            db.session.add(dat)
            db.session.commit()
        return 'Completed', 201


@app.route('/users/<int:id>', methods=['PUT', 'DELETE', 'GET'])
def user_by_id(id):
    if request.method == 'GET':
        user = User.query.get(id)
        return jsonify({
            'first_name': user.first_name,
            'last_name': user.last_name,
            'age': user.age,
            'email': user.email,
            'role': user.role,
            'phone': user.phone
        })
    elif request.method == 'PUT':
        user = User.query.get(id)
        data = request.json

        user.first_name = data["first_name"]
        user.last_name = data["last_name"]
        user.age = data['age']
        user.email = data['email']
        user.role = data['role']
        user.phone = data['phone']

        db.session.add(user)
        db.session.commit()
        return 'Completed', 201

    elif request.method == 'DELETE':
        user = User.query.get(id)

        db.session.delete(user)
        db.session.commit()
        return 'Removed', 201


@app.route('/offers', methods=['GET', 'POST'])
def offers_page():
    if request.method == 'GET':
        result = []
        for offer in db.session.query(Offer).all():
            result.append({
                'order_id': offer.order_id,
                'executor_id': offer.executor_id
            })

    elif request.method == 'POST':
        datas = request.json
        for data in datas:
            new_offer = Offer(**data)
            db.session.add(new_offer)
            db.session.commit()
        return 'Completed', 201

@app.route('/offers/<int:id>', methods=['PUT', 'DELETE', 'GET'])
def offers_by_id(id):
    offer = Offer.query.get(id)

    if request.method == 'GET':
        return jsonify({
            'order_id': offer.order_id,
            'executor_id': offer.executor_ide
        })

    elif request.method == 'PUT':
        offer = Offer.query.get(id)
        data = request.json
        offer.order_id = data["order_id"]
        offer.executor_id = data["executor_id"]

        db.session.add(offer)
        db.session.commit()
        return 'Removed', 201

    elif request.method == 'DELETE':
        offer = Offer.query.get(id)
        db.session.delete(offer)
        db.session.commit()
        return 'Removed', 201


@app.route('/orders', methods=['GET', 'POST'])
def orders_page():
    if request.method == 'GET':
        result = []
        for order in db.session.query(Order).all():
            result.append({
                'name': order.name,
                'description': order.description,
                'start_date': order.start_date,
                'end_date': order.end_date,
                'address': order.address,
                'price': order.price
            })
    elif request.method == 'POST':
        datas = request.json
        for data in datas:
            new_orders = Order(**data)
            db.session.add(new_orders)
            db.session.commit()
        return 'Completed', 201


app.run()
