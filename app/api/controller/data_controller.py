from flask import jsonify, request, Blueprint
from app.models.data_model import *

data = Blueprint("data", __name__, url_prefix="/api/v2/data")


class Absensi:
    def get_data():
        pass

    def get_one():
        pass

    def create_absen():
        pass

    def create_laporan():
        pass
