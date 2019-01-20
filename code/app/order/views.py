from flask import request, make_response, jsonify
from flask_login import login_required, current_user
from . import order
from .. import db
from ..models import Restaurant, Dish, Order


@order.route('/', methods=['GET'])
# @login_required
def get_all_orders():
    orders = Order.query.all()

    state2str = ['non-pay', 'paid', 'ready']

    res = []
    for order in orders:
        current = {}
        current['orderid'] = order.id
        current['tableid'] = order.table_id
        current['state'] = state2str[order.state]
        current['price'] = order.price
        current['ordertime'] = order.time
        dishs = order.dishs.all()
        all_dish = []
        for dish in dishs:
            tmp = {}
            dish_obj = Dish.query.filter_by(id=dish.dish_id).first()
            tmp['dishname'] = dish_obj.name
            tmp['dishcount'] = dish.dish_count
            all_dish.append(tmp)
        current['dishes'] = all_dish
        current['note'] = order.note

        res.append(current)

    response = make_response(jsonify(res), 200)
    return response


@order.route('/<int:id>/info', methods=['GET'])
# @login_required
def get_order_detail(id):
    order = Order.query.filter_by(id=id).first()

    if order is None:
        respose = make_response(jsonify({"message", "订单不存在"}), 400)
        return response

    state2str = ['non-pay', 'paid', 'ready']
    dishs = order.dishs.all()

    res = {}
    res['orderid'] = order.id
    res['tableid'] = order.table_id
    res['state'] = state2str[order.state]
    res['price'] = order.price
    res['ordertime'] = order.time
    all_dish = []
    for dish in dishs:
        tmp = {}
        tmp['dishid'] = dish.dish_id
        tmp['dishcount'] = dish.dish_count
        all_dish.append(tmp)
    res['dishes'] = all_dish
    res['note'] = order.note

    response = make_response(jsonify(res), 200)
    return response


@order.route('/<int:id>/payment', methods=['POST'])
def pay_order(id):
    if not request.json: # json不存在则返回400
        response = make_response(jsonify({'message' : 'json不存在'}), 400)
        return response

    if 'price' not in request.json:
        response = make_response(jsonify({'message' : 'price字段不存在'}) , 400)
        return response

    order = Order.query.filter_by(id=id).first()

    if order is None:
        response = make_response(jsonify({"message" : "订单不存在"}), 400)
        return response

    if order.state != 0:
        response = make_response(jsonify({"message" : "不要重复支付"}), 400)
        return response

    money = request.json['price']
    if abs(money - order.price) > 1e-6:
        response = make_response(jsonify({"message" : "支付金额错误"}), 400)
        return response

    order.state = 1

    db.session.add(order)
    db.session.commit()

    response = make_response(jsonify({"message" : "成功支付"}), 200)
    return response


@order.route('/', methods=['POST'])
def submit_order():
    if not request.json: # json不存在则返回400
        response = make_response(jsonify({'message' : 'json不存在'}), 400)
        return response

    fields = ['restaurant_id', 'tableid', 'dishes', 'note']
    for item in fields: # json中某些字段缺失则返回400
        if item not in request.json:
            response = make_response(jsonify({'message' : 'order.{}字段不存在'.format(item)}) , 400)
            return response

    tableid = request.json['tableid']
    restaurant_id = request.json['restaurant_id']

    price = 0.0
    dishs = []
    counts = []
    print(request.json)
    for item in request.json['dishes']:
        id = item['dishid']
        dish_count = item['count']
        dish = Dish.query.filter_by(id=id).first()
        if dish is None:
            response = make_response(jsonify({'message' : 'dishid:{}不存在'.format(id)}), 400)
            return response
        if dish_count <= 0:
            response = make_response(jsonify({'message' : 'dish_count <= 0'}), 400)
            return response
        price += dish.price * dish_count
        dishs.append(dish)
        counts.append(dish_count)

    note = request.json['note']

    new_order = Order(table_id=tableid, restaurant_id=restaurant_id, price=price, note=note)
    db.session.add(new_order)
    db.session.commit()
    for i in range(len(dishs)):
        new_order.add_dish(dishs[i], counts[i])

    response = make_response(jsonify({'orderid' : new_order.id}), 200)
    return response


@order.route('/<int:id>', methods=['POST'])
# @login_required
def handle_order(id):
    if not request.json: # json不存在则返回400
        response = make_response(jsonify({'message' : 'json不存在'}), 400)
        return response

    if 'state' not in request.json:
        response = make_response(jsonify({'message' : 'state字段不存在'}) , 400)
        return response

    order = Order.query.filter_by(id=id).first()
    if order is None:
        response = make_response(jsonify({'message' : '订单'}) , 400)
        return response

    order.state = request.json['state']

    db.session.add(order)
    db.session.commit()

    response = make_response(jsonify({"message" : "处理订单成功"}), 200)
    return response

