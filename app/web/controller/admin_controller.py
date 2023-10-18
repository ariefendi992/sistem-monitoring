import json
import time
from typing import Any
from flask import (
    Blueprint,
    Response,
    abort,
    make_response,
    request,
    redirect,
    send_from_directory,
    session,
    url_for,
    render_template,
    flash,
)
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from calendar import monthrange
from app.lib.status_code import HTTP_413_REQUEST_ENTITY_TOO_LARGE
from app.models.user_model import *
from app.models.master_model import *
from app.models.user_details_model import *
from app.lib.base_model import BaseModel
from app.web.forms.form_absen import FormSelectAbsensi, FormSelectKehadiranSemester
from app.web.forms.form_auth import FormEditStatus
from app.web.forms.form_jadwal import FormJadwalMengajar
from app.web.forms.form_letter_report import FormSelectKelas
from app.web.forms.form_master import *
from app.web.forms.form_pengguna import (
    FormEditAdmin,
    FormTambahAdmin,
    FormUpdatePasswordAmdin,
)
from app.web.forms.form_siswa import FormAddSiswa, FormEditSiswa
from ..forms.form_auth import *
from ..forms.form_guru import *
from ..lib.base_url import base_url
from app.models.user_login_model import *
from app.models.data_model import *
from sqlalchemy import func
from app.lib.db_statement import DBStatement
import os
import requests as req
import io
import xlwt


admin2 = Blueprint(
    "admin2",
    __name__,
    template_folder="../templates/",
    url_prefix="/admin",
    static_folder="../static/",
)

file = os.getcwd() + "/data.json"


sql = lambda x: x

dbs = DBStatement()


@admin2.route("/")
@login_required
def index():
    if current_user.group == "admin":
        jml_siswa = sql(
            x=db.session.query(UserModel).filter(UserModel.group == "siswa").count()
        )

        jml_bk = db.session.query(UserModel).filter(UserModel.group == "bk").count()
        jml_guru = (
            sql(x=db.session.query(UserModel).filter(UserModel.group == "guru").count())
            + jml_bk
        )
        jml_admin = sql(
            x=db.session.query(UserModel).filter(UserModel.group == "admin").count()
        )

        jml_mapel = sql(x=db.session.query(MapelModel).count())

        jml_kelas = sql(x=db.session.query(KelasModel).count())

        user = dbs.get_one(AdminModel, user_id=current_user.id)
        session.update(
            first_name=user.first_name.title(), last_name=user.last_name.title()
        )

        return render_template(
            "admin/index_admin.html",
            jml_siswa=jml_siswa,
            jml_guru=jml_guru,
            jml_admin=jml_admin,
            jml_mapel=jml_mapel,
            jml_kelas=jml_kelas,
        )
    else:
        abort(401)


class PenggunaSiswa:
    @admin2.route("get-siswa")
    @login_required
    def getSiswa():
        if current_user.group == "admin":
            urlKelas = base_url + "api/v2/master/kelas/get-all"
            respKelas = req.get(urlKelas)
            jsonRespKelas = respKelas.json()

            urlSiswa = base_url + url_for("siswa.get")
            respSiswa = req.get(urlSiswa)
            jsonRespSiswa = respSiswa.json()

            user = dbs.get_one(AdminModel, user_id=current_user.id)
            session.update(
                first_name=user.first_name.title(), last_name=user.last_name.title()
            )

            return render_template(
                "admin/siswa/get_siswa.html",
                kelas=jsonRespKelas,
                siswa=jsonRespSiswa,
            )
        else:
            flash(
                f"Hak akses anda telah dicabut/berakhir. Silahkan login kembali",
                "error",
            )
            abort(401)

    @admin2.route("/generate-qc", methods=["GET", "PUT"])
    @login_required
    def generate_qc():
        if current_user.group == "admin":
            id = request.args.get("id")
            url = base_url + url_for("siswa.generate_qc", id=id)
            headers = {"Content-Type": "application/json"}
            r = req.put(url, headers=headers)
            if r.status_code == 200:
                flash(
                    message=f"Generate QR kode berhasil. Status : {r.status_code}",
                    category="success",
                )
                return redirect(url_for("admin2.getSiswa"))
            else:
                flash(
                    message=f"Maaf terjadi kesalahan dalam generate QR CODE. Status : {r.status_code}",
                    category="error",
                )
                return redirect(url_for("admin2.getSiswa"))
        else:
            flash(
                f"Hak akses anda telah dicabut/berakhir. Silahkan login kembali",
                "error",
            )
            abort(401)

    # NOTE:  UPLOAD FOTO
    @admin2.post("/upload-photo")
    @login_required
    def upload_foto():
        if current_user.group == "admin":
            id = request.args.get("id")
            url = base_url + url_for("siswa.upload_photo", id=id)
            file = request.files["file"]
            file_name = secure_filename(file.filename)
            upload_folder = os.getcwd() + "/temp/"
            path = upload_folder + file_name
            file.save(path)

            files = {"images": open(path, "rb")}
            response = req.post(url, files=files)

            if response.status_code == 200:
                files.get("images").close()
                temp_file = upload_folder + file_name
                os.remove(f"{temp_file}")
                flash(
                    f"File foto siswa telah berhasil di upload. Status : {response.status_code}",
                    "success",
                )
                return redirect(url_for("admin2.getSiswa"))
            else:
                return f"<p>error : {response.status_code}</p>"
        else:
            flash(
                f"Hak akses anda telah dicabut/berakhir. Silahkan login kembali",
                "error",
            )
            abort(401)

    """
    kode in dimatikan hanya untuk sementara waktu.

    @admin2.errorhandler(413)
    def request_entity_too_large(error):
         return "File Upload Maks 2MB", HTTP_413_REQUEST_ENTITY_TOO_LARGE

    """

    # NOTE:  TAMBAH DATA SISWA
    @admin2.route("/add-siswa", methods=["GET", "POST"])
    @login_required
    def add_siswa():
        # get kelas

        if current_user.group == "admin":
            url_kelas = base_url + f"/api/v2/master/kelas/get-all"
            get_kelas = req.get(url_kelas)
            data = get_kelas.json()
            kelas = [("", "..::Select::..")]
            for _ in data["data"]:
                kelas.append((_["id"], _["kelas"]))

            url = base_url + f"/api/v2/auth/create"
            form = FormAddSiswa(request.form)
            form.kelas.choices = kelas
            if request.method == "POST" and form.validate_on_submit():
                username = form.username.data
                password = form.password.data
                group = form.tipe.data if form.tipe.data else "siswa"
                fullname = form.fullname.data
                first_name = ""
                last_name = ""
                first_name, *last_name = fullname.split()
                if len(last_name) == 0:
                    last_name = first_name
                elif len(last_name) != 0:
                    last_name = " ".join(last_name)
                gender = form.jenisKelamin.data
                agama = form.agama.data
                kelas = form.kelas.data
                telp = request.form.get("telp")

                payload = json.dumps(
                    {
                        "username": username,
                        "password": password,
                        "group": group,
                        "first_name": first_name,
                        "last_name": last_name,
                        "gender": gender,
                        "agama": agama,
                        "kelas_id": kelas,
                        "telp": telp,
                    }
                )
                headers = {"Content-Type": "application/json"}
                response = req.post(url=url, headers=headers, data=payload)
                msg = response.json()
                if response.status_code == 201:
                    flash(
                        message=f"{msg['msg']}. Status : {response.status_code}",
                        category="success",
                    )
                    return redirect(url_for("admin2.getSiswa"))
                elif response.status_code == 409:
                    flash(
                        message="NISN sudah yang di input, telah terdaftar",
                        category="error",
                    )
                else:
                    return render_template("admin/siswa/tambah_siswa.html", form=form)

            user = dbs.get_one(AdminModel, user_id=current_user.id)
            session.update(
                first_name=user.first_name.title(), last_name=user.last_name.title()
            )
            return render_template("admin/siswa/tambah_siswa.html", form=form)
        else:
            flash(
                f"Hak akses anda telah dicabut/berakhir. Silahkan login kembali",
                "error",
            )
            abort(401)

    # NOTE:  UPDATE DATA SISWA
    @admin2.route("/update-siswa/<int:siswa>", methods=["GET", "POST", "PUT"])
    @login_required
    def get_object_siswa(siswa):
        if current_user.group == "admin":
            form = FormEditSiswa(request.form)

            sql_kelas = KelasModel.query.all()
            sql_siswa = db.session.query(SiswaModel).filter_by(user_id=siswa).first()
            for i in sql_kelas:
                form.kelas.choices.append((i.id, i.kelas))

            ### NOTE: Definisi form data
            form.nisn.data = sql_siswa.user.username
            form.fullname.data = (
                f"{sql_siswa.first_name.title()} {sql_siswa.last_name.title()}"
            )
            form.kelas.data = f"{sql_siswa.kelas_id}"
            form.jenisKelamin.data = sql_siswa.gender.lower()
            form.tempatLahir.data = (
                sql_siswa.tempat_lahir.title() if sql_siswa.tempat_lahir else "-"
            )
            form.tanggalLahir.data = sql_siswa.tgl_lahir
            form.tanggalLahir.render_kw = dict(required=False)
            form.agama.data = sql_siswa.agama.lower()
            form.alamat.data = sql_siswa.alamat.title() if sql_siswa.alamat else "-"
            form.namaOrtu.data = (
                sql_siswa.nama_ortu_or_wali.title()
                if sql_siswa.nama_ortu_or_wali
                else "-"
            )
            form.telp.data = sql_siswa.no_telp if sql_siswa.no_telp else "-"

            data = dict(user_id=siswa, kelasId=sql_siswa.kelas_id)

            user = dbs.get_one(AdminModel, user_id=current_user.id)
            session.update(
                first_name=user.first_name.title(), last_name=user.last_name.title()
            )

            render = render_template(
                "admin/siswa/edit_siswa.html", form=form, data=data
            )

            response = make_response(render)
            return response
        else:
            abort(401)

    @admin2.route("update-siswa/update", methods=["GET", "POST"])
    @login_required
    def updated_siswa():
        if current_user.group == "admin":
            form = FormEditSiswa(request.form)

            user_id = request.args.get("siswa", type=int)
            kelas_id_sebelum = request.args.get("kelas", type=int)
            sql_siswa = SiswaModel.query.filter_by(user_id=user_id).first()

            sql_count_siswa = SiswaModel.query

            if request.method == "POST":
                nisn = form.nisn.data
                fullname = form.fullname.data
                first_name = ""
                last_name = ""
                first_name, *last_name = fullname.split() if fullname else "None"
                if len(last_name) == 0:
                    last_name = first_name
                elif len(last_name) != 0:
                    last_name = " ".join(last_name)
                kelas = form.kelas.data
                gender = form.jenisKelamin.data
                tempat = form.tempatLahir.data
                tgl_lahir = form.tanggalLahir.data
                agama = form.agama.data
                alamat = form.alamat.data
                orang_tua = form.namaOrtu.data
                telp = form.telp.data

                sql_siswa.user.username = nisn
                sql_siswa.first_name = first_name.title()
                sql_siswa.last_name = last_name.title()
                sql_siswa.kelas_id = kelas
                sql_siswa.gender = gender
                sql_siswa.tempat_lahir = tempat
                sql_siswa.tgl_lahir = tgl_lahir
                sql_siswa.agama = agama
                sql_siswa.alamat = alamat
                sql_siswa.nama_ortu_or_wali = orang_tua
                sql_siswa.telp = telp

                sql_kelas = KelasModel.query
                kelas_baru = sql_kelas.filter_by(id=kelas).first()
                kelas_lama = sql_kelas.filter_by(id=kelas_id_sebelum).first()

                if kelas_baru.id != kelas_lama.id:
                    kelas_baru.jml_seluruh = sql_count_siswa.filter_by(
                        kelas_id=kelas
                    ).count()
                    kelas_baru.jml_perempuan = sql_count_siswa.filter_by(
                        gender="perempuan", kelas_id=kelas
                    ).count()
                    kelas_baru.jml_laki = sql_count_siswa.filter_by(
                        gender="laki-laki", kelas_id=kelas
                    ).count()

                    kelas_lama.jml_seluruh = sql_count_siswa.filter_by(
                        kelas_id=kelas_id_sebelum
                    ).count()
                    kelas_lama.jml_perempuan = sql_count_siswa.filter_by(
                        gender="perempuan", kelas_id=kelas_id_sebelum
                    ).count()
                    kelas_lama.jml_laki = sql_count_siswa.filter_by(
                        gender="laki-laki", kelas_id=kelas_id_sebelum
                    ).count()
                else:
                    kelas_lama.jml_seluruh = sql_count_siswa.filter_by(
                        kelas_id=kelas_id_sebelum
                    ).count()
                    kelas_lama.jml_perempuan = sql_count_siswa.filter_by(
                        gender="perempuan", kelas_id=kelas_id_sebelum
                    ).count()
                    kelas_lama.jml_laki = sql_count_siswa.filter_by(
                        gender="laki-laki", kelas_id=kelas_id_sebelum
                    ).count()

                db.session.commit()

                flash("Data profil sisa telah diperbaharui", "success")
                direct = redirect(url_for(".getSiswa"))
                response = make_response(direct)

                return response

            else:
                direct = redirect(url_for(".get_object_siswa", siswa=user_id))
                response = make_response(direct)
                flash("Data profil siswa gagal diperbaharui!", "error")
                return response
        else:
            abort(401)

    # NOTE:  DELETE DATA SISWA
    @admin2.route("/siswa/delete-siswa", methods=["GET", "POST", "DELETE"])
    @login_required
    def delete_siswa():
        if current_user.group == "admin":
            user_id = request.args.get("siswa", type=int)
            kelas_id = request.args.get("kelas", type=int)

            sql_user = UserModel.query.filter_by(id=user_id).first()
            sql_kelas = KelasModel.query.filter_by(id=kelas_id)
            get = sql_kelas.first()

            dir_foto = os.getcwd() + "/app/api/static/img/siswa/foto/"
            dir_qr = os.getcwd() + "/app/api/static/img/siswa/qr_code/"
            dir_idcard = os.getcwd() + "/app/api/static/img/siswa/id_card/"

            if sql_user:
                sql_siswa = SiswaModel.query.filter_by(user_id=sql_user.id).first()

                if sql_siswa.pic and sql_siswa.qr_code:
                    os.remove(os.path.join(dir_foto, f"{sql_siswa.pic}"))
                    os.remove(os.path.join(dir_qr, f"{sql_siswa.qr_code}"))
                    os.remove(os.path.join(dir_idcard, f"{sql_siswa.id_card}"))
                elif sql_siswa.pic:
                    os.remove(os.path.join(dir_foto, f"{sql_siswa.pic}"))
                elif sql_siswa.qr_code:
                    os.remove(os.path.join(dir_qr, f"{sql_siswa.qr_code}"))

                db.session.delete(sql_siswa)
                db.session.delete(sql_user)

                sql_count_siswa = SiswaModel.query.filter_by(kelas_id=kelas_id)
                get.jml_seluruh = sql_count_siswa.count()
                get.jml_laki = sql_count_siswa.filter_by(gender="laki-laki").count()
                get.jml_perempuan = sql_count_siswa.filter_by(
                    gender="perempuan"
                ).count()

                db.session.commit()

                flash("Data siswa telah dihapus.", "success")

                direct = redirect(url_for(".getSiswa"))
                response = make_response(direct)

                return response
            else:
                flash("Gagal hapus data siswa!", "error")
        else:
            abort(401)

    ### NOTE: DELETE FOTO SISWA & QR CODE
    @admin2.route("siswa/delete-foto", methods=["GET", "POST"])
    @login_required
    def delete_foto():
        if current_user.group == "admin":
            path_file = os.getcwd() + "/app/api/static/img/siswa/foto/"
            path_idcard = os.getcwd() + "/app/api/static/img/siswa/id_card/"
            list_dir_idcard = os.listdir(path_idcard)
            user_id = request.args.get("siswa", type=int)
            sql_siswa = dbs.get_one(entity=SiswaModel, user_id=user_id)

            if sql_siswa.id_card and sql_siswa.id_card in list_dir_idcard:
                os.remove(os.path.join(path_file, f"{sql_siswa.pic}"))
                os.remove(os.path.join(path_idcard, f"{sql_siswa.id_card}"))
            else:
                os.remove(os.path.join(path_file, f"{sql_siswa.pic}"))

            sql_siswa.pic = None
            sql_siswa.id_card = None
            dbs.commit_data()

            direct = redirect(url_for("admin2.getSiswa"))
            response = make_response(direct)
            flash("Foto siswa telah dihapus dari direktori file.", "info")
            return response
        else:
            dbs.dbs_abort(401)

    @admin2.route("siswa/delete-qrfile", methods=["GET", "POST"])
    @login_required
    def delete_qr():
        if current_user.group == "admin":
            path_file = os.getcwd() + "/app/api/static/img/siswa/qr_code/"
            path_idcard = os.getcwd() + "/app/api/static/img/siswa/id_card/"
            list_dir_idcard = os.listdir(path_idcard)
            user_id = request.args.get("siswa", type=int)
            sql_siswa = dbs.get_one(SiswaModel, user_id=user_id)

            if sql_siswa.id_card and sql_siswa.id_card in list_dir_idcard:
                os.remove(os.path.join(path_file, sql_siswa.qr_code))
                os.remove(os.path.join(path_idcard, sql_siswa.id_card))
            else:
                os.remove(os.path.join(path_file, sql_siswa.qr_code))
            sql_siswa.qr_code = None
            sql_siswa.id_card = None
            dbs.commit_data()

            direct = redirect(url_for("admin2.getSiswa"))
            response = make_response(direct)
            flash("File QR Code siswa telah dihapus dari direktori file.", "info")
            return response

        else:
            dbs.dbs_abort(401)

    @admin2.route("siswa/download-foto", methods=["GET", "POST"])
    @login_required
    def download_foto():
        if current_user.group == "admin":
            path_file = os.getcwd() + "/app/api/static/img/siswa/foto/"

            user_id = request.args.get("siswa", type=int)

            sql_siswa = dbs.get_one(SiswaModel, user_id=user_id)

            unduh = send_from_directory(path_file, sql_siswa.pic, as_attachment=True)
            response = make_response(unduh)
            return response
        else:
            abort(401)

    @admin2.route("siswa/download-qr", methods=["GET", "POST"])
    @login_required
    def download_qr():
        if current_user.group == "admin":
            dir_file = os.getcwd() + "/app/api/static/img/siswa/qr_code/"

            user_id = request.args.get("siswa", type=int)
            sql_siswa = dbs.get_one(SiswaModel, user_id=user_id)

            unduh = send_from_directory(dir_file, sql_siswa.qr_code, as_attachment=True)
            response = make_response(unduh)
            return response
        else:
            abort(401)

    @admin2.route("siswa/idcard")
    @login_required
    def id_card_siswa():
        if current_user.group == "admin":
            sql_siswa = (
                db.session.query(SiswaModel)
                .join(KelasModel)
                .order_by(KelasModel.kelas.asc())
                .order_by(SiswaModel.first_name.asc())
                .all()
            )
            path = os.getcwd() + "/app/api/static/img/siswa/id_card/"
            list_dir = os.listdir(path)

            for i in sql_siswa:
                if i.id_card and i.id_card not in list_dir:
                    sql_update = SiswaModel.get_filter_by(id=i.id)
                    sql_update.id_card = None
                    db.session.commit()

                # data.append(
                #     dict(
                #         id=i.id,
                #         user_id=i.user_id,
                #         first_name=i.first_name,
                #         last_name=i.last_name,
                #         id_card=i.id_card,
                #     )
                # )

            render = render_template("admin/siswa/id_card.html", data=sql_siswa)
            response = make_response(render)
            return response

        else:
            abort(401)

    @admin2.route("siswa/search/id-card")
    @login_required
    def search_idcard():
        if current_user.group == "admin":
            q = request.args.get("q")

            if q != "":
                results = (
                    SiswaModel.query.join(UserModel)
                    .filter(
                        SiswaModel.first_name.icontains(q)
                        | SiswaModel.last_name.icontains(q)
                        | UserModel.username.icontains(q)
                    )
                    .order_by(SiswaModel.first_name.asc())
                    .order_by(SiswaModel.last_name.asc())
                    .limit(100)
                )
            else:
                results = dbs.get_all(SiswaModel)

            render = render_template(
                "admin/siswa/htmx/search_idcard.html", results=results
            )
            response = make_response(render)
            return response
        else:
            abort(401)

    @admin2.route("siswa/id-card/unduh", methods=["GET", "POST"])
    @login_required
    def unduh_idcard():
        if current_user.group == "admin":
            dir = os.getcwd() + "/app/api/static/img/siswa/id_card/"
            siswa = request.args.get("siswa", int)

            sql_siswa = dbs.get_one(SiswaModel, user_id=siswa)

            unduh = send_from_directory(dir, sql_siswa.id_card, as_attachment=True)
            response = make_response(unduh)
            return response
        else:
            abort(401)

    @admin2.route("siswa/id-card/cetak", methods=["GET", "POST"])
    @login_required
    def cetak_idcard():
        if current_user.group == "admin":
            if request.method == "POST":
                list_cetak = request.form.getlist("idcardCheck")
                if len(list_cetak) == 0:
                    flash("Harap Pilih data yang ingin dicetak!", "error")

                else:
                    print(list_cetak)
                    data = []
                    for i in list_cetak:
                        user = dbs.get_one(SiswaModel, user_id=i)

                        data.append(
                            dict(
                                userid=i,
                                idcard=url_for(
                                    "siswa.static",
                                    filename=f"img/siswa/id_card/{user.id_card}",
                                ),
                            ),
                        )

                    render = render_template(
                        "admin/siswa/result_idcard.html", data=data
                    )
                    response = make_response(render)
                    return response

                direct = redirect(url_for("admin2.id_card_siswa"))
                return direct
        else:
            abort(401)

    # eksport data
    @admin2.route("/export-siswa")
    def export_siswa():
        url = request.url_root + url_for("siswa.get")
        req_url = req.get(url)
        data = req_url.json()
        # output in bytes
        output = io.BytesIO()
        # create workbook object
        workbook = xlwt.Workbook()
        # style header
        # style = xlwt.easyxf('font: name Times New Roman, color-index black, bold on; \
        #                     align: wrap on, vert center, horiz center;')
        style = xlwt.XFStyle()
        # background
        bg_color = xlwt.Pattern()
        bg_color.pattern = xlwt.Pattern.SOLID_PATTERN
        bg_color.pattern_fore_colour = xlwt.Style.colour_map["ocean_blue"]
        style.pattern = bg_color

        # border
        boder = xlwt.Borders()
        boder.bottom = xlwt.Borders.THIN
        style.borders = boder

        # font
        font = xlwt.Font()
        font.bold = True
        font.name = "Times New Roman"
        font.height = 220
        style.font = font

        # font aligment
        align = xlwt.Alignment()
        align.wrap = xlwt.Alignment.NOT_WRAP_AT_RIGHT
        align.horz = xlwt.Alignment.HORZ_CENTER
        align.vert = xlwt.Alignment.VERT_CENTER
        style.alignment = align

        # add a sheet
        sh = workbook.add_sheet("Data Siswa")
        # add headers
        sh.write(0, 0, "NO", style)
        sh.write(0, 1, "ID", style)
        sh.write(0, 2, "Nama", style)

        no = 0
        urut = 0

        for row in data["data"]:
            sh.write(no + 1, 0, urut + 1)
            sh.write(no + 1, 1, row["id"])
            no += 1
            urut += 1

        workbook.save(output)
        output.seek(0)

        return Response(
            output,
            mimetype="application/ms-excel",
            headers={"Content-Disposition": "attachment; filename=data_siswa.xls"},
        )


# """NOTE: DATA GURU"""
class PenggunaGuru:
    @admin2.route("data-guru")
    @login_required
    def get_guru():
        if current_user.group == "admin":
            url = base_url + "api/v2/guru/get-all"
            response = req.get(url)
            json_resp = response.json()

            user = dbs.get_one(AdminModel, user_id=current_user.id)
            session.update(
                first_name=user.first_name.title(), last_name=user.last_name.title()
            )
            return render_template("admin/guru/data_guru.html", model=json_resp)
        else:
            abort(401)

    @admin2.route("tambah-data", methods=["GET", "POST"])
    @login_required
    def add_guru():
        if current_user.group == "admin":
            form = FormAddGuru(request.form)
            base = request.root_url

            if request.method == "POST" and form.validate_on_submit():
                username = form.username.data
                password = form.password.data
                group = form.tipe.data if form.tipe.data else "guru"
                fullname = form.fullname.data
                first_name = ""
                last_name = ""
                first_name, *last_name = fullname.split() if fullname else "None"
                if len(last_name) == 0:
                    last_name = first_name
                elif len(last_name) != 0:
                    last_name = " ".join(last_name)
                gender = form.jenisKelamin.data
                agama = form.agama.data
                alamat = form.alamat.data
                telp = form.telp.data

                url_create = base + "api/v2/auth/create"
                payload = json.dumps(
                    {
                        "username": username,
                        "password": password,
                        "group": group,
                        "first_name": first_name,
                        "last_name": last_name,
                        "gender": gender,
                        "alamat": alamat,
                        "agama": agama,
                        "telp": telp,
                    }
                )
                headers = {"Content-Type": "application/json"}
                response = req.post(url=url_create, data=payload, headers=headers)
                msg = response.json().get("msg")

                if response.status_code == 201:
                    flash(f"{msg} Status : {response.status_code}", "success")
                    return redirect(url_for("admin2.get_guru"))
                else:
                    flash(f"{msg}. Status : {response.status_code}", "error")
                    # return redirect(url_for('admin2.get_guru'))
                    return render_template("admin/guru/tambah_guru.html", form=form)

            user = dbs.get_one(AdminModel, user_id=current_user.id)
            session.update(
                first_name=user.first_name.title(), last_name=user.last_name.title()
            )
            return render_template("admin/guru/tambah_guru.html", form=form)
        else:
            abort(401)

    @admin2.route("update-guru/<int:id>", methods=["POST", "GET"])
    @login_required
    def update_guru(id):
        if current_user.group == "admin":
            form = FormEditGuru(request.form)
            # NOTE: GET SINGLE OBJECT
            url_obj = base_url + f"api/v2/guru/single/{id}"
            resp_obj = req.get(url=url_obj)
            jsonObj = resp_obj.json()

            # FORM DEFAULT VALUE
            form.nip.default = jsonObj["nip"]
            form.fullname.default = jsonObj["first_name"] + " " + jsonObj["last_name"]
            form.jenisKelamin.default = jsonObj["gender"].lower()
            form.agama.default = jsonObj["agama"].lower()
            form.alamat.default = jsonObj["alamat"]
            form.telp.default = jsonObj["telp"]
            form.process()

            # NOTE: REQUEST FORM TO SAVE CHANGES
            if request.method == "POST":
                nip = request.form.get("nip")
                fullname = request.form.get("fullname")
                # NOTE : SPLIT FULLNAME TO FIRST_NAME and LAST_NAME
                first_name = ""
                last_name = ""
                first_name, *last_name = fullname.split() if fullname else "None"
                if len(last_name) == 0:
                    last_name = first_name
                elif len(last_name) != 0:
                    last_name = " ".join(last_name)
                # END
                gender = request.form.get("jenisKelamin")
                agama = request.form.get("agama")
                alamat = request.form.get("alamat")
                telp = request.form.get("telp")

                # HEADERS, DATA TO RESPONSE
                payload = json.dumps(
                    {
                        "nip": nip,
                        "first_name": first_name,
                        "last_name": last_name,
                        "gender": gender,
                        "agama": agama,
                        "alamat": alamat,
                        "telp": telp,
                    }
                )
                headers = {"Content-Type": "application/json"}

                resp_obj = req.put(url=url_obj, data=payload, headers=headers)
                msg = resp_obj.json()
                if resp_obj.status_code == 200:
                    flash(f"{msg['msg']} Status : {resp_obj.status_code}", "success")
                    return redirect(url_for("admin2.get_guru"))
                else:
                    flash(f"{msg['msg']}. Status : {resp_obj.status_code}", "error")
                return render_template("admin/guru/edit_guru.html", form=form)

            user = dbs.get_one(AdminModel, user_id=current_user.id)
            session.update(
                first_name=user.first_name.title(), last_name=user.last_name.title()
            )
            return render_template("admin/guru/edit_guru.html", form=form)
        else:
            abort(401)

    @admin2.route("delete-guru/<id>", methods=["GET", "DELETE", "POST"])
    @login_required
    def delete_guru(id):
        if current_user.group == "admin":
            url = base_url + f"api/v2/guru/single/{id}"
            response = req.delete(url=url)

            if response.status_code == 204:
                flash(
                    message=f"Data guru telah berhasil di hapus. Status : {response.status_code}",
                    category="info",
                )
                return redirect(url_for("admin2.get_guru"))
            else:
                flash(
                    message=f"Terjadi kesalahan dalama memuat data. Status : {response.status_code}",
                    category="info",
                )
                return redirect(url_for("admin2.get_guru"))
        else:
            abort(401)


class PenggunaUser:
    @admin2.route("/data-user")
    @login_required
    def get_user():
        if current_user.group == "admin":
            # url = base_url + f"api/v2/auth/get-all"
            # response = req.get(url)
            # json_resp = response.json()
            users = UserModel.query.all()
            form = FormEditStatus()
            formUpdatePassword = FormEditPassword()

            user = dbs.get_one(AdminModel, user_id=current_user.id)
            session.update(
                first_name=user.first_name.title(), last_name=user.last_name.title()
            )
            return render_template(
                "admin/pengguna/data_user.html",
                user=users,
                form=form,
                formPassword=formUpdatePassword,
            )
        else:
            abort(401)

    @admin2.route("/status-pengguna", methods=["GET", "POST"])
    @login_required
    def update_status():
        if current_user.group == "admin":
            user_id = request.args.get("pengguna", type=int)

            sql_user = dbs.get_one(UserModel, id=user_id)

            status = ""

            if sql_user.is_active == "1":
                status = 0
            elif sql_user.is_active == "0":
                status = 1

            sql_user.is_active = status
            sql_user.update_date = utc_makassar()

            dbs.commit_data()

            direct = redirect(url_for("admin2.get_user"))
            response = make_response(direct)

            return response

        else:
            abort(400)

    @admin2.route("/pengguna/tambah-admin", methods=["GET", "POST"])
    @login_required
    def tambah_admin():
        if current_user.group == "admin":
            form = FormTambahAdmin()

            if form.validate_on_submit():
                username = form.username.data
                password = form.password.data
                group = form.group.data
                fullname = form.fullname.data
                gender = form.gender.data
                alamat = form.alamat.data

                first_name = ""
                last_name = ""

                first_name, *last_name = fullname.split(" ") if fullname else ""

                if len(last_name) == 0:
                    last_name = first_name
                elif len(last_name) != 0:
                    last_name = " ".join(last_name)

                pswd = generate_password_hash(password)
                user = UserModel(username, pswd, group)

                dbs.add_data(user)
                detail: AdminModel = None
                if user:
                    detail = AdminModel(
                        first_name, last_name, gender, alamat, user=user
                    )

                    dbs.add_data(detail)

                    dbs.commit_data()

                    flash("Data user admin telah ditambahkan.", "success")
                    direct = redirect(url_for("admin2.get_user"))
                    response = make_response(direct)
                    return response
                else:
                    flash("Gagal menambahkan data user amdin", "error")

            user = dbs.get_one(AdminModel, user_id=current_user.id)
            session.update(
                first_name=user.first_name.title(), last_name=user.last_name.title()
            )
            render = render_template("admin/pengguna/tambah_admin.html", form=form)
            response = make_response(render)
            return response
        else:
            abort(401)

    @admin2.post("edit-pswd/<int:id>")
    @login_required
    def update_password(id):
        if current_user.group == "admin":
            url = base_url + f"api/v2/auth/edit-password?id={id}"
            if request.method == "POST":
                password = request.form.get("kataSandi")

                headers = {"Content-Type": "application/json"}
                payload = json.dumps({"password": password})

                response = req.put(url=url, data=payload, headers=headers)
                msg = response.json()
                if response.status_code == 200:
                    flash(
                        message=f'{msg["msg"]}, status : {response.status_code}',
                        category="success",
                    )
                    return redirect(url_for("admin2.get_user"))
                elif response.status_code == 400:
                    flash(
                        f'Error: {msg["msg"]}, status : {response.status_code}', "error"
                    )
                    return redirect(url_for("admin2.get_user"))
                else:
                    flash(
                        f"Error: Terjadi kesalahan dalam memuat data, status : {response.status_code}",
                        "error",
                    )
                    return redirect(url_for("admin2.get_user"))
        else:
            abort(401)

    @admin2.route("/admin/perbaharui-data", methods=["GET", "POST"])
    @login_required
    def update_profil():
        if current_user.group == "admin":
            form = FormEditAdmin()
            user_id = current_user.id
            user = dbs.get_one(UserModel, id=user_id)

            form.username.data = user.username
            for i in user.admins:
                form.fullname.data = f"{i.first_name.title()} {i.last_name.title() if i.first_name.lower() != i.last_name.lower() else ''}"
                form.gender.data = i.gender
                form.alamat.data = i.alamat.title() if i.alamat else ""
                form.telp.data = i.telp

            user = dbs.get_one(AdminModel, user_id=current_user.id)
            session.update(
                first_name=user.first_name.title(), last_name=user.last_name.title()
            )
            render = render_template("akun/profil_admin.html", form=form)
            response = make_response(render)
            return response

        else:
            abort(401)

    @admin2.route("/admin/perbaharui-data/updated", methods=["GET", "POST"])
    @login_required
    def updated_data_admin():
        if current_user.group == "admin":
            fullname = request.form.get("fullname")
            gender = request.form.get("gender")
            alamat = request.form.get("alamat")
            telp = request.form.get("telp")

            firstName: str | None
            lastName: str | None

            firstName, *lastName = fullname.split(" ") if fullname else ""
            if len(lastName) == 0:
                lastName = firstName
            elif len(lastName) != 0:
                lastName = " ".join(lastName)

            user = dbs.get_one(AdminModel, user_id=current_user.id)

            user.first_name = firstName
            user.last_name = lastName
            user.gender = gender
            user.alamat = alamat
            user.telp = telp

            dbs.commit_data()

            flash("Data profil admin telah diperbaharui", "success")
            direct = redirect(url_for("admin2.index"))
            response = make_response(direct)
            return response

        else:
            abort(401)

    @admin2.route("/admin/update-password", methods=["GET", "POST"])
    @login_required
    def update_password_admin():
        if current_user.group == "admin":
            form = FormUpdatePasswordAmdin()

            if form.validate_on_submit():
                password = form.password.data

                user = dbs.get_one(UserModel, id=current_user.id)
                pswd = generate_password_hash(password)
                user.password = pswd

                dbs.commit_data()

                flash("Password admin telah diperbaharui", "success")
                direct = redirect(url_for("admin2.index"))
                response = make_response(direct)
                return response

            render = render_template("akun/update_password.html", form=form)
            response = make_response(render)
            return response

        else:
            abort(401)


# NOTE: MASTER DATA
class MasterData:
    # NOTE: ================== MASTER DATA MAPEL =====================================
    @admin2.get("data-mapel")
    @login_required
    def get_mapel():
        if current_user.group == "admin":
            url = base_url + f"api/v2/master/mapel/get-all"
            response = req.get(url)
            jsonRespon = response.json()

            """
            NOTE : Form add data
            """

            form = FormMapel()
            return render_template(
                "admin/master/mapel/data_mapel.html",
                model=jsonRespon,
                form=form,
                r=request,
            )
        else:
            abort(401)

    @admin2.route("add-mapel", methods=["POST", "GET"])
    @login_required
    def add_mapel():
        if current_user.group == "admin":
            form = FormMapel(request.form)
            # URL = base_url + f"api/v2/master/mapel/create"
            # if request.method == "POST" and form.validate_on_submit():
            #     mapel = form.mapel.data
            #     payload = json.dumps({"mapel": mapel})
            #     headers = {"Content-Type": "application/json"}
            #     response = req.post(url=URL, data=payload, headers=headers)
            #     msg = response.json()
            #     if response.status_code == 201:
            #         flash(
            #             message=f"{msg['msg']}. Status : {response.status_code}",
            #             category="success",
            #         )
            #         return redirect(url_for("admin2.get_mapel"))
            #     else:
            #         flash(
            #             message=f"{msg['msg']}. Status : {response.status_code}",
            #             category="error",
            #         )
            #         direct = redirect(url_for("admin2.get_mapel"))
            #         response = make_response(direct)
            #         return response

            # direct = redirect(url_for("admin2.get_mapel"))
            # response = make_response(direct)
            # return response

            if form.validate_on_submit() and request.method == "POST":
                mapel = form.mapel.data
                data = MapelModel(mapel)
                data.save()

                flash("Data mapel\\n telah ditambahkan.", "success")

                return redirect(url_for("admin2.get_mapel"))

            user = dbs.get_one(AdminModel, user_id=current_user.id)
            session.update(
                first_name=user.first_name.title(), last_name=user.last_name.title()
            )
            model = MapelModel.get_all()

            return render_template(
                "admin/master/mapel/data_mapel.html",
                model=dict(data=model),
                form=form,
                r=request,
            )
        else:
            abort(401)

    @admin2.route("edit-mapel", methods=["GET", "POST"])
    @login_required
    def edit_mapel():
        if current_user.group == "admin":
            # URL = base_url + f"api/v2/master/mapel/get-one/{id}"

            # # NOTE: GET ONE DATA BY ID
            # responGetMapel = req.get(url=URL)
            # jsonResponse = responGetMapel.json()

            # form = FormMapel(request.form)
            # form.mapel.data = jsonResponse["mapel"]
            # if request.method == "POST" and form.validate_on_submit():
            #     mapel = request.form.get("mapel")
            #     payload = json.dumps({"mapel": mapel})
            #     headers = {"Content-Type": "application/json"}
            #     response = req.put(url=URL, data=payload, headers=headers)
            #     msg = response.json()
            #     if response.status_code == 200:
            #         flash(
            #             message=f'{msg["msg"]} Status : {response.status_code}',
            #             category="info",
            #         )
            #         return redirect(url_for("admin2.get_mapel"))
            #     else:
            #         flash(
            #             message=f'{msg["msg"]} Status : {response.status_code}',
            #             category="error",
            #         )
            #         return render_template(
            #             "admin/master/mapel/edit_mapel.html", form=form
            #         )

            form = FormEditMapel()
            id = request.args.get("id")
            mapels = MapelModel.get_all()
            get_mapel = MapelModel.get_filter_by(id=id)

            form.mapel.data = get_mapel.mapel

            if request.method == "POST":
                get_mapel.mapel = request.form.get("mapel")

                dbs.commit_data()

                flash("Data mapel\\ntelah diperbaharui.", "success")

                return redirect(url_for("admin2.get_mapel"))

            user = dbs.get_one(AdminModel, user_id=current_user.id)

            session.update(
                first_name=user.first_name.title(), last_name=user.last_name.title()
            )
            return render_template(
                "admin/master/mapel/data_mapel.html",
                model=dict(data=mapels),
                form=form,
                r=request,
                id=get_mapel.id,
            )
        else:
            abort(401)

    @admin2.route("delete-mapel/<int:id>", methods=["GET", "DELETE"])
    @login_required
    def delete_mapel(id):
        if current_user.group == "admin":
            URL = base_url + f"api/v2/master/mapel/get-one/{id}"
            response = req.delete(URL)
            if response.status_code == 204:
                flash(
                    message=f"Data mapel telah di hapus dari database. Status : {response.status_code}",
                    category="info",
                )
                return redirect(url_for("admin2.get_mapel"))
            elif response.status_code == 404:
                msg = response.json()
                flash(
                    message=f"{msg['msg']} : {response.status_code}",
                    category="info",
                )
                return redirect(url_for("admin2.get_mapel"))
        else:
            abort(401)

    # NOTE: ================== MASTER DATA SESMESTER =====================================
    @admin2.get("data-semester")
    @login_required
    def get_semester():
        if current_user.group == "admin":
            URL = base_url + f"api/v2/master/semester/get-all"
            response = req.get(URL)
            jsonResp = response.json()
            return render_template(
                "admin/master/semester/data_semester.html", model=jsonResp
            )
        else:
            abort(401)

    @admin2.route("add-semester", methods=["GET", "POST"])
    @login_required
    def add_semester():
        if current_user.group == "admin":
            form = FormSemester(request.form)
            URL = base_url + f"api/v2/master/semester/create"
            if request.method == "POST" and form.validate_on_submit():
                semester = form.semester.data
                status = form.status.data

                payload = json.dumps({"semester": semester, "status": status})
                headers = {"Content-Type": "application/json"}
                response = req.post(url=URL, data=payload, headers=headers)
                msg = response.json()

                if response.status_code == 201:
                    flash(
                        message=f'{msg["msg"]} Status: {response.status_code}',
                        category="success",
                    )
                    return redirect(url_for("admin2.get_semester"))
                else:
                    flash(
                        message=f'{msg["msg"]} Status: {response.status_code}',
                        category="error",
                    )
                    return render_template(
                        "admin/master/semester/tambah_semester.html", form=form
                    )
            user = dbs.get_one(AdminModel, user_id=current_user.id)
            session.update(
                first_name=user.first_name.title(), last_name=user.last_name.title()
            )
            return render_template(
                "admin/master/semester/tambah_semester.html", form=form
            )
        else:
            abort(401)

    @admin2.route("edit-semester/<int:id>", methods=["GET", "POST"])
    @login_required
    def edit_semester(id):
        if current_user.group == "admin":
            form = FormEditSemester(request.form)
            URL = base_url + f"api/v2/master/semester/get-one/{id}"
            responseGet = req.get(url=URL)
            jsonResp = responseGet.json()
            form.status.data = "1" if jsonResp["status"] == True else "0"

            if request.method == "POST" and form.validate_on_submit():
                status = request.form.get("status")
                payload = json.dumps({"status": status})
                headers = {"Content-Type": "application/json"}
                response = req.put(url=URL, data=payload, headers=headers)
                msg = response.json()

                if response.status_code == 200:
                    flash(
                        message=f'{msg["msg"]} Status : {response.status_code}',
                        category="info",
                    )
                    return redirect(url_for("admin2.get_semester"))
                else:
                    flash(
                        message=f'{msg["msg"]} Status : {response.status_code}',
                        category="error",
                    )
                    return render_template(
                        "admin/master/semester/edit_semester.html", form=form
                    )

            user = dbs.get_one(AdminModel, user_id=current_user.id)
            session.update(
                first_name=user.first_name.title(), last_name=user.last_name.title()
            )
            return render_template(
                "admin/master/semester/edit_semester.html", form=form
            )
        else:
            abort(401)

    @admin2.route("delete-semester/<int:id>", methods=["DELETE", "GET"])
    @login_required
    def delete_semester(id):
        if current_user.group == "admin":
            URL = base_url + f"api/v2/master/semester/get-one/{id}"
            response = req.delete(URL)
            if response.status_code == 204:
                flash(
                    message=f"Data semester telah di hapus dari database. Status : {response.status_code}",
                    category="info",
                )
                return redirect(url_for("admin2.get_semester"))
        else:
            abort(401)

    # NOTE: ================== MASTER DATA TAHUN AJARAN =====================================
    @admin2.route("data-tahun-ajaran")
    @login_required
    def get_ajaran():
        if current_user.group == "admin":
            URL = base_url + "api/v2/master/ajaran/get-all"
            response = req.get(URL)
            jsonResp = response.json()

            user = dbs.get_one(AdminModel, user_id=current_user.id)
            session.update(
                first_name=user.first_name.title(), last_name=user.last_name.title()
            )
            return render_template(
                "admin/master/tahun_ajaran/data_tahun_ajaran.html", model=jsonResp
            )
        else:
            abort(401)

    @admin2.route("add-tahun-ajaran", methods=["GET", "POST"])
    @login_required
    def add_ajaran():
        if current_user.group == "admin":
            form = FormTahunAJaran(request.form)
            URL = base_url + "api/v2/master/ajaran/create"

            if request.method == "POST" and form.validate_on_submit():
                ajaran = form.tahunAjaran.data
                status = form.status.data

                payload = json.dumps({"ajaran": ajaran, "status": status})
                headers = {"Content-Type": "application/json"}
                response = req.post(url=URL, data=payload, headers=headers)
                msg = response.json()

                if response.status_code == 201:
                    flash(
                        message=f'{msg["msg"]} Status : {response.status_code}',
                        category="success",
                    )
                    return redirect(url_for("admin2.get_ajaran"))
                else:
                    flash(
                        message=f'{msg["msg"]} Status : {response.status_code}',
                        category="error",
                    )
                    return render_template(
                        "admin/master/tahun_ajaran/tambah_tahun_ajaran.html", form=form
                    )

            user = dbs.get_one(AdminModel, user_id=current_user.id)
            session.update(
                first_name=user.first_name.title(), last_name=user.last_name.title()
            )
            return render_template(
                "admin/master/tahun_ajaran/tambah_tahun_ajaran.html", form=form
            )
        else:
            abort(401)

    @admin2.route("edit-tahun-ajaran/<int:id>", methods=["GET", "POST"])
    @login_required
    def edit_ajaran(id):
        if current_user.group == "admin":
            form = FormTahunAJaran(request.form)
            URL = base_url + f"api/v2/master/ajaran/get-one/{id}"
            response = req.get(URL)
            jsonResp = response.json()
            form.tahunAjaran.data = jsonResp["ajaran"]
            form.status.data = "1" if jsonResp["status"] == True else "0"

            if request.method == "POST" and form.validate_on_submit():
                ajaran = request.form.get("tahunAjaran")
                status = request.form.get("status")
                payload = json.dumps({"ajaran": ajaran, "status": status})
                headers = {"Content-Type": "application/json"}
                response = req.put(url=URL, data=payload, headers=headers)
                msg = response.json()
                if response.status_code == 200:
                    flash(
                        message=f'{msg["msg"]} Status : {response.status_code}',
                        category="info",
                    )
                    return redirect(url_for("admin2.get_ajaran"))
                else:
                    flash(
                        message=f'{msg["msg"]} Status : {response.status_code}',
                        category="error",
                    )
                    return render_template(
                        "admin/master/tahun_ajaran/edit_tahun_ajaran.html", form=form
                    )

            user = dbs.get_one(AdminModel, user_id=current_user.id)
            session.update(
                first_name=user.first_name.title(), last_name=user.last_name.title()
            )

            return render_template(
                "admin/master/tahun_ajaran/edit_tahun_ajaran.html", form=form
            )
        else:
            abort(401)

    @admin2.route("delete-tahun-ajaran/<int:id>", methods=["GET", "DELETE"])
    @login_required
    def delete_ajaran(id):
        if current_user.group == "admin":
            URL = base_url + f"api/v2/master/ajaran/get-one/{id}"
            response = req.delete(URL)
            if response.status_code == 204:
                flash(
                    message=f"Data Tahun Ajaran telah dihapus dari database. Status : {response.status_code}",
                    category="info",
                )
                return redirect(url_for("admin2.get_ajaran"))
        else:
            abort(401)

    # NOTE: ================== MASTER DATA KELAS =====================================
    @admin2.route("data-kelas")
    @login_required
    def get_kelas():
        if current_user.group == "admin":
            form = FormKelas()
            URL = base_url + "api/v2/master/kelas/get-all"
            response = req.get(URL)
            jsonResp = response.json()

            user = dbs.get_one(AdminModel, user_id=current_user.id)
            session.update(
                first_name=user.first_name.title(), last_name=user.last_name.title()
            )
            return render_template(
                "admin/master/kelas/data_kelas.html",
                model=jsonResp,
                form=form,
                r=request,
            )
        else:
            abort(401)

    @admin2.route("add-kelas", methods=["GET", "POST"])
    @login_required
    def add_kelas():
        if current_user.group == "admin":
            form = FormKelas(request.form)
            URL = base_url + "api/v2/master/kelas/create"

            if request.method == "POST" and form.validate_on_submit():
                kelas = form.kelas.data

                payload = json.dumps({"kelas": kelas})
                headers = {"Content-Type": "application/json"}
                response = req.post(url=URL, data=payload, headers=headers)
                msg = response.json()
                if response.status_code == 201:
                    flash(
                        message=f'{msg["msg"]} Status : {response.status_code}',
                        category="success",
                    )
                    return redirect(url_for("admin2.get_kelas"))
                else:
                    flash(
                        message=f'{msg["msg"]} Status : {response.status_code}',
                        category="error",
                    )
                    return render_template(
                        "admin/master/kelas/data_kelas.html", form=form
                    )

            user = dbs.get_one(AdminModel, user_id=current_user.id)
            session.update(
                first_name=user.first_name.title(), last_name=user.last_name.title()
            )

            return render_template("admin/master/kelas/data_kelas.html", form=form)
        else:
            abort(401)

    @admin2.route("edit-kelas", methods=["GET", "POST"])
    @login_required
    def edit_kelas():
        if current_user.group == "admin":
            form = FormEditKelas(request.form)
            id = request.args.get("id")
            URL = base_url + f"api/v2/master/kelas/get-one/{id}"

            response = req.get(URL)
            jsonResp = response.json()
            form.kelas.data = jsonResp["kelas"]
            form.jumlahLaki.data = jsonResp["laki"]
            form.jumlahPerempuan.data = jsonResp["perempuan"]
            form.jumlahSiswa.data = jsonResp["seluruh"]

            data_kelas = KelasModel.get_all()

            if request.method == "POST":
                kelas = request.form.get("kelas")
                laki = request.form.get("jumlahLaki")
                perempuan = request.form.get("jumlahPerempuan")
                # seluruh = request.form.get("jumlahSiswa")
                seluruh = int(laki) + int(perempuan)

                payload = json.dumps(
                    {
                        "kelas": kelas,
                        "laki": laki,
                        "perempuan": perempuan,
                        "seluruh": seluruh,
                    }
                )
                headers = {"Content-Type": "application/json"}

                response = req.put(url=URL, data=payload, headers=headers)
                msg = response.json()

                if response.status_code == 200:
                    flash(f'{msg["msg"]} Status : {response.status_code}', "info")
                    return redirect(url_for("admin2.get_kelas"))
                else:
                    flash(f'{msg["msg"]} Status : {response.status_code}', "error")
                    return render_template(
                        "admin/master/kelas/data_kelas.html",
                        form=form,
                        r=request,
                        model=dict(data=data_kelas),
                        id=id,
                    )

            user = dbs.get_one(AdminModel, user_id=current_user.id)
            session.update(
                first_name=user.first_name.title(), last_name=user.last_name.title()
            )

            return render_template(
                "admin/master/kelas/data_kelas.html",
                form=form,
                r=request,
                model=dict(data=data_kelas),
                id=id,
            )
        else:
            abort(401)

    @admin2.route("delete-kelas/<int:id>", methods=["GET", "DELETE"])
    @login_required
    def delete_kelas(id):
        if current_user.group == "admin":
            URL = base_url + f"api/v2/master/kelas/get-one/{id}"
            response = req.delete(URL)
            if response.status_code == 204:
                flash(
                    f"Data kelas telah dihpus dari database. Status : {response.status_code}",
                    "info",
                )
                return redirect(url_for("admin2.get_kelas"))
        else:
            abort(401)

    # NOTE: ================== MASTER DATA HARI =====================================
    @admin2.route("data-hari")
    @login_required
    def get_hari():
        if current_user.group == "admin":
            URL = base_url + "api/v2/master/hari/get-all"
            response = req.get(URL)
            jsonResp = response.json()

            user = dbs.get_one(AdminModel, user_id=current_user.id)
            session.update(
                first_name=user.first_name.title(), last_name=user.last_name.title()
            )
            return render_template("admin/master/hari/data_hari.html", model=jsonResp)
        else:
            abort(401)

    @admin2.route("add-hari", methods=["GET", "POST"])
    @login_required
    def add_hari():
        if current_user.group == "admin":
            URL = base_url + "api/v2/master/hari/create"
            form = FormHari(request.form)
            if request.method == "POST" and form.validate_on_submit():
                hari = form.hari.data

                payload = json.dumps({"hari": hari})
                headers = {"Content-Type": "application/json"}
                response = req.post(url=URL, data=payload, headers=headers)
                msg = response.json()
                if response.status_code == 201:
                    flash(
                        message=f'{msg["msg"]} Status : {response.status_code}',
                        category="success",
                    )
                    return redirect(url_for("admin2.get_hari"))
                else:
                    flash(
                        message=f'{msg["msg"]} Status : {response.status_code}',
                        category="error",
                    )
                    return render_template(
                        "admin/master/hari/tambah_hari.html", form=form
                    )

            user = dbs.get_one(AdminModel, user_id=current_user.id)
            session.update(
                first_name=user.first_name.title(), last_name=user.last_name.title()
            )
            return render_template("admin/master/hari/tambah_hari.html", form=form)
        else:
            abort(401)

    @admin2.route("edit-hari/<int:id>", methods=["GET", "POST"])
    def edit_hari(id):
        pass

    @admin2.route("delete-hari/<int:id>", methods=["GET", "DELETE"])
    @login_required
    def delete_hari(id):
        if current_user.group == "admin":
            URL = base_url + f"api/v2/master/hari/get-one/{id}"
            response = req.delete(URL)
            if response.status_code == 204:
                flash(
                    f"Data hari telah di hapus dari database. Status : {response.status_code}",
                    "info",
                )
                return redirect(url_for("admin2.get_hari"))
        else:
            abort(401)

    # NOTE: ================== MASTER DATA JAM =====================================
    @admin2.route("data-jam")
    @login_required
    def get_jam():
        if current_user.group == "admin":
            url = base_url + "api/v2/master/jam/get-all"
            resp = req.get(url)
            jsonResp = resp.json()
            form = FormJam(request.form)

            user = dbs.get_one(AdminModel, user_id=current_user.id)
            session.update(
                first_name=user.first_name.title(), last_name=user.last_name.title()
            )

            return render_template(
                "admin/master/jam/data_jam.html", model=jsonResp, form=form
            )
        else:
            abort(401)

    @admin2.route("tambah-jam", methods=["GET", "POST"])
    @login_required
    def add_jam():
        if current_user.group == "admin":
            form = FormJam(request.form)
            url = base_url + "api/v2/master/jam/create"
            if request.method == "POST":
                jam = form.jam.data
                payload = json.dumps({"jam": jam})
                headers = {"Content-Type": "application/json"}
                resp = req.post(url=url, data=payload, headers=headers)
                msg = resp.json()
                if resp.status_code == 201:
                    flash(
                        message=f'{msg["msg"]} Status : {resp.status_code}',
                        category="success",
                    )
                    return redirect(url_for("admin2.get_jam"))
                else:
                    flash(
                        message=f'{msg["msg"]} Status : {resp.status_code}',
                        category="error",
                    )
                    return redirect(url_for("admin2.get_jam"))
            else:
                flash(
                    f"Hak akses anda telah dicabut/berakhir. Silahkan login kembali",
                    "error",
                )
                abort(401)

    @admin2.route("edit-jam/<int:id>", methods=["GET", "POST"])
    @login_required
    def edit_jam(id):
        if current_user.group == "admin":
            url = base_url + f"api/v2/master/jam/get-one/{id}"
            if request.method == "POST":
                jam = request.form.get("jam")
                payload = json.dumps({"jam": jam})
                headers = {"Content-Type": "application/json"}
                resp = req.put(url=url, data=payload, headers=headers)
                msg = resp.json()
                if resp.status_code == 200:
                    flash(
                        message=f'{msg["msg"]} Status: {resp.status_code}',
                        category="info",
                    )
                    return redirect(url_for("admin2.get_jam"))
                else:
                    flash(
                        message=f'{msg["msg"]} Status: {resp.status_code}',
                        category="error",
                    )
                    return redirect(url_for("admin2.get_jam"))
            else:
                flash(
                    f"Hak akses anda telah dicabut/berakhir. Silahkan login kembali",
                    "error",
                )
                abort(401)

    @admin2.route("delete-jam/<int:id>", methods=["GET", "POST"])
    @login_required
    def delete_jam(id):
        if current_user.group == "admin":
            url = base_url + f"api/v2/master/jam/get-one/{id}"
            resp = req.delete(url=url)
            if resp.status_code == 204:
                flash(
                    message=f"Data Jam telah dihapus dari database Status: {resp.status_code}",
                    category="info",
                )
                return redirect(url_for("admin2.get_jam"))
            else:
                msg = resp.json()
                flash(
                    message=f'{msg["msg"]} Status: {resp.status_code}', category="error"
                )
                return redirect(url_for("admin2.get_jam"))
        else:
            abort(401)

    # NOTE: ================== MASTER DATA WALI KELAS =====================================
    @admin2.route("data-wali-kelas")
    @login_required
    def get_wali():
        if current_user.group == "admin":
            url = base_url + "api/v2/master/wali-kelas/get-all"
            resp = req.get(url)
            jsonResp = resp.json()

            form = FormWaliKelas(request.form)
            urlGuru = base_url + "api/v2/guru/get-all"
            respGuru = req.get(urlGuru)
            jsonRespGuru = respGuru.json()
            for i in jsonRespGuru:
                form.namaGuru.choices.append(
                    (i["id"], i["first_name"] + "" + i["last_name"])
                )

            urlKelas = base_url + "api/v2/master/kelas/get-all"
            respKelas = req.get(urlKelas)
            jsonRespKelas = respKelas.json()
            for i in jsonRespKelas["data"]:
                form.kelas.choices.append((i["id"], i["kelas"]))

            user = dbs.get_one(AdminModel, user_id=current_user.id)
            session.update(
                first_name=user.first_name.title(), last_name=user.last_name.title()
            )
            return render_template(
                "admin/master/wali_kelas/data_wali.html",
                model=jsonResp,
                form=form,
                jsonGuru=jsonRespGuru,
                jsonKelas=jsonRespKelas["data"],
                r=request,
            )
        else:
            abort(401)

    @admin2.route("tambah-wali", methods=["GET", "POST"])
    @login_required
    def add_wali():
        if current_user.group == "admin":
            form = FormWaliKelas(request.form)
            url = base_url + "api/v2/master/wali-kelas/create"
            data_wali = WaliKelasModel.get_all()
            data_guru = GuruModel.get_all()
            data_kelas = KelasModel.get_all()

            for g in data_guru:
                form.namaGuru.choices.append(
                    (g.id, f"{g.first_name.title()} {g.last_name.title()}")
                )

            for item in data_kelas:
                form.kelas.choices.append((item.id, item.kelas))

            data = []
            for i in data_wali:
                data.append(
                    dict(
                        id=i.id,
                        nip=i.guru.user.username,
                        first_name=i.guru.first_name.title(),
                        last_name=i.guru.last_name.title(),
                        kelas=i.kelas.kelas,
                    ),
                )

            if request.method == "POST" and form.validate_on_submit():
                guru = form.namaGuru.data
                kelas = form.kelas.data
                payload = json.dumps({"guru_id": guru, "kelas_id": kelas})
                headers = {"Content-Type": "application/json"}
                resp = req.post(url=url, data=payload, headers=headers)
                msg = resp.json()
                if resp.status_code == 201:
                    flash(
                        message=f'{msg["msg"]} Status : {resp.status_code}',
                        category="success",
                    )
                    return redirect(url_for("admin2.get_wali"))
                else:
                    flash(
                        message=f'{msg["msg"]} Status : {resp.status_code}',
                        category="error",
                    )
                    return render_template(
                        "admin/master/wali_kelas/data_wali.html",
                        form=form,
                        model=dict(data=data),
                        r=request,
                    )
            else:
                return render_template(
                    "admin/master/wali_kelas/data_wali.html",
                    form=form,
                    model=dict(data=data),
                    r=request,
                )

        # flash(
        #     f"Hak akses anda telah dicabut/berakhir. Silahkan login kembali",
        #     "error",
        # )
        abort(401)

    @admin2.route("update-wali", methods=["GET", "POST"])
    @login_required
    def edit_wali():
        if current_user.group == "admin":
            # url = base_url + f"api/v2/master/wali-kelas/get-one/{id}"
            # if request.method == "POST":
            #     guru_id = request.form.get("namaGuru")
            #     kelas_id = request.form.get("namaKelas")
            #     paylaod = json.dumps({"guru_id": guru_id, "kelas_id": kelas_id})
            #     headers = {"Content-Type": "application/json"}
            #     resp = req.put(url=url, data=paylaod, headers=headers)
            #     msg = resp.json()
            #     if resp.status_code == 200:
            #         flash(f'{msg["msg"]} Status : {resp.status_code}', "info")
            #         return redirect(url_for("admin2.get_wali"))
            #     else:
            #         flash(f'{msg["msg"]} Status : {resp.status_code}', "error")
            #         return redirect(url_for("admin2.get_wali"))

            form = FormEditWaliKelas()
            id = request.args.get("id")
            data_kelas = KelasModel.get_all()
            data_guru = GuruModel.get_all()
            data_wali = WaliKelasModel.get_all()

            for i in data_guru:
                form.namaGuru.choices.append(
                    (i.user_id, f"{i.first_name.title()} {i.last_name.title()}")
                )

            for i in data_kelas:
                form.kelas.choices.append((i.id, i.kelas))

            wali = WaliKelasModel.get_filter_by(id)

            form.namaGuru.default = wali.guru_id
            form.kelas.default = wali.kelas_id
            form.process()

            data = []
            for i in data_wali:
                data.append(
                    dict(
                        id=i.id,
                        nip=i.guru.user.username,
                        first_name=i.guru.first_name.title(),
                        last_name=i.guru.last_name.title(),
                        kelas=i.kelas.kelas,
                    ),
                )

            if request.method == "POST":
                guru_id = request.form.get("namaGuru")
                kelas_id = request.form.get("kelas")

                wali.guru_id = guru_id
                wali.kelas_id = kelas_id

                db.session.commit()

                flash("Data wali kelas\\ntelah diperbaharui.", "success")

                return redirect(url_for("admin2.get_wali"))

            return render_template(
                "admin/master/wali_kelas/data_wali.html",
                form=form,
                model=dict(data=data),
                r=request,
                id=id,
            )

        else:
            abort(401)

    @admin2.route("delete-wali/<int:id>", methods=["GET", "POST"])
    @login_required
    def delete_wali(id):
        if current_user.group == "admin":
            url = base_url + f"api/v2/master/wali-kelas/get-one/{id}"

            resp = req.delete(url=url)
            if resp.status_code == 204:
                flash(
                    f"Data wali kelas telah dihapus dari database. Status : {resp.status_code}",
                    "info",
                )
                return redirect(url_for("admin2.get_wali"))
            else:
                flash(
                    f"Terjadi kesalahan dalam memuat data. Status : {resp.status_code}",
                    "error",
                )
                return redirect(url_for("admin2.get_wali"))
        else:
            abort(401)

    # NOTE: ================== MASTER DATA GURU BK=====================================
    @admin2.route("data-guru-bk", methods=["GET"])
    @login_required
    def get_bk():
        if current_user.group == "admin":
            url = base_url + "api/v2/master/guru-bk/get-all"
            resp = req.get(url)
            jsonResp = resp.json()
            form = FormGuruBK(request.form)
            urlGuru = base_url + "api/v2/guru/get-all"
            respGuru = req.get(urlGuru)
            jsonRespGuru = respGuru.json()
            for i in jsonRespGuru:
                form.namaGuru.choices.append(
                    (i["id"], i["first_name"] + " " + i["last_name"])
                )

            user = dbs.get_one(AdminModel, user_id=current_user.id)
            session.update(
                first_name=user.first_name.title(), last_name=user.last_name.title()
            )
            return render_template(
                "admin/master/guru_bk/data_guru_bk.html",
                model=jsonResp,
                form=form,
                jsonGuru=jsonRespGuru,
                r=request,
            )
        else:
            abort(401)

    @admin2.route("add-guru-bk", methods=["GET", "POST"])
    @login_required
    def add_bk():
        if current_user.group == "admin":
            form = FormGuruBK()
            data_bk = GuruBKModel.get_all()
            data_guru = GuruModel.get_all()

            for i in data_guru:
                form.namaGuru.choices.append(
                    (
                        i.user_id,
                        f"{i.first_name.title()} {i.last_name.title()}",
                    ),
                )

            data = []
            for i in data_bk:
                data.append(
                    dict(
                        id=i.id,
                        nip=i.guru.user.username,
                        first_name=i.guru.first_name.title(),
                        last_name=i.guru.last_name.title(),
                        status=i.status,
                    ),
                )

            if form.validate_on_submit() and request.method == "POST":
                guru = form.namaGuru.data
                bk_data = GuruBKModel(guru)
                bk_data.save()

                flash("Data Guru BK\\ntelah ditambahkan.", "success")

                return redirect(url_for("admin2.get_bk"))

                # url = base_url + f"api/v2/master/guru-bk/create"
                # guru_id = request.form.get("namaGuru")
                # status = request.form.get("status")
                # payload = json.dumps({"guru_id": guru_id, "status": status})
                # headers = {"Content-Type": "application/json"}
                # resp = req.post(url=url, data=payload, headers=headers)
                # msg = resp.json()
                # if resp.status_code == 201:
                #     flash(f'{msg["msg"]} Status : {resp.status_code}', "success")
                #     return redirect(url_for("admin2.get_bk"))
                # else:
                #     flash(f'{msg["msg"]} Status : {resp.status_code}', "error")
                #     # return redirect(url_for("admin2.get_bk"))
                #     return render_template(
                #         "admin/master/guru_bk/data_guru_bk.html", form=form
                #     )
            return render_template(
                "admin/master/guru_bk/data_guru_bk.html",
                form=form,
                model=dict(data=data),
                r=request,
            )
        else:
            abort(401)

    @admin2.route("edit-guru-bk/<int:id>", methods=["GET", "POST"])
    @login_required
    def edit_bk(id):
        if current_user.group == "admin":
            form = FormEditGuruBK()

            data_guru = GuruModel.get_all()
            data_bk = GuruBKModel.get_all()
            get_bk = GuruBKModel.get_filter_by(id=id)

            form.namaGuru.default = get_bk.guru_id
            form.process()

            data = list()

            for i in data_bk:
                data.append(
                    dict(
                        id=i.id,
                        nip=i.guru.user.username,
                        first_name=i.guru.first_name.title(),
                        last_name=i.guru.last_name.title(),
                        status=i.status,
                    )
                )

            for i in data_guru:
                form.namaGuru.choices.append(
                    (
                        i.user_id,
                        f"{i.first_name.title()} {i.last_name.title()}",
                    ),
                )

            # url = base_url + f"api/v2/master/guru-bk/get-one/{id}"
            # status = request.form.get("status")
            # payload = json.dumps({"status": status})
            # headers = {"Content-Type": "application/json"}

            # resp = req.put(url=url, data=payload, headers=headers)
            # msg = resp.json()
            # if resp.status_code == 200:
            #     flash(f'{msg["msg"]} Status : {resp.status_code}', "info")
            #     return redirect(url_for("admin2.get_bk"))
            # else:
            #     flash(f'{msg["msg"]} Status : {resp.status_code}', "error")
            #     return redirect(url_for("admin2.get_bk"))

            if request.method == "POST" and request.method == "POST":
                guru_id = request.form.get("namaGuru")

                get_bk.guru_id = guru_id
                db.session.commit()

                flash("Data Guru BK\\ntelah diperbaharui.", "success")

                return redirect(url_for("admin2.get_bk"))

            return render_template(
                "admin/master/guru_bk/data_guru_bk.html",
                form=form,
                model=dict(data=data),
                r=request,
                id=id,
            )

        else:
            abort(401)

    @admin2.route("delete-guru-bk/<int:id>", methods=["GET", "DELETE"])
    @login_required
    def delete_bk(id):
        if current_user.group == "admin":
            url = base_url + f"api/v2/master/guru-bk/get-one/{id}"

            resp = req.delete(url=url)
            if resp.status_code == 204:
                flash(
                    f"Data Guru BK telah dihapus dari database. Status : {resp.status_code}",
                    "info",
                )
                return redirect(url_for("admin2.get_bk"))
            else:
                flash(f"Gagal memuat data. Status : {resp.status_code}", "error")
                return redirect(url_for("admin2.get_bk"))
        else:
            abort(401)

    # NOTE: ================== MASTER DATA KEPALA SEKOLAH =====================================
    @admin2.route("data-kepsek", methods=["GET"])
    @login_required
    def get_kepsek():
        if current_user.group == "admin":
            url = base_url + "api/v2/master/kepsek/get-all"
            resp = req.get(url)
            jsonResp = resp.json()
            form = FormKepsek(request.form)
            urlGuru = base_url + "api/v2/guru/get-all"
            respGuru = req.get(urlGuru)
            jsonRespGuru = respGuru.json()

            if not jsonResp["data"]:
                for i in jsonRespGuru:
                    form.namaGuru.choices.append(
                        (i["id"], i["first_name"] + "" + i["last_name"])
                    )

            status = [
                {"id": "0", "status": "tidak aktif"},
                {"id": "1", "status": "aktif"},
            ]

            user = dbs.get_one(AdminModel, user_id=current_user.id)
            session.update(
                first_name=user.first_name.title(), last_name=user.last_name.title()
            )

            return render_template(
                "admin/master/kepsek/data_kepsek.html",
                model=jsonResp,
                form=form,
                jsonGuru=jsonRespGuru,
                status=status,
            )
        else:
            abort(401)

    @admin2.route("add-kepsek", methods=["GET", "POST"])
    @login_required
    def add_kepsek():
        if current_user.group == "admin":
            # url = base_url + f"api/v2/master/kepsek/create"
            # guru_id = request.form.get("namaGuru")
            # payload = json.dumps({"guru_id": guru_id})
            # headers = {"Content-Type": "application/json"}
            # resp = req.post(url=url, data=payload, headers=headers)

            # if resp.status_code == 201:
            #     msg = resp.json()
            #     flash(f'{msg["msg"]} Status : {resp.status_code}', "success")
            #     return redirect(url_for("admin2.get_kepsek"))
            # else:
            #     flash(f"Ma'af! Terjadi kesalahan menginput data.", "error")
            #     return redirect(url_for("admin2.get_kepsek"))
            form = FormKepsek()
            data_guru = GuruModel.get_all()
            data_kepsek = KepsekModel.get_all()
            data = []

            for i in data_kepsek:
                data.append(
                    dict(
                        id=i.id,
                        nip=i.guru.user.username,
                        firs_name=i.guru.first_name.title(),
                        last_name=i.guru.last_name.title(),
                        status="Aktif" if i.status == "1" else "Tidak",
                    )
                )

            for i in data_guru:
                form.namaGuru.choices.append(
                    (i.user_id, f"{i.first_name.title()} {i.last_name.title()}")
                )

            if form.validate_on_submit() and request.method == "POST":
                guru_id = form.namaGuru.data

                data = KepsekModel(guru_id)
                data.save()

                flash("Data Kepala sekolah\\n telah ditambahkan.", "success")

                return redirect(url_for("admin2.get_kepsek"))

            return render_template(
                "admin/master/kepsek/data_kepsek.html",
                form=form,
                model=dict(data=data),
            )
        else:
            abort(401)

    @admin2.route("edit-kepsek/<int:id>", methods=["GET", "POST"])
    @login_required
    def edit_kepsek(id):
        if current_user.group == "admin":
            url = base_url + f"api/v2/master/kepsek/get-one/{id}"
            guru_id = request.form.get("namaGuru")
            status = request.form.get("status")

            payload = json.dumps({"guru_id": guru_id, "status": status})
            headers = {"Content-Type": "application/json"}

            resp = req.put(url=url, data=payload, headers=headers)
            msg = resp.json()
            if resp.status_code == 200:
                flash(f'{msg["msg"]} Status : {resp.status_code}', "info")
                return redirect(url_for("admin2.get_kepsek"))
            else:
                flash(f'{msg["msg"]} Status : {resp.status_code}', "error")
                return redirect(url_for("admin2.get_kepsek"))
        else:
            abort(401)

    @admin2.route("delete-kepsek/<int:id>", methods=["GET", "DELETE"])
    @login_required
    def delete_kepsek(id):
        if current_user.group == "admin":
            url = base_url + f"api/v2/master/kepsek/get-one/{id}"

            resp = req.delete(url=url)
            if resp.status_code == 204:
                flash(
                    f"Data Kepala Sekolah telah dihapus dari database. Status : {resp.status_code}",
                    "info",
                )
                return redirect(url_for("admin2.get_kepsek"))
            else:
                flash(f"Gagal memuat data. Status : {resp.status_code}", "error")
                return redirect(url_for("admin2.get_kepsek"))
        else:
            abort(401)


class JadwalMengajar:
    # NOTE: ================== DATA JADWAL MENGAAJAR =====================================
    @admin2.route("data-jawdwal-mengajar")
    @login_required
    def get_jadwal():
        if current_user.group == "admin":
            url = base_url + "api/v2/master/jadwal-mengajar/get-all"
            resp = req.get(url)
            jsonResp = resp.json()

            user = dbs.get_one(AdminModel, user_id=current_user.id)
            session.update(
                first_name=user.first_name.title(), last_name=user.last_name.title()
            )
            return render_template(
                "admin/jadwal_mengajar/data_jadwal.html", model=jsonResp
            )
        else:
            abort(401)

    @admin2.route("tambah-jadwal-mengajar", methods=["GET", "POST"])
    @login_required
    def add_jadwal():
        if current_user.group == "admin" and current_user.is_authenticated:
            form = FormJadwalMengajar(request.form)
            kodeMengajar = "MPL-" + str(time.time()).rsplit(".", 1)[1]
            urlSemester = base_url + "api/v2/master/semester/get-all"
            respSemester = req.get(urlSemester)
            ta = None
            sms = None
            ta_id = None
            sms_id = None
            for i in respSemester.json()["data"]:
                if i["status"] == True:
                    sms = i["semester"]
                    sms_id = i["id"]

            urlTahunAjaran = base_url + "api/v2/master/ajaran/get-all"
            respTahunAjaran = req.get(urlTahunAjaran)
            for i in respTahunAjaran.json()["data"]:
                if i["status"] == True:
                    ta = i["th_ajaran"]
                    ta_id = i["id"]

            urlGuru = base_url + "api/v2/guru/get-all"
            respGuru = req.get(urlGuru)
            jsonRespGuru = respGuru.json()
            for i in jsonRespGuru:
                form.namaGuru.choices.append(
                    (i["id"], i["first_name"] + " " + i["last_name"])
                )

            urlMapel = base_url + "api/v2/master/mapel/get-all"
            respMapel = req.get(urlMapel)
            for i in respMapel.json()["data"]:
                form.namaMapel.choices.append((i["id"], i["mapel"].title()))

            urlHari = base_url + "api/v2/master/hari/get-all"
            respHari = req.get(urlHari)
            for i in respHari.json()["data"]:
                form.hari.choices.append((i["id"], i["hari"].title()))

            urlKelas = base_url + "api/v2/master/kelas/get-all"
            respKelas = req.get(urlKelas)
            for i in respKelas.json()["data"]:
                form.kelas.choices.append((i["id"], i["kelas"]))

            form.kode.data = kodeMengajar
            form.semester.data = sms.title()
            form.ta.data = ta_id
            form.sms.data = sms_id
            form.tahunAjaran.data = ta

            if request.method == "POST" and form.validate_on_submit():
                kode_mengajar = request.form.get("kode")
                tahun_ajaran_id = request.form.get("ta")
                semeter_id = request.form.get("sms")
                guru_id = request.form.get("namaGuru")
                mapel_id = request.form.get("namaMapel")
                hari_id = request.form.get("hari")
                kelas_id = request.form.get("kelas")

                jam_mulai2 = request.form.get("waktuMulai2")
                jam_selesai2 = request.form.get("waktuSelesai2")
                jam_ke = request.form.get("jamKe")

                url = base_url + "api/v2/master/jadwal-mengajar/create"
                payload = json.dumps(
                    {
                        # "kode_mengajar": kode_mengajar,
                        "tahun_ajaran_id": tahun_ajaran_id,
                        "semeter_id": semeter_id,
                        "guru_id": guru_id,
                        "mapel_id": mapel_id,
                        "hari_id": hari_id,
                        "kelas_id": kelas_id,
                        "jam_mulai": jam_mulai2,
                        "jam_selesai": jam_selesai2,
                        "jam_ke": jam_ke,
                    }
                )
                headers = {"Content-Type": "application/json"}
                resp = req.post(url=url, data=payload, headers=headers)
                msg = resp.json()
                if resp.status_code == 201:
                    flash(f'{msg["msg"]} Status : {resp.status_code}', "success")
                    return redirect(url_for("admin2.get_jadwal"))
                else:
                    flash(f'{msg["msg"]} Status : {resp.status_code}', "error")
                    return redirect(url_for("admin2.get_jadwal"))

            user = dbs.get_one(AdminModel, user_id=current_user.id)
            session.update(
                first_name=user.first_name.title(), last_name=user.last_name.title()
            )
            return render_template(
                "admin/jadwal_mengajar/tambah_jadwal.html", form=form
            )
        else:
            abort(401)

    @admin2.route("edit-jadwal/<int:id>", methods=["GET", "POST"])
    def edit_jadwal(id):
        if current_user.group == "admin":
            form = FormJadwalMengajar(request.form)
            url = base_url + f"api/v2/master/jadwal-mengajar/get-one/{id}"
            respGet = req.get(url)
            jsonResp = respGet.json()

            urlGuru = base_url + "api/v2/guru/get-all"
            respGuru = req.get(urlGuru)
            jsonRespGuru = respGuru.json()
            for i in jsonRespGuru:
                form.namaGuru.choices.append(
                    (i["id"], i["first_name"] + " " + i["last_name"])
                )

            urlMapel = base_url + "api/v2/master/mapel/get-all"
            respMapel = req.get(urlMapel)
            for i in respMapel.json()["data"]:
                form.namaMapel.choices.append((i["id"], i["mapel"].title()))

            urlHari = base_url + "api/v2/master/hari/get-all"
            respHari = req.get(urlHari)
            for i in respHari.json()["data"]:
                form.hari.choices.append((i["id"], i["hari"].title()))

            urlKelas = base_url + "api/v2/master/kelas/get-all"
            respKelas = req.get(urlKelas)
            for i in respKelas.json()["data"]:
                form.kelas.choices.append((i["id"], i["kelas"]))

            form.kode.default = jsonResp["kode_mengajar"]
            form.tahunAjaran.default = jsonResp["tahun_ajaran"]
            form.namaGuru.default = jsonResp["guru_id"]
            form.semester.default = jsonResp["semester"].upper()
            form.namaMapel.default = jsonResp["mapel_id"]
            form.hari.default = jsonResp["hari_id"]
            form.kelas.default = jsonResp["kelas_id"]
            form.waktuMulai2.default = jsonResp["jam_mulai"]
            form.waktuSelesai2.default = jsonResp["jam_selesai"]
            form.jamKe.default = jsonResp["jam_ke"]
            form.process()

            if request.method == "POST":
                guru_id = request.form.get("namaGuru")
                mapel_id = request.form.get("namaMapel")
                hari_id = request.form.get("hari")
                jam_mulai = request.form.get("waktuMulai2")
                jam_selesai = request.form.get("waktuSelesai2")
                kelas_id = request.form.get("kelas")
                jam_ke = request.form.get("jamKe")

                payload = json.dumps(
                    {
                        "guru_id": guru_id,
                        "hari_id": hari_id,
                        "mapel_id": mapel_id,
                        "jam_mulai": jam_mulai,
                        "jam_selesai": jam_selesai,
                        "kelas_id": kelas_id,
                        "jam_ke": jam_ke,
                    }
                )

                headers = {"Content-Type": "application/json"}

                resp = req.put(url=url, data=payload, headers=headers)

                jsonRespPut = resp.json()

                if resp.status_code == 200:
                    flash(f'{jsonRespPut["msg"]} Status : {resp.status_code}', "info")
                    return redirect(url_for("admin2.get_jadwal"))
                else:
                    flash(
                        f"Terjadi kesalahan dalam perbaharui data. Status : {resp.status_code}"
                    )

            user = dbs.get_one(AdminModel, user_id=current_user.id)
            session.update(
                first_name=user.first_name.title(), last_name=user.last_name.title()
            )

            return render_template(
                "admin/jadwal_mengajar/edit_jadwal.html", model=jsonResp, form=form
            )

    @admin2.route("delete-jadwal/<int:id>", methods=["GET", "DELETE"])
    @login_required
    def delete_jadwal(id):
        if current_user.group == "admin":
            url = base_url + f"api/v2/master/jadwal-mengajar/get-one/{id}"
            resp = req.delete(url)

            if resp.status_code == 204:
                flash(
                    f"Data Jadwal Pelajaran telah dibatalkan. Status : {resp.status_code}",
                    "info",
                )
                return redirect(url_for("admin2.get_jadwal"))
            else:
                flash(
                    f"Gala memuat Data Jadwal Pelajaran. Status : {resp.status_code}",
                    "error",
                )
                return redirect(url_for("admin2.get_jadwal"))
        else:
            abort(401)


"""
NOTE : DATABASE DIRECT NO API
"""


@admin2.route("/data-kehadiran/bulan", methods=["GET", "POST"])
@login_required
def data_kehadiran_bulan():
    if current_user.group == "admin":
        base_kelas = BaseModel(KelasModel)
        kelas = base_kelas.get_all()
        base_bulan = BaseModel(NamaBulanModel)
        bulan = base_bulan.get_all()
        sql_absen = AbsensiModel.query.group_by(func.year(AbsensiModel.tgl_absen)).all()

        form = FormSelectAbsensi()
        # data kelas
        for i in kelas:
            form.kelas.choices.append((i.id, i.kelas))
        # data bulan
        for i in bulan:
            form.bulan.choices.append((i.id, i.nama_bulan.title()))

        for i in sql_absen:
            form.tahun.choices.append((i.tgl_absen.year, i.tgl_absen.year))

        if request.method == "POST" and form.validate_on_submit():
            kelas_id = request.form.get("kelas")
            bulan_id = request.form.get("bulan")
            tahun = request.form.get("tahun")

            sql_kehadiran = (
                db.session.query(AbsensiModel)
                .join(SiswaModel)
                .join(MengajarModel)
                .filter(AbsensiModel.siswa_id == SiswaModel.user_id)
                .filter(func.month(AbsensiModel.tgl_absen) == bulan_id)
                .filter(func.year(AbsensiModel.tgl_absen) == tahun)
                .filter(SiswaModel.kelas_id == kelas_id)
                .group_by(AbsensiModel.siswa_id)
                .order_by(AbsensiModel.siswa_id.asc())
                .all()
            )

            sql_keterangan = db.session.query(AbsensiModel)
            data = {}
            data["bulan"] = base_bulan.get_one(id=bulan_id).nama_bulan
            for i in sql_kehadiran:
                data["kelas"] = i.siswa.kelas.kelas
                data["tahun_ajaran"] = i.mengajar.tahun_ajaran.th_ajaran
                data["semester"] = i.mengajar.semester.semester

            this_year = datetime.date(datetime.today())
            data["tahun"] = this_year.year
            date_in_month = monthrange(
                int(
                    this_year.year,
                ),
                int(bulan_id),
            )
            data["month_range"] = date_in_month[1]

            response = make_response(
                render_template(
                    "admin/absensi/result_daftar_hadir.html",
                    sql_kehadiran=sql_kehadiran,
                    data=data,
                    sql_ket=sql_keterangan,
                    func=func,
                    AbsensiModel=AbsensiModel,
                )
            )
            return response

        user = dbs.get_one(AdminModel, user_id=current_user.id)
        session.update(
            first_name=user.first_name.title(), last_name=user.last_name.title()
        )
        return render_template(
            "admin/absensi/daftar_hadir_siswa.html",
            kelas=kelas,
            bulan=bulan,
            form=form,
        )
    else:
        return abort(401)


@admin2.route("data-kehadiran/semester", methods=["GET", "POST"])
@login_required
def data_kehadiran_semester():
    if current_user.group == "admin":
        form = FormSelectKehadiranSemester()
        sql_kelas = BaseModel(KelasModel).get_all()
        sql_semester = BaseModel(SemesterModel).get_all()

        for i in sql_kelas:
            form.kelas.choices.append((i.id, i.kelas))

        for i in sql_semester:
            form.semester.choices.append((i.id, i.semester.upper()))
        if form.validate_on_submit():
            kelas = request.form.get("kelas")
            semester = request.form.get("semester")

            sql_siswa = (
                db.session.query(AbsensiModel)
                .join(SiswaModel)
                .filter(AbsensiModel.siswa_id == SiswaModel.user_id)
                .filter(SiswaModel.kelas_id == kelas)
                .group_by(AbsensiModel.siswa_id)
            )

            sql_ket = (
                db.session.query(AbsensiModel)
                .join(MengajarModel)
                .filter(MengajarModel.semester_id == semester)
            )

            user = dbs.get_one(AdminModel, user_id=current_user.id)
            session.update(
                first_name=user.first_name.title(), last_name=user.last_name.title()
            )

            return render_template(
                "admin/absensi/result_daftar_hadir_sms.html",
                sql_siswa=sql_siswa,
                AbsensiModel=AbsensiModel,
                sql_ket=sql_ket,
            )
        return render_template("admin/absensi/daftar_hadir_semester.html", form=form)
    else:
        return abort(401)


@admin2.route("surat-pernyataan/pilih-kelas", methods=["GET", "POST"])
@login_required
def select_siswa():
    if current_user.group == "admin":
        base_kelas = BaseModel(KelasModel)
        sql_kelas = base_kelas.get_all()
        form = FormSelectKelas()
        for i in sql_kelas:
            form.kelas.choices.append((i.id, i.kelas))

        data = {}

        if form.validate_on_submit():
            kelas = request.form.get("kelas")
            base_siswa = BaseModel(SiswaModel)
            sql_siswa = base_siswa.get_all_filter_by(kelas_id=kelas)
            for i in sql_siswa:
                data["kelas"] = i.kelas.kelas

            return render_template(
                "admin/siswa/get_siswa_by_kelas.html", model=sql_siswa, data=data
            )

        user = dbs.get_one(AdminModel, user_id=current_user.id)
        session.update(
            first_name=user.first_name.title(), last_name=user.last_name.title()
        )

        return render_template("admin/letter_report/select_kelas.html", form=form)
    else:
        return abort(401)


@admin2.route("surat-pernyataan", methods=["GET", "POST"])
@login_required
def surat_pernyataan():
    try:
        if current_user.group == "admin":
            base_siswa = BaseModel(SiswaModel)
            id = request.args.get(key="siswa_id", type=int)
            sql_siswa = base_siswa.get_one(id=id)
            today = datetime.date(datetime.today())
            sql_wali = BaseModel(WaliKelasModel).get_one(kelas_id=sql_siswa.kelas_id)
            sql_bk = BaseModel(GuruBKModel).get_one_or_none(status="1")
            user = dbs.get_one(AdminModel, user_id=current_user.id)
            session.update(
                first_name=user.first_name.title(), last_name=user.last_name.title()
            )
            return render_template(
                "arsip/surat_pernyataan.html",
                sql_siswa=sql_siswa,
                today=today,
                sql_wali=sql_wali,
                sql_bk=sql_bk,
            )
        else:
            return abort(401)
    except Exception as e:
        return e


@admin2.route("rekap-absen", methods=["GET", "POST"])
@login_required
def rekap_bulan():
    # form = FormSelectAbsensi()
    base_kelas = BaseModel(KelasModel)
    sql_kelas = base_kelas.get_all()
    base_bulan = BaseModel(NamaBulanModel)
    sql_bulan = base_bulan.get_all()
    sql_year = AbsensiModel.query.group_by(func.year(AbsensiModel.tgl_absen)).all()

    form = FormSelectAbsensi()
    # data kelas
    for i in sql_kelas:
        form.kelas.choices.append((i.id, i.kelas))
    # data bulan
    for i in sql_bulan:
        form.bulan.choices.append((i.id, i.nama_bulan.title()))

    for i in sql_year:
        form.tahun.choices.append((i.tgl_absen.year, i.tgl_absen.year))
        # try:
        if form.validate_on_submit():
            kelas = request.form.get("kelas")
            bulan = request.form.get("bulan")
            tahun = request.form.get("tahun")

            sql_siswa = (
                db.session.query(AbsensiModel)
                .join(SiswaModel)
                .filter(AbsensiModel.siswa_id == SiswaModel.user_id)
                .filter(SiswaModel.kelas_id == kelas)
                .filter(func.month(AbsensiModel.tgl_absen) == bulan)
                .filter(func.year(AbsensiModel.tgl_absen) == tahun)
                .group_by(AbsensiModel.siswa_id)
                .order_by(SiswaModel.first_name.asc())
                .all()
            )

            if sql_siswa:
                sql_wali = (
                    db.session.query(WaliKelasModel).filter_by(kelas_id=kelas).scalar()
                )
                sql_kepsek = KepsekModel.query.filter_by(status=1).first()
                sql_ket = db.session.query(AbsensiModel)
                month_range = monthrange(int(tahun), int(bulan))
                data = {}
                data["bulan"] = base_bulan.get_one_or_none(id=bulan).nama_bulan
                data["kelas"] = base_kelas.get_one_or_none(id=kelas).kelas
                data[
                    "wali_kelas"
                ] = f"{sql_wali.guru.first_name} {sql_wali.guru.last_name}"
                data["nip_wali"] = sql_wali.guru.user.username
                data["semester"] = min(
                    [i.mengajar.semester.semester for i in sql_siswa]
                )
                data["ta"] = min([i.mengajar.tahun_ajaran.th_ajaran for i in sql_siswa])
                data["month_range"] = month_range[1]
                data["today"] = datetime.date(datetime.today())
                data[
                    "kepsek"
                ] = f"{sql_kepsek.guru.first_name} {sql_kepsek.guru.last_name}"

                data["nip_kepsek"] = sql_kepsek.guru.user.username
                response = make_response(
                    render_template(
                        "admin/letter_report/result_rekap_bulan.html",
                        AbsensiModel=AbsensiModel,
                        sql_siswa=sql_siswa,
                        data=data,
                        db=db,
                        func=func,
                        sql_ket=sql_ket,
                    )
                )
                return response
            else:
                flash("Data tidak ditemukan, harap periksa kembali!", "warning")
                response = make_response(
                    render_template("admin/letter_report/rekap_bulan.html", form=form)
                )
                return response

    else:
        user = dbs.get_one(AdminModel, user_id=current_user.id)
        session.update(
            first_name=user.first_name.title(), last_name=user.last_name.title()
        )
        response = make_response(
            render_template("admin/letter_report/rekap_bulan.html", form=form)
        )
        return response
