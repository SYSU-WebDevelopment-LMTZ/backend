from flask import request, make_response, jsonify
from flask_login import login_required, login_user, logout_user, current_user
from . import restaurant
from .. import db
from ..models import Restaurant


@restaurant.route('/', methods=['POST'])
def register():
    if not request.json: # json不存在则返回400
        response = make_response(jsonify({'message' : 'json不存在'}), 400)
        return response

    fields = ['phone', 'password', 'name', 'description', 'logo']
    for item in fields: # json中某些字段缺失则返回400
        if item not in request.json:
            response = make_response(jsonify({'message' : 'restaurant.{}字段不存在'.format(item)}) , 400)
            return response

    phone = request.json['phone']
    password = request.json['password']
    name = request.json['name']
    description = request.json['description']
    logo = request.json['logo']

    if Restaurant.query.filter_by(phone=phone).all(): # 如果json中的电话号码已经被注册过，则返回400
        response = make_response(jsonify({'message' : '电话号码已经被注册过'}), 400)
        return response

    if Restaurant.query.filter_by(name=name).all(): # 如果json中的餐厅名已经被注册过，则返回400
        response = make_response(jsonify({'message' : '餐厅名已经被注册过'}), 400)
        return response

    new_restaurant = Restaurant(phone=phone,
                                password=password,
                                name=name,
                                description=description,
                                image_url=logo)
    db.session.add(new_restaurant)
    db.session.commit()
    response = make_response(jsonify({'message' : '注册成功'}), 200)
    return response


@restaurant.route('/session', methods=['POST'])
def login():
    if not request.json: # json不存在则返回400
        response = make_response(jsonify({'message' : 'json不存在'}), 400)
        return response

    fields = ['phone', 'password']
    for item in fields: # json中某些字段缺失则返回400
        if item not in request.json:
            response = make_response(jsonify({'message' : 'restaurant.{}字段不存在'.format(item)}) , 400)
            return response

    phone = request.json['phone']
    password = request.json['password']

    restaurant = Restaurant.query.filter_by(phone=phone).first()
    if restaurant and restaurant.verify_password(password): # 验证密码
        login_user(restaurant, True) # Flask-Login提供的登陆函数，把该餐厅标记为已登录
        response = make_response(jsonify({'message' : '成功登陆'}), 200)
        return response

    response = make_response(jsonify({'message' : '电话号码或密码不正确'}), 400) # 登陆失败
    return response


@restaurant.route('/session', methods=['DELETE'])
@login_required
def logout():
    logout_user()
    response = make_response(jsonify({'message' : '退出成功'}), 200)
    return response


# # 由于curl是短连接，难以调试登陆功能，因此用下面两个函数测试登陆功能
# @restaurant.route('/login', methods=['GET'])
# def login():
#     if current_user.is_authenticated:
#         return '不要重复登陆'
#     phone = request.args.get('phone')
#     password = request.args.get('password')
#     restaurant = Restaurant.query.filter_by(phone=phone).first()
#     if restaurant and restaurant.verify_password(password): # 验证密码
#         login_user(restaurant, True) # Flask-Login提供的登陆函数，把该餐厅标记为已登录
#         return '成功登陆'
#     return '错误密码'
#
#
# @restaurant.route('/logout')
# def logout():
#     logout_user()
#     return '退出成功'


@restaurant.route('/testlogin')
@login_required
def test_login():
    return 'successful login'


@restaurant.route('/self/info', methods=['GET', 'POST'])
# @login_required
def get_info():
    if request.method == 'GET':
        # if current_user.is_authenticated:
        #     restaurant = current_user._get_current_object()

        #     res = {}
        #     res['phone'] = restaurant.phone
        #     res['name'] = restaurant.name
        #     res['description'] = restaurant.description
        #     res['logo'] = restaurant.image_url

        #     response = make_response(jsonify(res), 200)
        #     return response
        # else:
        #     response = make_response(jsonify({'message' : '获取信息失败'}), 400)
        #     return response
        restaurant = Restaurant.query.first()

        res = {}
        res['phone'] = restaurant.phone
        res['name'] = restaurant.name
        res['description'] = restaurant.description
        res['logo'] = restaurant.image_url

        response = make_response(jsonify(res), 200)
        return response

    elif request.method == 'POST':
        if current_user.is_authenticated:
            if not request.json: # json不存在则返回400
                response = make_response(jsonify({'message' : 'json不存在'}), 400)
                return response
            restaurant = current_user._get_current_object()

            if 'name' in request.json:
                restaurant.name = request.json['name']
            if 'description' in request.json:
                restaurant.description = request.json['description']
            if 'logo' in request.json:
                restaurant.logo = request.json['image_url']
            if 'password' in request.json:
                restaurant.password = request.json['password']

            db.session.add(restaurant)
            db.session.commit()

            response = make_response(jsonify({'message' : '修改成功'}), 200)
            return response
        else:
            response = make_response(jsonify({'message' : '修改信息失败'}), 400)
            return response

