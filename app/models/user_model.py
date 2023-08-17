from app.extensions import db
import sqlalchemy as sa
from app.lib.date_time import utc_makassar
from werkzeug.security import check_password_hash
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from uuid import uuid4


class UserModel(db.Model, UserMixin):
    __tablename__ = "auth_user"
    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String(128), nullable=False)
    password = sa.Column(sa.String(256), nullable=False)
    group = sa.Column(sa.String(128), nullable=False)
    join_date = sa.Column(sa.DateTime, default=utc_makassar())
    update_date = sa.Column(sa.DateTime, nullable=True)
    is_active = sa.Column(sa.String(2), nullable=False)
    user_last_login = sa.Column(sa.DateTime)
    user_logout = sa.Column(sa.DateTime)

    def __init__(self, username=None, password=None, group=None) -> None:
        super().__init__()
        self.username = username
        self.password = password
        self.group = group
        self.is_active = 1

    def __repr__(self) -> str:
        return self.username

    def check_pswd(*args, **kwargs):
        return check_password_hash(*args, **kwargs)


class TokenBlockList(db.Model):
    __tablename__ = "auth_token_block"
    id = sa.Column(sa.Integer, primary_key=True)
    jti = sa.Column(sa.String(36), nullable=False, index=True)
    created_at = sa.Column(sa.DateTime, nullable=False)
    user_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("auth_user.id", ondelete="CASCADE", onupdate="CASCADE"),
    )


class StatusUserLogin(db.Model):
    __tablename__ = "auth_status_user_login"
    # id = sa.Column(sa.Integer, primary_key=True)
    id = sa.Column(sa.String(36), primary_key=True, default=uuid4)

    user_login_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("auth_user.id", ondelete="CASCADE"),
    )
    user_login = relationship("UserModel", backref="UserLogin")
    status_login = sa.Column(sa.Boolean, default=False)

    def __init__(self, user_login_id: int, status_login: bool):
        self.user_login_id = user_login_id
        self.status_login = status_login
