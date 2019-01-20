from flask import request, make_response, jsonify
from flask_login import login_required, current_user
from . import dish
from .. import db
from ..models import Restaurant, Dish, RecommendDish


@dish.route('/', methods=['GET'])
def get_all_dishs():
    dishs = Dish.query.all()

    res = []
    for dish in dishs:
        current = {}
        current['dishid'] = dish.id
        current['name'] = dish.name
        current['price'] = dish.price
        current['imageurl'] = dish.image_url
        current['description'] = dish.description

        res.append(current)

    response = make_response(jsonify(res), 200)
    return response


@dish.route('/<int:id>', methods=['GET'])
def get_dish_detail(id):
    print('id:{}'.format(id))
    dish = Dish.query.filter_by(id=id).first()

    if dish is None:
        response = make_response(jsonify({'message' : '菜品不存在'}), 400)
        return response

    res = {}
    res['dishid'] = dish.id
    res['name'] = dish.name
    res['price'] = dish.price
    res['description'] = dish.description
    res['imageurl'] = dish.image_url

    response = make_response(jsonify(res), 200)
    return response


@dish.route('/', methods=['POST'])
def add_dish():
    if not request.json: # json不存在则返回400
        response = make_response(jsonify({'message' : 'json不存在'}), 400)
        return response

    fields = ['name', 'price', 'description', 'imageurl']
    for item in fields: # json中某些字段缺失则返回400
        if item not in request.json:
            response = make_response(jsonify({'message' : 'dish.{}字段不存在'.format(item)}) , 400)
            return response

    name = request.json['name']
    price = request.json['price']
    description = request.json['description']
    image_url = request.json['imageurl']

    # # 需要登录
    # restaurant = current_user._get_current_object()
    # new_dish = Dish(name=name, price=price, description=description, image_url=image_url, restaurant_id=restaurant.id)

    # 不需要登录（测试用）
    new_dish = Dish(name=name, price=price, description=description, image_url=image_url)

    db.session.add(new_dish)
    db.session.commit()

    response = make_response(jsonify({'message' : '成功添加菜品'}), 200)
    return response


@dish.route('/<int:id>', methods=['PUT', 'DELETE'])
# @login_required
def modify_dish(id):
    if request.method == 'PUT': # 修改菜品详细信息
        if not request.json: # json不存在则返回400
            response = make_response(jsonify({'message' : 'json不存在'}), 400)
            return response

        dish = Dish.query.filter_by(id=id).first()

        if dish is None:
            response = make_response(jsonify({'message' : '菜品不存在'}), 400)
            return response

        if 'name' in request.json:
            dish.name = request.json['name']
        if 'price' in request.json:
            dish.price = request.json['price']
        if 'description' in request.json:
            dish.description = request.json['description']
        if 'imageurl' in request.json:
            dish.image_url = request.json['imageurl']

        db.session.add(dish)
        db.session.commit()

        response = make_response(jsonify({'message' : '修改菜品信息成功'}), 200)
        return response

    elif request.method == 'DELETE':
        dish = Dish.query.filter_by(id=id).first()

        if dish is None:
            response = make_response(jsonify({'message' : '菜品不存在'}), 400)
            return response

        db.session.delete(dish)
        db.session.commit()

        response = make_response(jsonify({'message' : '删除菜品成功'}), 200)
        return response

@dish.route('/recommendation', methods=['GET'])
def get_recommendation():
    recommendation_dishs = RecommendDish.query.all()

    res = []
    for dish in recommendation_dishs:
        current = {}
        current['id'] = dish.id
        current['dishid'] = dish.dish_id
        current['discription'] = dish.description

        res.append(current)

    response = make_response(jsonify(res), 200)
    return response


@dish.route('/recommendation', methods=['POST'])
# @login_required
def modify_recommendation():
    if not request.json: # json不存在则返回400
        response = make_response(jsonify({'message' : 'json不存在'}), 400)
        return response

    fields = ['dishid', 'description']
    for item in fields: # json中某些字段缺失则返回400
        if item not in request.json:
            response = make_response(jsonify({'message' : 'recommendation.{}字段不存在'.format(item)}) , 400)
            return response

    dish_id = request.json['dishid']
    description = request.json['description']

    dish = Dish.query.filter_by(id=dish_id).first()
    if dish is None:
        response = make_response(jsonify({'message' : '菜品不存在'.format(item)}) , 400)
        return response

    new_recommendation = RecommendDish(dish_id=dish_id, description=description)

    db.session.add(new_recommendation)
    db.session.commit()

    response = make_response(jsonify({'message' : '添加推荐菜品成功'}), 200)
    return response


@dish.route('/recommendation/<int:id>', methods=['DELETE'])
# @login_required
def delete_recommendation(id):
    recommendation = RecommendDish.query.filter_by(id=id).first()

    if recommendation is None:
        response = make_response(jsonify({'message' : '推荐菜品不存在'}), 400)
        return response

    db.session.delete(recommendation)
    db.session.commit()

    response = make_response(jsonify({'message' : '成功删除推荐菜品'}), 200)
    return response

