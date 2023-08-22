from app.lib.date_time import *
from app.lib.filters import from_db


def register_filters(app):
    app.jinja_env.filters["format_indo"] = format_indo
    app.jinja_env.filters["date_indo_non_weekday"] = format_indo_non_weekday
    app.jinja_env.filters["tgl"] = day_in_date
    app.jinja_env.filters["date_from_db"] = from_db
