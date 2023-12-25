import logging

from flask import Flask, abort
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, logout_user
from flask_mail import Mail
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_siwadoc import SiwaDoc
from flask_cors import CORS
from app.app_log import app_log
from app.common import Result

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
# login.login_view = 'apiAuth.unauthorized_handler'   # 前后端分离项目 不需要此配置
# login.login_message = 'Please log in to access this page.'    # 前后端分离项目 不需要此配置
mail = Mail()
bootstrap = Bootstrap()
siwa = SiwaDoc()

from app.main import bp as main_bp
from app.auth import bp as auth_bp
from app.demo import bp as demo_bp
from app.userManagement import bp as userManagement_bp
from app.databaseManagement import bp as databaseManagement_bp
from app.workbench import bp as workbench_bp
from app.apiAuth import bp as apiAuth_bp
from app.groupManagement import bp as groupManagement_bp


def create_app(config_class=Config):
    print("flask name=", __name__)
    flask_app = Flask(__name__)
    flask_app.config.from_object(config_class)
    flask_app.json.ensure_ascii = False

    db.init_app(flask_app)
    migrate.init_app(flask_app, db)

    login.init_app(flask_app)
    mail.init_app(flask_app)
    bootstrap.init_app(flask_app)
    siwa.init_app(flask_app)
    CORS(flask_app, resources=r'/api/*')  # 配置跨域

    flask_app.register_blueprint(main_bp)
    flask_app.register_blueprint(auth_bp)
    flask_app.register_blueprint(demo_bp)
    flask_app.register_blueprint(userManagement_bp)
    flask_app.register_blueprint(databaseManagement_bp)
    flask_app.register_blueprint(workbench_bp)
    flask_app.register_blueprint(apiAuth_bp)
    flask_app.register_blueprint(groupManagement_bp)

    flask_app.logger.addHandler(app_log.errorHandler())
    flask_app.logger.setLevel(logging.WARNING)

    @flask_app.errorhandler(500)
    def handlerError(e):
        flask_app.logger.error('统一异常捕获，异常信息为：' + str(e))
        return Result.common(500, str(e))

    return flask_app


from app.models import User


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@login.unauthorized_handler
def unauthorized():
    abort(401)
