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
    # ENGINE = str(os.getenv("ENGINE"))
    root = str(os.getenv("ROOT"))
    passwd = str(os.getenv("PASSWD"))
    host = str(os.getenv("HOST"))
    db = str(os.getenv("DB"))
    # SQLALCHEMY_DATABASE_URI = (
    #     "mysql+pymysql://" + root + ":" + passwd + "@" + host + "/" + db
    # )
    # SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/db_monitoring'
    #

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root@localhost:3306/{db}"
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
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024
    # TEMPLATE
    # PREFERRED_URL_SCHEME = "https"
    TEMPLATES_AUTO_RELOAD = str(os.getenv("TEMPLATES_AUTO_RELOAD"))
    # EXPLAIN_TEMPLATE_LOADING = str(os.getenv("EXPLAIN_TEMPLATE_LOADING"))
