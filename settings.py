from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))


class Config(object):
    # APP CONFIG NEXT
    # USE_SESSION_FOR_NEXT = True
    SECRET_KEY = str(os.getenv("SECRET_KEY"))
    # PERMANENT_SESSION_LIFETIME = timedelta(minutes=10)
    # DATABASE ENGINE WITH SQLALCHEMY
    ENGINE = str(os.getenv("ENGINE"))
    USER = str(os.getenv("USER"))
    PASSWORD = str(os.getenv("PASSWORD"))
    HOST = str(os.getenv("HOST"))
    NAME = str(os.getenv("NAME"))
    SQLALCHEMY_DATABASE_URI = (
        ENGINE + "://" + USER + ":" + PASSWORD + "@" + HOST + "/" + NAME
    )
    # SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/db_monitoring'
    SQLALCHEMY_TRACK_MODIFICATIONS = str(os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS"))
    SQLALCHEMY_QUERIES_RECORD = str(os.getenv("SQLALCHEMY_QUERIES_RECORD"))
    # MODIFY DEFAULT CONFIG
    JSON_SORT_KEYS = False
    # JSON
    JWT_SECRET_KEY = str(os.getenv("JWT_SECRET_KEY"))
    ACCESS_EXPIRE = timedelta(hours=1)
    JWT_ACCESS_TOKEN_EXPIRES = ACCESS_EXPIRE
    ACCESS_REFRESH = timedelta(days=30)
    JWT_REFRESH_TOKEN_EXPIRES = ACCESS_REFRESH
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024
    # TEMPLATE
    # PREFERRED_URL_SCHEME = "https"
    TEMPLATES_AUTO_RELOAD = str(os.getenv("TEMPLATES_AUTO_RELOAD"))
    # EXPLAIN_TEMPLATE_LOADING = str(os.getenv("EXPLAIN_TEMPLATE_LOADING"))
