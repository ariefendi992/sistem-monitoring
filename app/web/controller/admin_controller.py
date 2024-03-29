import hashlib
import time
from flask import (
    Blueprint,
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
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import *
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from calendar import monthrange
from app.lib.date_time import format_datetime_id, format_indo
from app.lib.uploader import upload_resize_photo
from app.models.user_model import *
from app.models.master_model import *
from app.models.user_details_model import *
from app.lib.base_model import BaseModel
from app.web.forms.form_absen import FormSelectAbsensi, FormSelectKehadiranSemester
from app.web.forms.form_auth import FormEditStatus
from app.web.forms.form_jadwal import FormJadwalMengajar, FormUpdateJadwalMengajar
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

from app.models.user_login_model import *
from app.models.data_model import *
from sqlalchemy import and_, func
from app.lib.db_statement import DBStatement
import os
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
        jml_siswa = sql(x=db.session.query(SiswaModel).count())

        jml_bk = db.session.query(GuruBKModel).count()
        jml_guru = sql(x=db.session.query(GuruModel).count())
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
            kelas_model = KelasModel
            sql_kelas = kelas_model.get_all()

            siswa_model = SiswaModel
            sql_siswa = siswa_model.getAll()

            list_siswa = []
            list_nama_foto = []
            path_file = os.getcwd() + "/app/api/static/img/siswa/"
            list_file = os.listdir(path_file + "foto/")
            list_id_card = os.listdir(path_file + "id_card/")
            list_qr_file = os.listdir(path_file + "qr_code/")

            for i in sql_siswa:
                if i.pic is not None:
                    list_nama_foto.append(i.pic)
                if i.pic and i.pic not in list_file:
                    get_siswa = siswa_model.get_filter_by(id=i.id)
                    get_siswa.pic = None
                    siswa_model.commit()

                if i.id_card and i.id_card not in list_id_card:
                    get_siswa = siswa_model.get_filter_by(id=i.id)
                    get_siswa.id_card = None
                    siswa_model.commit()

                if i.qr_code and i.qr_code not in list_qr_file:
                    get_siswa = siswa_model.get_filter_by(id=i.id)
                    get_siswa.qr_code = None
                    siswa_model.commit()

                list_siswa.append(
                    dict(
                        id=i.user.id,
                        nisn=i.user.username,
                        first_name=i.first_name.title(),
                        last_name=i.last_name.title(),
                        gender=i.gender.title(),
                        kelas=i.kelas.kelas if i.kelas_id else "-",
                        kelas_id=i.kelas_id,
                        tempat_lahir=i.tempat_lahir if i.tempat_lahir else "-",
                        tgl_lahir=format_indo(i.tgl_lahir) if i.tgl_lahir else "-",
                        agama=i.agama if i.agama else "-",
                        alamat=i.alamat if i.alamat else "-",
                        nama_ortu=i.nama_ortu_or_wali if i.nama_ortu_or_wali else "-",
                        picture=i.pic,
                        telp=i.no_telp if i.no_telp else "-",
                        qr_code=i.qr_code,
                        active="Aktif" if i.user.is_active == "1" else "Non-Aktif",
                        join=format_datetime_id(i.user.join_date)
                        if i.user.join_date
                        else "-",
                        last_update=format_indo(i.user.update_date)
                        if i.user.update_date
                        else "-",
                        last_login=format_datetime_id(i.user.user_last_login)
                        if i.user.user_last_login
                        else "-",
                        logout=i.user.user_logout if i.user.user_logout else "-",
                        id_card=i.id_card,
                    ),
                )

            user = dbs.get_one(AdminModel, user_id=current_user.id)
            session.update(
                first_name=user.first_name.title(), last_name=user.last_name.title()
            )

            return render_template(
                "admin/siswa/get_siswa.html",
                kelas=sql_kelas,
                siswa=list_siswa,
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
            qc_folder = os.getcwd() + "/app/api/static/img/siswa/qr_code/"
            id = request.args.get("id")
            siswa_model = SiswaModel
            get_one = siswa_model.get_one(user_id=id)

            if not get_one:
                flash("Terjadi kesalahan!\\nPeriksa ID Siswa", "error")

            qc = qrcode.QRCode(
                error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=20, border=2
            )
            qc.add_data(get_one.user.username)
            qc_image = qc.make_image(
                image_factory=StyledPilImage,
                module_drawer=RoundedModuleDrawer(),
                fit=True,
            )
            enc_filename = hashlib.md5(
                secure_filename(get_one.user.username).encode("utf-8")
            ).hexdigest()

            first_name = (
                get_one.first_name
                if len(get_one.first_name) != 2
                else get_one.last_name.split(" ", 1)[0]
            )
            path_file = (
                qc_folder
                + get_one.kelas.kelas
                + "_"
                + first_name.lower()
                + "_"
                + enc_filename
                + ".png"
            )

            qc_image.save(path_file)

            get_one.qr_code = (
                get_one.kelas.kelas
                + "_"
                + first_name.lower()
                + "_"
                + enc_filename
                + ".png"
            )

            siswa_model.commit()

            flash(
                f"Kode QR {get_one.first_name} {get_one.last_name}\\ntelah dibuat.",
                "success",
            )
            return redirect(url_for("admin2.getSiswa"))
        else:
            flash(
                f"Hak akses anda telah dicabut/berakhir. Silahkan login kembali",
                "error",
            )
            abort(401)

    # NOTE:  UPLOAD FOTO
    @admin2.get("/upload-photo")
    @admin2.post("/upload-photo")
    @login_required
    def upload_foto():
        if current_user.group == "admin":
            id = request.args.get("id")
            siswa_model = SiswaModel
            get_one = siswa_model.get_one(user_id=id)

            if not get_one:
                flash("Terjadi kesalahan upload!\\nPeriksa User ID Siswa.", "error")

            file = request.files["file"]
            if file.filename == "":
                flash("Tidak ada foto terpilih!", "error")
                return redirect(request.url)
            first_name = (
                get_one.first_name
                if len(get_one.first_name) >= 3
                else get_one.last_name.split(" ", 1)[0]
            )
            user_first_name = first_name.replace(" ", "_").lower()
            up_resize = upload_resize_photo(file, user_first_name, get_one.kelas)

            if up_resize["status"] == "Ok":
                get_one.pic = up_resize["filename"]
                siswa_model.commit()
                flash(
                    f"Unggah Foto siswa {get_one.first_name.title() if len(get_one.first_name) >=3 else get_one.last_name.title()}\\nberhasil.",
                    "success",
                )
                return redirect(url_for("admin2.getSiswa"))
            else:
                flash(
                    f"Unggah Foto siswa {get_one.first_name.title() if len(get_one.first_name) >=3 else get_one.last_name.title()}\\ngagal.",
                    "error",
                )
                return redirect(url_for("admin2.getSiswa"))

            """
                Jika uploda menggunakan requests (API) maka bisa gunakan code dibawah ini
                dengan menambahkan foldet temp terlebih dahulu.

                # file_name = secure_filename(file.filename)
                # upload_folder = os.getcwd() + "/temp/"
                # path = upload_folder + file_name
                # file.save(path)

                # files = {"images": open(path, "rb")}
                # response = req.post(url, files=files)

                # if response.status_code == 200:
                #     files.get("images").close()
                #     temp_file = upload_folder + file_name
                #     os.remove(f"{temp_file}")
                #     flash(
                #         f"File foto siswa telah berhasil di upload. Status : {response.status_code}",
                #         "success",
                #     )
                #     return redirect(url_for("admin2.getSiswa"))
                # else:
                #     return f"<p>error : {response.status_code}</p>"
            """
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
            kelas_model = KelasModel
            get_kelas = kelas_model.get_all()
            kelas = [("", "..::Select::..")]
            for i in get_kelas:
                kelas.append((i.id, i.kelas))

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

                get_one = UserModel.get_filter_by(username=username)
                if get_one:
                    flash(
                        f"Username sudah terdaftar.\\nSilahkan masukkan username lain.",
                        "error",
                    )

                hash_pswd = generate_password_hash(password=password)
                user_model = UserModel(
                    username=username, password=hash_pswd, group=group
                )
                user_model.save()

                siswa_model = SiswaModel(
                    first_name=first_name,
                    last_name=last_name,
                    gender=gender,
                    agama=agama,
                    kelas_id=kelas,
                    telp=telp,
                    user_id=user_model.id,
                )
                kelas_model = KelasModel
                get_kelas = kelas_model.get_filter_by(id=kelas)
                siswa_model.save()

                countSiswaGender = (
                    db.session.query(func.count(SiswaModel.kelas_id))
                    .filter(SiswaModel.kelas_id == kelas)
                    .filter(SiswaModel.gender == gender)
                    .scalar()
                )
                countSiswaLaki = (
                    db.session.query(func.count(SiswaModel.kelas_id))
                    .filter(SiswaModel.kelas_id == kelas)
                    .filter(SiswaModel.gender == "laki-laki")
                    .scalar()
                )
                countSiswaPerempuan = (
                    db.session.query(func.count(SiswaModel.kelas_id))
                    .filter(SiswaModel.kelas_id == kelas)
                    .filter(SiswaModel.gender == "perempuan")
                    .scalar()
                )
                countSiswaAll = (
                    db.session.query(func.count(SiswaModel.kelas_id))
                    .filter(SiswaModel.kelas_id == kelas)
                    .scalar()
                )

                if siswa_model.gender == "laki-laki":
                    get_kelas.jml_laki = countSiswaGender
                    get_kelas.jml_perempuan = countSiswaPerempuan

                elif siswa_model.gender == "perempuan":
                    get_kelas.jml_laki = countSiswaLaki
                    get_kelas.jml_perempuan = countSiswaPerempuan

                get_kelas.jml_seluruh = countSiswaAll
                db.session.commit()

                return redirect(url_for("admin2.getSiswa"))

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
            sql_siswa = SiswaModel.query.filter_by(user_id=user_id).first()
            # kelas_id_sebelum = request.args.get("kelas", type=int)
            # kelas_id_sebelum = request.args.get("kelas", type=int)
            kelas_id_sebelum = sql_siswa.kelas_id

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
                
                if (nisn == '' or nisn is None) or (fullname == '' or fullname is None) or (kelas == '' or kelas is None):
                    flash(f"Gagal!\\nForm Kelas atau Nama atau NISN tidak boleh kosong.","error")
                    # flash(f"Gagal!\\nForm {'Kelas' if (kelas == "" or kelas == None) else 'NISN' if (nisn=='' or nisn is None) else 'Nama Lengkap' } tidak boleh kosong.","error")
                    
                    return redirect(url_for('.get_object_siswa', siswa=user_id))
                else:
                    
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

                    if kelas_id_sebelum is not None:
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
    # @admin2.route("/export-siswa")
    # def export_siswa():
    #     url = request.url_root + url_for("siswa.get")
    #     req_url = requests.get(url)
    #     data = req_url.json()
    #     # output in bytes
    #     output = io.BytesIO()
    #     # create workbook object
    #     workbook = xlwt.Workbook()
    #     # style header
    #     # style = xlwt.easyxf('font: name Times New Roman, color-index black, bold on; \
    #     #                     align: wrap on, vert center, horiz center;')
    #     style = xlwt.XFStyle()
    #     # background
    #     bg_color = xlwt.Pattern()
    #     bg_color.pattern = xlwt.Pattern.SOLID_PATTERN
    #     bg_color.pattern_fore_colour = xlwt.Style.colour_map["ocean_blue"]
    #     style.pattern = bg_color

    #     # border
    #     boder = xlwt.Borders()
    #     boder.bottom = xlwt.Borders.THIN
    #     style.borders = boder

    #     # font
    #     font = xlwt.Font()
    #     font.bold = True
    #     font.name = "Times New Roman"
    #     font.height = 220
    #     style.font = font

    #     # font aligment
    #     align = xlwt.Alignment()
    #     align.wrap = xlwt.Alignment.NOT_WRAP_AT_RIGHT
    #     align.horz = xlwt.Alignment.HORZ_CENTER
    #     align.vert = xlwt.Alignment.VERT_CENTER
    #     style.alignment = align

    #     # add a sheet
    #     sh = workbook.add_sheet("Data Siswa")
    #     # add headers
    #     sh.write(0, 0, "NO", style)
    #     sh.write(0, 1, "ID", style)
    #     sh.write(0, 2, "Nama", style)

    #     no = 0
    #     urut = 0

    #     for row in data["data"]:
    #         sh.write(no + 1, 0, urut + 1)
    #         sh.write(no + 1, 1, row["id"])
    #         no += 1
    #         urut += 1

    #     workbook.save(output)
    #     output.seek(0)

    #     return Response(
    #         output,
    #         mimetype="application/ms-excel",
    #         headers={"Content-Disposition": "attachment; filename=data_siswa.xls"},
    #     )


# """NOTE: DATA GURU"""
class PenggunaGuru:
    @admin2.route("data-guru")
    @login_required
    def get_guru():
        if current_user.group == "admin":
            get_guru = GuruModel.get_all()

            user = dbs.get_one(AdminModel, user_id=current_user.id)
            session.update(
                first_name=user.first_name.title(), last_name=user.last_name.title()
            )
            return render_template("admin/guru/data_guru.html", model=get_guru)
        else:
            abort(401)

    @admin2.route("tambah-data", methods=["GET", "POST"])
    @login_required
    def add_guru():
        if current_user.group == "admin":
            form = FormAddGuru(request.form)

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

                hash_pswd = UserModel.generate_pswd(password)

                get_one_user = UserModel.get_filter_by(username=username)
                if get_one_user:
                    flash("Username yang di input sudah ada.", "error")

                user_model = UserModel(username, hash_pswd, group)
                user_model.save()

                guru_model = GuruModel(
                    first_name.title(),
                    last_name.title(),
                    gender,
                    alamat,
                    agama,
                    telp,
                    user_model.id,
                )
                guru_model.save()

                flash("Data guru telah di tambahkan.", "success")
                return redirect(url_for("admin2.get_guru"))

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
            guru_model = GuruModel
            get_one = guru_model.get_one(user_id=id)

            # FORM DEFAULT VALUE
            form.nip.default = get_one.user.username
            form.fullname.default = (
                get_one.first_name.title() + " " + get_one.last_name.title()
            )
            form.jenisKelamin.default = get_one.gender.lower()
            form.agama.default = get_one.agama.lower()
            form.alamat.default = get_one.alamat
            form.telp.default = get_one.telp
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

                get_one.user.username = nip
                get_one.first_name = first_name.title()
                get_one.last_name = last_name.title()
                get_one.gender = gender
                get_one.agama = agama
                get_one.alamat = alamat
                get_one.telp = telp

                guru_model.update()

                flash("Data Guru telah diperbaharui.", "success")
                return redirect(url_for("admin2.get_guru"))

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
            guru_model = GuruModel
            get_one = guru_model.get_one(user_id=id)

            if not get_one:
                flash("Terjadi kesalah!\\nPeriksa User ID atau ID", "error")

            guru_model.delete(get_one)
            flash("Data Guru telah dihapus", "success")
            return redirect(url_for("admin2.get_guru"))
        else:
            abort(401)


class PenggunaUser:
    @admin2.route("/data-user")
    @login_required
    def get_user():
        if current_user.group == "admin":
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
            user_model = UserModel
            get_one = user_model.get_one(id=id)

            if request.method == "POST":
                password = request.form.get("kataSandi")

                hash_pass = UserModel.generate_pswd(password)

                get_one.password = hash_pass
                user_model.update()

                flash(
                    f"Kata Sandi dengan username {get_one.username}\\ntelah diperbaharui.",
                    "success",
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
            mapel_model = MapelModel
            get_mapels = mapel_model.get_all()
            """
            NOTE : Form add data
            """

            form = FormMapel()
            return render_template(
                "admin/master/mapel/data_mapel.html",
                model=get_mapels,
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
            form = FormEditMapel()
            id = request.args.get("id", type=int)
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
                model=mapels,
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
            mapel_model = MapelModel
            get_mapel = mapel_model.get_filter_by(id=id)

            if not get_mapel:
                flash("Data tidak ditemukan.\\nSilahkan periksa kembali.", "error")
                return redirect(url_for("admin2.get_mapel"))

            mapel_model.delete(get_mapel)

            flash("\\nData mapel telah dihapus", "success")
            return redirect(url_for("admin2.get_mapel"))

        else:
            abort(401)

    # NOTE: ================== MASTER DATA SESMESTER =====================================
    @admin2.get("data-semester")
    @login_required
    def get_semester():
        if current_user.group == "admin":
            get_semester = SemesterModel.query.all()
            return render_template(
                "admin/master/semester/data_semester.html", model=get_semester
            )
        else:
            abort(401)

    @admin2.route("add-semester", methods=["GET", "POST"])
    @login_required
    def add_semester():
        if current_user.group == "admin":
            form = FormSemester(request.form)
            semester_model = SemesterModel

            if request.method == "POST" and form.validate_on_submit():
                semester = form.semester.data
                status = form.status.data

                semester_model.semester = semester
                semester_model.is_active = status

                semester_model.save(semester_model)

                flash("Data semester telah ditambahkan", "success")
                return redirect(url_for("admin2.get_semester"))

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
            model = SemesterModel
            get_one = model.get_one(id=id)
            form.status.data = get_one.is_active

            if request.method == "POST" and form.validate_on_submit():
                status = request.form.get("status")

                get_one.is_active = status

                model.update()

                flash("Data semester telah diperbaharui", "success")

                return redirect(url_for("admin2.get_semester"))

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
            model = SemesterModel
            get_one = model.get_one(id=id)

            model.delete(get_one)

            flash("Data semester telah dihapus!", "success")

            return redirect(url_for("admin2.get_semester"))
        else:
            abort(401)

    # NOTE: ================== MASTER DATA TAHUN AJARAN =====================================
    @admin2.route("data-tahun-ajaran")
    @login_required
    def get_ajaran():
        if current_user.group == "admin":
            user = dbs.get_one(AdminModel, user_id=current_user.id)
            session.update(
                first_name=user.first_name.title(), last_name=user.last_name.title()
            )

            model = TahunAjaranModel.get_all()

            return render_template(
                "admin/master/tahun_ajaran/data_tahun_ajaran.html", model=model
            )
        else:
            abort(401)

    @admin2.route("add-tahun-ajaran", methods=["GET", "POST"])
    @login_required
    def add_ajaran():
        if current_user.group == "admin":
            form = FormTahunAJaran(request.form)
            model = TahunAjaranModel

            if request.method == "POST" and form.validate_on_submit():
                ajaran = form.tahunAjaran.data
                status = form.status.data

                model.th_ajaran = ajaran
                model.is_active = status

                model.save(model)

                flash("Data tahun ajaran telah ditambahkan.", "success")
                return redirect(url_for("admin2.get_ajaran"))

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
            model = TahunAjaranModel
            get_one = model.get_one(id=id)

            form.tahunAjaran.data = get_one.th_ajaran
            form.status.data = get_one.is_active

            if request.method == "POST" and form.validate_on_submit():
                ajaran = request.form.get("tahunAjaran")
                status = request.form.get("status")

                get_one.th_ajaran = ajaran
                get_one.is_active = status

                model.update()

                flash("Data tahun ajaran telah diperbaharui.", "success")

                return redirect(url_for("admin2.get_ajaran"))

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
            model = TahunAjaranModel
            get_one = model.get_one(id=id)
            model.delete(get_one)

            flash("Data tahun ajaran telah dihapus.", "success")

            return redirect(url_for("admin2.get_ajaran"))
        else:
            abort(401)

    # NOTE: ================== MASTER DATA KELAS =====================================
    @admin2.route("data-kelas")
    @login_required
    def get_kelas():
        if current_user.group == "admin":
            form = FormKelas()

            kelas_model = KelasModel
            gets_kelas = kelas_model.get_all()
            for i in gets_kelas:
                get_count_l = (
                    SiswaModel.query.filter_by(kelas_id=i.id)
                    .filter_by(gender="laki-laki")
                    .count()
                )
                get_count_p = (
                    SiswaModel.query.filter_by(kelas_id=i.id)
                    .filter_by(gender="perempuan")
                    .count()
                )

                get_kelas = kelas_model.get_filter_by(id=i.id)
                get_kelas.jml_laki = get_count_l
                get_kelas.jml_perempuan = get_count_p
                get_kelas.jml_seluruh = get_count_l + get_count_p

                kelas_model.commit()

            user = dbs.get_one(AdminModel, user_id=current_user.id)
            session.update(
                first_name=user.first_name.title(), last_name=user.last_name.title()
            )
            return render_template(
                "admin/master/kelas/data_kelas.html",
                model=gets_kelas,
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

            if request.method == "POST" and form.validate_on_submit():
                kelas = form.kelas.data
                kelas_model = KelasModel(kelas)

                if kelas_model.get_filter_by(kelas=kelas):
                    print("Data Kelas Addddddaaaa")
                    flash(
                        f"Data kelas sudah ada.\\nPeriksa kembali inputan kelas.",
                        "error",
                    )

                    return redirect(url_for("admin2.get_kelas"))

                else:
                    kelas_model.save()

                    flash(
                        message=f"\\nData kelas telah ditambahkan.",
                        category="success",
                    )
                    return redirect(url_for("admin2.get_kelas"))

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
            kelas_model = KelasModel
            gets_kelas = kelas_model.get_all()

            get_kelas = kelas_model.get_filter_by(id=id)

            form.kelas.data = get_kelas.kelas
            form.jumlahLaki.data = get_kelas.jml_laki
            form.jumlahPerempuan.data = get_kelas.jml_perempuan
            form.jumlahSiswa.data = get_kelas.jml_seluruh

            if request.method == "POST":
                kelas = request.form.get("kelas")
                laki = request.form.get("jumlahLaki")
                perempuan = request.form.get("jumlahPerempuan")
                seluruh = int(laki) + int(perempuan)

                get_kelas.kelas = kelas
                get_kelas.jml_laki = laki
                get_kelas.jml_perempuan = perempuan
                get_kelas.jml_seluruh = seluruh

                kelas_model.commit()

                flash("Data kelas telah diperbaharui.", "success")
                return redirect(url_for("admin2.get_kelas"))

            user = dbs.get_one(AdminModel, user_id=current_user.id)
            session.update(
                first_name=user.first_name.title(), last_name=user.last_name.title()
            )

            return render_template(
                "admin/master/kelas/data_kelas.html",
                form=form,
                r=request,
                model=gets_kelas,
                id=id,
            )
        else:
            abort(401)

    @admin2.route("delete-kelas/<int:id>", methods=["GET", "DELETE"])
    @login_required
    def delete_kelas(id):
        if current_user.group == "admin":
            kelas_model = KelasModel
            get_kelas = kelas_model.get_filter_by(id=id)
            kelas_model.delete(get_kelas)
            flash(
                f"Data kelas telah dihapus",
                "success",
            )
            return redirect(url_for("admin2.get_kelas"))
        else:
            abort(401)

    # NOTE: ================== MASTER DATA HARI =====================================
    @admin2.route("data-hari")
    @login_required
    def get_hari():
        if current_user.group == "admin":
            model = HariModel.get_all()

            user = dbs.get_one(AdminModel, user_id=current_user.id)
            session.update(
                first_name=user.first_name.title(), last_name=user.last_name.title()
            )
            return render_template("admin/master/hari/data_hari.html", model=model)
        else:
            abort(401)

    @admin2.route("add-hari", methods=["GET", "POST"])
    @login_required
    def add_hari():
        if current_user.group == "admin":
            form = FormHari(request.form)
            model = HariModel

            if request.method == "POST" and form.validate_on_submit():
                hari = form.hari.data

                model.hari = hari

                model.save(model)

                flash("Data hari telah ditambahkan.", "success")

                return redirect(url_for("admin2.get_hari"))

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
            model = HariModel
            get_one = model.get_one(id=id)

            model.delete(get_one)
            flash("Data hari telah dihapus.", "success")
            return redirect(url_for("admin2.get_hari"))
        else:
            abort(401)

    # NOTE: ================== MASTER DATA WALI KELAS =====================================
    @admin2.route("data-wali-kelas")
    @login_required
    def get_wali():
        if current_user.group == "admin":
            wali_model = WaliKelasModel
            get_gurus = db.session.query(GuruModel).filter(UserModel.group == "guru")
            gets_kelas = KelasModel.get_all()
            get_walis = wali_model.get_all()

            form = FormWaliKelas(request.form)
            for i in get_gurus:
                form.namaGuru.choices.append(
                    (i.user.id, i.first_name.title() + "" + i.last_name.title())
                )

            for i in gets_kelas:
                form.kelas.choices.append((i.id, i.kelas))

            user = dbs.get_one(AdminModel, user_id=current_user.id)
            session.update(
                first_name=user.first_name.title(), last_name=user.last_name.title()
            )
            return render_template(
                "admin/master/wali_kelas/data_wali.html",
                model=get_walis,
                form=form,
                jsonGuru=get_gurus,
                jsonKelas=gets_kelas,
                r=request,
            )
        else:
            abort(401)

    @admin2.route("tambah-wali", methods=["GET", "POST"])
    @login_required
    def add_wali():
        if current_user.group == "admin":
            form = FormWaliKelas(request.form)
            data_wali = WaliKelasModel.get_all()
            data_guru = GuruModel.get_all()
            data_kelas = KelasModel.get_all()

            for g in data_guru:
                form.namaGuru.choices.append(
                    (g.user_id, f"{g.first_name.title()} {g.last_name.title()}")
                )

            for item in data_kelas:
                form.kelas.choices.append((item.id, item.kelas))

            if request.method == "POST" and form.validate_on_submit():
                guru = form.namaGuru.data
                kelas = form.kelas.data

                wali_model = WaliKelasModel(guru, kelas)

                wali_model.save()

                return redirect(url_for("admin2.get_wali"))

            else:
                return render_template(
                    "admin/master/wali_kelas/data_wali.html",
                    form=form,
                    model=data_wali,
                    r=request,
                )

        abort(401)

    @admin2.route("update-wali", methods=["GET", "POST"])
    @login_required
    def edit_wali():
        if current_user.group == "admin":
            form = FormEditWaliKelas()
            id = request.args.get("id")
            data_kelas = KelasModel.get_all()
            data_guru = (
                db.session.query(GuruModel).filter(UserModel.group == "guru").all()
            )
            data_wali = WaliKelasModel.get_all()

            for i in data_guru:
                form.namaGuru.choices.append(
                    (i.user_id, f"{i.first_name.title()} {i.last_name.title()}")
                )

            for i in data_kelas:
                form.kelas.choices.append((i.id, i.kelas))

            wali = WaliKelasModel.get_filter_by(id=id)

            form.namaGuru.default = wali.guru_id
            form.kelas.default = wali.kelas_id
            form.process()

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
                model=data_wali,
                r=request,
                id=id,
            )

        else:
            abort(401)

    @admin2.route("delete-wali/<int:id>", methods=["GET", "POST"])
    @login_required
    def delete_wali(id):
        if current_user.group == "admin":
            wali_model = WaliKelasModel
            get_wali = wali_model.get_filter_by(id=id)
            wali_model.delete(get_wali)

            flash("Data wali kelas telah dihapus.", "success")
            return redirect(url_for("admin2.get_wali"))
        else:
            abort(401)

    # NOTE: ================== MASTER DATA GURU BK=====================================
    @admin2.route("data-guru-bk", methods=["GET"])
    @login_required
    def get_bk():
        if current_user.group == "admin":
            guru_bk_model = GuruBKModel
            get_all_bk = guru_bk_model.get_all()
            get_all_guru = GuruModel.get_all()
            form = FormGuruBK(request.form)
            for i in get_all_guru:
                form.namaGuru.choices.append(
                    (i.user_id, i.first_name.title() + " " + i.last_name.title())
                )

            user = dbs.get_one(AdminModel, user_id=current_user.id)
            session.update(
                first_name=user.first_name.title(), last_name=user.last_name.title()
            )
            return render_template(
                "admin/master/guru_bk/data_guru_bk.html",
                model=get_all_bk,
                form=form,
                jsonGuru=get_all_guru,
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

            if form.validate_on_submit() and request.method == "POST":
                guru = form.namaGuru.data
                bk_data = GuruBKModel(guru)
                bk_data.save()

                flash("Data Guru BK\\ntelah ditambahkan.", "success")

                return redirect(url_for("admin2.get_bk"))

            return render_template(
                "admin/master/guru_bk/data_guru_bk.html",
                form=form,
                model=data_bk,
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

            if request.method == "POST" and request.method == "POST":
                guru_id = request.form.get("namaGuru")

                get_bk.guru_id = guru_id
                db.session.commit()

                flash("Data Guru BK\\ntelah diperbaharui.", "success")

                return redirect(url_for("admin2.get_bk"))

            return render_template(
                "admin/master/guru_bk/data_guru_bk.html",
                form=form,
                model=data_bk,
                r=request,
                id=id,
            )

        else:
            abort(401)

    @admin2.route("delete-guru-bk/<int:id>", methods=["GET", "DELETE"])
    @login_required
    def delete_bk(id):
        if current_user.group == "admin":
            bk_model = GuruBKModel
            get_bk = bk_model.get_filter_by(id=id)

            if not get_bk:
                flash(
                    "Terjadi kelasahan!\\nID tidak ditemukan dalam database.", "error"
                )

            bk_model.delete(get_bk)

            flash("Data Guru BK telah dihapus.", "success")

            return redirect(url_for("admin2.get_bk"))

        else:
            abort(401)

    # NOTE: ================== MASTER DATA KEPALA SEKOLAH =====================================
    @admin2.route("data-kepsek", methods=["GET"])
    @login_required
    def get_kepsek():
        if current_user.group == "admin":
            get_kepsek = KepsekModel.get_all()
            get_guru = GuruModel.get_all()

            form = FormKepsek(request.form)
            if not get_kepsek:
                for i in get_guru:
                    form.namaGuru.choices.append(
                        (i.user_id, i.first_name.title() + "" + i.last_name.title())
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
                model=get_kepsek,
                form=form,
                jsonGuru=get_guru,
                status=status,
            )
        else:
            abort(401)

    @admin2.route("add-kepsek", methods=["GET", "POST"])
    @login_required
    def add_kepsek():
        if current_user.group == "admin":
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

    @admin2.route("delete-kepsek/<int:id>", methods=["GET", "DELETE"])
    @login_required
    def delete_kepsek(id):
        if current_user.group == "admin":
            model = KepsekModel
            get_one = model.get_one(id=id)

            model.delete(get_one)

            flash("Data Kepsek telah dihapus.", "success")
            return redirect(url_for("admin2.get_kepsek"))
        else:
            abort(401)


class JadwalMengajar:
    # NOTE: ================== DATA JADWAL MENGAAJAR =====================================
    @admin2.route("data-jawdwal-mengajar")
    @login_required
    def get_jadwal():
        if current_user.group == "admin":
            get_jadwal = (
                db.session.query(MengajarModel)
                .join(TahunAjaranModel)
                .join(SemesterModel)
                .filter(TahunAjaranModel.is_active == "1")
                .filter(SemesterModel.is_active == "1")
                .all()
            )
            data = []
            for i in get_jadwal:
                data.append(
                    dict(
                        id=i.id,
                        kode_mengajar=i.kode_mengajar,
                        first_name=i.guru.first_name.title(),
                        last_name=i.guru.last_name.title(),
                        mapel=i.mapel.mapel,
                        jam_ke=i.jam_ke,
                        hari=i.hari.hari,
                        jam_mulai=i.jam_mulai,
                        jam_selesai=i.jam_selesai,
                        kelas=i.kelas.kelas,
                        semester=i.semester.semester,
                        tahun_ajaran=i.tahun_ajaran.th_ajaran,
                    ),
                )

            user = dbs.get_one(AdminModel, user_id=current_user.id)
            session.update(
                first_name=user.first_name.title(), last_name=user.last_name.title()
            )
            return render_template("admin/jadwal_mengajar/data_jadwal.html", model=data)
        else:
            abort(401)

    @admin2.route("tambah-jadwal-mengajar", methods=["GET", "POST"])
    @login_required
    def add_jadwal():
        if current_user.group == "admin" and current_user.is_authenticated:
            form = FormJadwalMengajar(request.form)
            kodeMengajar = "MPL-" + str(time.time()).rsplit(".", 1)[1]

            get_semester = SemesterModel.query.all()
            ta = None
            sms = None
            ta_id = None
            sms_id = None
            for i in get_semester:
                if i.is_active == "1":
                    sms = i.semester
                    sms_id = i.id

            get_th_ajaran = TahunAjaranModel.query.all()
            for i in get_th_ajaran:
                if i.is_active == "1":
                    ta = i.th_ajaran
                    ta_id = i.id

            get_guru = (
                db.session.query(GuruModel)
                .join(UserModel)
                .filter(UserModel.group == "guru")
                .all()
            )
            for i in get_guru:
                form.namaGuru.choices.append(
                    (i.user_id, i.first_name.title() + " " + i.last_name.title())
                )

            get_mapels = MapelModel.get_all()
            for i in get_mapels:
                form.namaMapel.choices.append((i.id, i.mapel.title()))

            get_hari = HariModel.query.all()
            for i in get_hari:
                form.hari.choices.append((i.id, i.hari.title()))

            get_kelas = KelasModel.get_all()
            for i in get_kelas:
                form.kelas.choices.append((i.id, i.kelas))

            form.kode.data = kodeMengajar
            form.semester.data = sms.title()
            form.ta.data = ta_id
            form.sms.data = sms_id
            form.tahunAjaran.data = ta

            if request.method == "POST" and form.validate_on_submit():
                kode_mengajar = request.form.get("kode")
                tahun_ajaran_id = request.form.get("ta")
                semester_id = request.form.get("sms")
                guru_id = request.form.get("namaGuru")
                mapel_id = request.form.get("namaMapel")
                hari_id = request.form.get("hari")
                kelas_id = request.form.get("kelas")

                jam_mulai2 = request.form.get("waktuMulai2")
                jam_selesai2 = request.form.get("waktuSelesai2")
                jam_ke = request.form.get("jamKe")

                mengajar_model = MengajarModel(
                    guruId=guru_id,
                    hariId=hari_id,
                    jamMulai=jam_mulai2,
                    jamSelesai=jam_selesai2,
                    kelasId=kelas_id,
                    semesterId=semester_id,
                    tahunAjaranId=tahun_ajaran_id,
                    mapelId=mapel_id,
                    jamKe=jam_ke,
                )
                mengajar_model.save()

                flash("Data jadwal telah ditambahkan.", "success")
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
            form = FormUpdateJadwalMengajar(request.form)
            mengajar_model = MengajarModel
            get_jadwal = mengajar_model.get_one(id=id)

            data_jadwal = dict(
                id=get_jadwal.id,
                kode_mengajar=get_jadwal.kode_mengajar,
                guru_id=get_jadwal.guru_id,
                first_name=get_jadwal.guru.first_name,
                last_name=get_jadwal.guru.last_name,
                mapel=get_jadwal.mapel.mapel,
                mapel_id=get_jadwal.mapel_id,
                jam_ke=get_jadwal.jam_ke,
                hari_id=get_jadwal.hari_id,
                hari=get_jadwal.hari.hari,
                jam_mulai=get_jadwal.jam_mulai,
                jam_selesai=get_jadwal.jam_selesai,
                kelas_id=get_jadwal.kelas_id,
                kelas=get_jadwal.kelas.kelas,
                semester=get_jadwal.semester.semester,
                tahun_ajaran=get_jadwal.tahun_ajaran.th_ajaran,
            )

            get_guru = GuruModel.get_all()
            for i in get_guru:
                form.namaGuru.choices.append(
                    (i.user_id, i.first_name.title() + " " + i.last_name.title())
                )

            get_mapel = MapelModel.get_all()
            for i in get_mapel:
                form.namaMapel.choices.append((i.id, i.mapel.title()))

            get_hari = HariModel.query.all()
            for i in get_hari:
                form.hari.choices.append((i.id, i.hari.title()))

            get_kelas = KelasModel.get_all()
            for i in get_kelas:
                form.kelas.choices.append((i.id, i.kelas))

            form.kode.default = data_jadwal["kode_mengajar"]
            form.tahunAjaran.default = data_jadwal["tahun_ajaran"]
            form.namaGuru.default = data_jadwal["guru_id"]
            form.semester.default = data_jadwal["semester"].upper()
            form.namaMapel.default = data_jadwal["mapel_id"]
            form.hari.default = data_jadwal["hari_id"]
            form.kelas.default = data_jadwal["kelas_id"]
            form.waktuMulai2.default = data_jadwal["jam_mulai"]
            form.waktuSelesai2.default = data_jadwal["jam_selesai"]
            form.jamKe.default = data_jadwal["jam_ke"]
            form.process()

            if request.method == "POST":
                guru_id = request.form.get("namaGuru")
                mapel_id = request.form.get("namaMapel")
                hari_id = request.form.get("hari")
                jam_mulai = request.form.get("waktuMulai2")
                jam_selesai = request.form.get("waktuSelesai2")
                kelas_id = request.form.get("kelas")
                jam_ke = request.form.get("jamKe")

                if (
                    guru_id == ""
                    or mapel_id == ""
                    or hari_id == ""
                    or (kelas_id == "" or kelas_id is None)
                    or jam_mulai == ""
                    or jam_selesai == ""
                    or jam_ke == ""
                ):
                    flash(
                        "Perbaharui jadwal gagal.\\nTidak boleh ada form yang kosong!",
                        "error",
                    )
                else:
                    get_jadwal.guru_id = guru_id
                    get_jadwal.hari_id = hari_id
                    get_jadwal.mapel_id = mapel_id
                    get_jadwal.jam_mulai = jam_mulai
                    get_jadwal.jam_selesai = jam_selesai
                    get_jadwal.kelas_id = kelas_id
                    get_jadwal.jam_ke = jam_ke
                    mengajar_model.commit()
                    flash("Data Jadwal telah di perbaharui.", "success")

                    return redirect(url_for("admin2.get_jadwal"))

            user = dbs.get_one(AdminModel, user_id=current_user.id)
            session.update(
                first_name=user.first_name.title(), last_name=user.last_name.title()
            )

            return render_template(
                "admin/jadwal_mengajar/edit_jadwal.html", model=data_jadwal, form=form
            )

    @admin2.route("delete-jadwal/<int:id>", methods=["GET", "DELETE"])
    @login_required
    def delete_jadwal(id):
        if current_user.group == "admin":
            jadwal_model = MengajarModel
            get_jadwal = jadwal_model.get_one(id=id)

            if not get_jadwal:
                flash("Terjadi kesalah.\\nPeriksa kembali id jadwal.", "error")

            jadwal_model.delete(get_jadwal)

            flash("Data jadwal telah dihapus.", "success")
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
