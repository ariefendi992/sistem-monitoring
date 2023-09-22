from datetime import timedelta
import os
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))


class Config(object):
    SECRET_KEY = str(os.getenv("SECRET_KEY"))
    root = str(os.getenv("ROOT"))
    passwd = str(os.getenv("PASSWD"))
    host = str(os.getenv("HOST"))
    db = str(os.getenv("DB"))
    #

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root@localhost/{db}"
    # SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{}@localhost/{db}"
    # SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:Ari19920905@localhost:3306/{db}"
    """
        Jika menggunakan `pymysql` variabel user harus disesuaikan dengan
        dengan nama user.
        Contoh:
            root = root
            user = user
            dst...
    """
    # SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{root}:{passwd}@{host}/{db}'
    SQLALCHEMY_TRACK_MODIFICATIONS = str(os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS"))
    SQLALCHEMY_QUERIES_RECORD = str(os.getenv("SQLALCHEMY_QUERIES_RECORD"))
    # JSON
    JWT_SECRET_KEY = str(os.getenv("JWT_SECRET_KEY"))
    ACCESS_EXPIRE = timedelta(minutes=60)
    JWT_ACCESS_TOKEN_EXPIRES = ACCESS_EXPIRE
    ACCESS_REFRESH = timedelta(minutes=7200)
    JWT_REFRESH_TOKEN_EXPIRES = ACCESS_REFRESH
    TEMPLATES_AUTO_RELOAD = str(os.getenv("TEMPLATES_AUTO_RELOAD"))

    duration = timedelta(seconds=3600)
    PERMANENT_SESSION_LIFETIME = duration
    REMEMBER_COOKIE_DURATION = duration
