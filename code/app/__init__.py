from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from config import config


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'


def create_app(config_name):
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    # CORS(app)
    app.config.from_object(config[config_name])
    db.init_app(app)
    login_manager.init_app(app)

    # 注册蓝本
    from .main import main as main_blueprint
    from .restaurant import restaurant as restaurant_blueprint
    from .dish import dish as dish_blueprint
    from .order import order as order_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(restaurant_blueprint, url_prefix='/restaurant')
    app.register_blueprint(dish_blueprint, url_prefix='/dish')
    app.register_blueprint(order_blueprint, url_prefix='/order')

    return app

