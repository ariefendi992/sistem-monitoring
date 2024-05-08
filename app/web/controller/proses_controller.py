import os
import hashlib
import time
from turtle import position
from werkzeug.utils import secure_filename
from PIL import Image, ImageDraw, ImageFont
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
dir_foto_siswa = os.getcwd() + "/app/api/static/img/siswa/foto/"
dir_id_qr_siswa = os.getcwd() + "/app/api/static/img/siswa/qr_code/"
bg_id_card = os.getcwd() + "/app/static/images/bg_kartu_pelajar.png"

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

    # enc = hashlib.md5(
    #     get_secure_filename(sql_siswa.first_name).encode("utf-8")
    # ).hexdigest()
    # f_name = f"{sql_siswa.kelas}_{sql_siswa.first_name.title() if len(sql_siswa.first_name)>= 3 else sql_siswa.last_name.split(" ",1)[0].replace(" ", "_").lower()}_{enc[1:5]}"

    # url_ = requests.get(f'http://127.0.0.1:8000/data-proses/idcard?siswa={user_id}', verify=False)
    # urllib3.disable_warnings()

    dir = os.getcwd() + "/app/api/static/img/siswa/id_card/"
    # hti.size = (295, 500)
    # hti.output_path = dir
    # hti.screenshot(
    #     url=url_.url,
    #     save_as=f"{f_name}.png",
    # )

    # time.sleep(1)

    bg = Image.open(bg_id_card)

    foto_siswa = Image.open(f"{dir_foto_siswa}/{sql_siswa.pic}")
    qr_code = Image.open(f"{dir_id_qr_siswa}/{sql_siswa.qr_code}")
    new_qr = qr_code.resize((180, 180))

    fullname = f"{sql_siswa.first_name.title()} {sql_siswa.last_name.title()}"
    kelas = f"{sql_siswa.kelas.kelas}"
    # new_fullname = f"{fullname if len(fullname.split(' ')) < 3  else f'{ ' '.join(fullname.split(' ')[:2])}\n{' '.join(fullname.split(' ')[2:])}'}"

    if len(fullname.split(" ")) < 3:
        new_fullname == fullname + "\n" + kelas
    else:
        new_fullname = (
            " ".join(fullname.split(" ")[:2])
            + "\n"
            + " ".join(fullname.split(" ")[2:])
            + "\n"
            + kelas
        )

    teks = ImageDraw.Draw(bg)
    font = os.getcwd() + "/app/static/fonts/"
    font_image = ImageFont.truetype(font=f"{font}/OpenSans-Medium.ttf", size=32)

    # position_foto = (0,0)

    teks.text((68, 690), text=new_fullname, font=font_image, fill=(0, 0, 0))
    bg.paste(foto_siswa, (130, 220))
    bg.paste(new_qr, (390, 735))

    filename = f"{sql_siswa.kelas.kelas}_{'_'.join(sql_siswa.first_name.split(' '))}_{'_'.join(sql_siswa.last_name.split(' '))}"

    bg.save(f"{dir}/{filename}.png")

    list_dir = os.listdir(dir)
    if f"{filename}.png" in list_dir:
        sql_siswa.id_card = f"{filename}.png"
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

    # flash("ID Card telah berhasil dibuat.", "success")
    # direct = redirect(url_for("admin2.id_card_siswa"))
    # response = make_response(direct)
    # return response


# else:
#     abort(401)
