from flask import Blueprint
# import pandas as pd
import io

data_pre = Blueprint("data_pre", __name__, url_prefix="/data-prep/")


@data_pre.route("data-absensi")
def ex_abnsensi():
    pass
