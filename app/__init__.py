from flask import Flask
from .extensions import jwt
from app.api.register_app import register_app
from app.models.user_model import TokenBlockList, UserModel
from app.register_cli import register_cli
from app.web.register_app import register_app_web
from settings import Config
from app.lib.date_time import *
from app.register_filters import register_filters
from .extensions import login_manager


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.json_provider_class.sort_keys = False

    extended_ext(app)
    register_app(app)
    register_app_web(app)
    register_cli(app)
    # loginManager(app)

    register_filters(app)

    # login_manager.session_protection = "strong"
    login_manager.login_view = "auth2.login"
    login_manager.login_message = (
        f"Ma'af...!!!\\nSilahkan Login Untuk Mengakses Halaman Ini."
    )
    login_manager.login_message_category = "warning"

    @login_manager.user_loader
    def load_user(user_id):
        return UserModel.query.get(int(user_id))

    @jwt.token_in_blocklist_loader
    def token_in_blocklist_callback(jwt_header, jwt_data):
        jti = jwt_data["jti"]

        token = TokenBlockList.query.filter_by(jti=jti).scalar()

        return token is not None

    return app


def extended_ext(app):
    from app.extensions import db, jwt, migrate, login_manager

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    login_manager.init_app(app)

app = create_app()
