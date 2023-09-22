import os
from flask import Blueprint, send_from_directory, request

from app.lib.db_statement import DBStatement
from app.lib.status_code import HTTP_200_OK
from app.models.user_details_model import SiswaModel

dbs = DBStatement()

download = Blueprint("download", __name__, url_prefix="/api/v2/download")


# @download.route('/file/<name>')
# def download_file(name):
#     base_url = request.full_path
#     print(base_url)
#     folder_download = os.getcwd() +'/app/static/'
#     download = send_from_directory(folder_download +'doc/', path=name )
#     return download
@download.route("/file/<path:name>", methods=["GET", "POST"])
def image(name):
    # return f'foto: {name}'
    folder_path = os.getcwd() + "/app/api/static/img/"
    return send_from_directory(folder_path + "siswa/foto/", path=name)


@download.route("/idcard", methods=["GET", "POST"])
def idcard():
    user_id = request.args.get("siswa", type=int)
    user = dbs.get_one(SiswaModel, user_id=user_id)
    if not user:
        return "User tidak ada"
    path = os.getcwd() + f"/app/api/static/img/siswa/id_card/"

    unduh = send_from_directory(
        path,
        user.id_card,
    )
    return unduh, HTTP_200_OK
