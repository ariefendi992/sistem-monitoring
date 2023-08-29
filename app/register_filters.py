from app.lib.date_time import *
from app.lib.filters import from_db, hari_minggu, hari_sabtu, tgl_absen


def register_filters(app):
    app.jinja_env.filters["format_indo"] = format_indo
    app.jinja_env.filters["date_indo_non_weekday"] = format_indo_non_weekday
    app.jinja_env.filters["tgl"] = day_in_date
    app.jinja_env.filters["date_from_db"] = from_db
    app.jinja_env.filters["sabtu"] = hari_sabtu
    app.jinja_env.filters["minggu"] = hari_minggu
    app.jinja_env.filters["tglAbsen"] = tgl_absen
