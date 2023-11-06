import io
import os
import hashlib
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
from flask_login import current_user, login_required
from app.lib.db_statement import DBStatement
from app.models.user_details_model import SiswaModel
from urllib.parse import urlparse

proses = Blueprint("proses", __name__, url_prefix="/data-proses/")

dir = os.getcwd() + "/app/api/static/img/siswa/id_card/"
hti = Html2Image()
dbs = DBStatement()


def get_secure_filename(filename: str) -> str:
    return str(secure_filename(filename))


@proses.route("idcard", methods=["GET", "POST"])
def get_idcard():
    user_id = request.args.get("siswa", type=int)
    sql_siswa = dbs.get_one(SiswaModel, user_id=user_id)

    foto = url_for("siswa.static", filename=f"img/siswa/foto/{sql_siswa.pic}")
    qr = url_for("siswa.static", filename=f"img/siswa/qr_code/{sql_siswa.qr_code}")

    file = dict(foto=foto, qr=qr)
    render = render_template(
        "admin/siswa/create_kartu_pelajar.html",
        data=sql_siswa,
        file=file
        # "admin/siswa/create_id_card.html", data=sql_siswa, file=file
    )
    response = make_response(render)
    return response


@proses.route("generate-idcard", methods=["GET", "POST"])
# @login_required
def generate_idcard():
    # if current_user.group == "admin":
    user_id = request.args.get("siswa", type=int)
    sql_siswa = dbs.get_one(SiswaModel, user_id=user_id)

    enc = hashlib.md5(
        get_secure_filename(sql_siswa.first_name).encode("utf-8")
    ).hexdigest()
    f_name = f"{sql_siswa.kelas}_{sql_siswa.first_name.title() if len(sql_siswa.first_name)>= 3 else sql_siswa.last_name.split(" ",1)[0].replace(" ", "_").lower()}_{enc[1:5]}"

    html = url_for("proses.get_idcard", siswa=sql_siswa.user_id)
    url = urlparse(request.base_url)
    url_link = f"{url.scheme}://{url.netloc}{html}"

    dir = os.getcwd() + "/app/api/static/img/siswa/id_card/"
    # hti.size = (204, 325)
    hti.size = (295, 500)
    hti.output_path = dir
    hti.screenshot(
        url=url_link,
        save_as=f"{f_name}.png",
    )

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
