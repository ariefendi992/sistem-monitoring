from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_login import LoginManager


# db = SQLAlchemy(model_class=IdModel)
login_manager = LoginManager()
db = SQLAlchemy()
jwt = JWTManager()

migrate = Migrate()
