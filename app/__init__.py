from flask import Flask
from flask_avatars import Avatars
from flask_sqlalchemy import SQLAlchemy
from settings import config
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
mail = Mail()
avatars = Avatars()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'





#工厂函数
def create_app(config_model):    #通过传入参数来控制环境    如生产环境,开发环境,测试环境
    app = Flask(__name__)
    app.config.from_object(config[config_model])
    config[config_model].init_app(app)

    #初始化拓展
    db.init_app(app)
    mail.init_app(app)
    avatars.init_app(app)
    login_manager.init_app(app)

    #注册蓝本
    from .main import main as main_bp
    from .auth import auth as auth_bp
    from .api import api as api_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp,url_prefix='/auth')
    app.register_blueprint(api_bp, url_prefix='/api')

    return app

