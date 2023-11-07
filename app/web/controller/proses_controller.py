import os
import hashlib
import time
from h11 import Response
from werkzeug.utils import secure_filename
from flask import (
    Blueprint,
    flash,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)
from html2image import Html2Image
from selenium import webdriver
from flask_login import current_user, login_required
from app.lib.db_statement import DBStatement
from app.models.user_details_model import SiswaModel
from urllib.parse import urlparse
import requests
import urllib3
proses = Blueprint("proses", __name__, url_prefix="/data-proses/")

dir = os.getcwd() + "/app/api/static/img/siswa/id_card/"
hti = Html2Image()
dbs = DBStatement()


# os.environ["CURL_CA_BUNDLE"] = ''
# urllib3.disable_warnings()

def get_secure_filename(filename: str) -> str:
    return str(secure_filename(filename))


@proses.route("idcard", methods=["GET", "POST"])
def get_idcard():
    user_id = request.args.get("siswa", type=int)
    sql_siswa = dbs.get_one(SiswaModel, user_id=user_id)


    render = render_template(
        "admin/siswa/create_kartu_pelajar.html",
        data=sql_siswa,
        # "admin/siswa/create_id_card.html", data=sql_siswa, file=file
    )
    response = make_response(render)
    return response


    
@proses.route("generate-idcard", methods=["GET", "POST"])
# @login_required
def generate_idcard():

    user_id = request.args.get("siswa", type=int)
    sql_siswa = dbs.get_one(SiswaModel, user_id=user_id)

    enc = hashlib.md5(
        get_secure_filename(sql_siswa.first_name).encode("utf-8")
    ).hexdigest()
    f_name = f"{sql_siswa.kelas}_{sql_siswa.first_name.title() if len(sql_siswa.first_name)>= 3 else sql_siswa.last_name.split(" ",1)[0].replace(" ", "_").lower()}_{enc[1:5]}"

    url_ = requests.get(f'https://smpn2-mks.my.id/data-proses/idcard?siswa={user_id}', verify=False)
    urllib3.disable_warnings()
    
    dir = os.getcwd() + "/app/api/static/img/siswa/id_card/"
    hti.size = (295, 500)
    hti.output_path = dir
    hti.screenshot(
        url=url_.url,
        save_as=f"{f_name}.png",
    )
    
    time.sleep(1)

    list_dir = os.listdir(dir)
    if f"{f_name}.png" in list_dir:
        sql_siswa.id_card = f"{f_name}.png"
        dbs.commit_data()
        flash("ID Card telah berhasil dibuat.", "success")
        direct = redirect(url_for("admin2.id_card_siswa"))
        response = make_response(direct)
        return response
    else:
        flash("Generate ID CARD gagal.", "error")
        direct = redirect(url_for("admin2.getSiswa"))
        response = make_response(direct)
        return response


# else:
#     abort(401)
