import hashlib
from time import sleep
import qrcode, os
from sqlalchemy import and_, func
from werkzeug.utils import secure_filename
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import HorizontalBarsDrawer
from flask import (
    Blueprint,
    jsonify,
    make_response,
    request,
    url_for,
)
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.lib.base_model import BaseModel
from app.lib.date_time import (
    format_date_today,
    format_datetime_id,
    format_indo,
    today_,
    utc_makassar,
)
from app.lib.status_code import *
from app.models.data_model import PelanggaranModel
from app.models.master_model import (
    HariModel,
    KelasModel,
    MapelModel,
    MengajarModel,
    SemesterModel,
    WaliKelasModel,
)
from app.models.user_details_model import SiswaModel
from app.models.user_model import UserModel
from app.extensions import db
from app.lib.uploader import upload_resize_photo, uploads
from datetime import datetime
from app.models.data_model import AbsensiModel
from PIL import Image

siswa = Blueprint(
    "siswa",
    __name__,
    url_prefix="/api/v2/student",
    static_url_path="/path/",
    static_folder="../static/",
)
qc_folder = os.getcwd() + "/app/api/static/img/siswa/qr_code/"


# NOTE : MANUAL STATIC FOLDER
# @siswa.route('api/<path:filename>')
# def static(filename):
#     dir = send_from_directory('api/static', filename)
#     return dir

dic_data = lambda **args: args


@siswa.route("/get-all")
def get():
    # model = db.session.query(UserModel, SiswaModel)\
    #                   .join(SiswaModel).all()
    model = (
        db.session.query(SiswaModel).join(KelasModel)
        # .order_by(SiswaModel.first_name.asc())
        .order_by(SiswaModel.kelas_id.asc(), SiswaModel.first_name.asc())
    )
    data = []
    path_file = os.getcwd() + "/app/api/static/img/siswa/"
    list_file = os.listdir(path_file + "foto/")
    list_qr_file = os.listdir(path_file + "qr_code/")

    for user in model:
        if user.pic and user.pic not in list_file:
            sql_siswa = SiswaModel.query.filter_by(id=user.id).first()
            sql_siswa.pic = None
            db.session.commit()

        if user.qr_code and user.qr_code not in list_qr_file:
            sql_siswa = SiswaModel.query.filter_by(id=user.id).first()
            sql_siswa.qr_code = None
            db.session.commit()
        data.append(
            {
                "id": user.user.id,
                "nisn": user.user.username,
                "first_name": user.first_name.title(),
                "last_name": user.last_name.title(),
                "gender": user.gender.title(),
                "kelas": user.kelas.kelas if user.kelas_id else "-",
                "kelas_id": user.kelas_id,
                "tempat_lahir": user.tempat_lahir.title() if user.tempat_lahir else "-",
                # 'tgl_lahir': user.tgl_lahir if user.tgl_lahir else '-',
                "tgl_lahir": format_indo(user.tgl_lahir) if user.tgl_lahir else "-",
                "agama": user.agama.title() if user.agama else "-",
                "alamat": user.alamat.title() if user.alamat else "-",
                "nama_ortu": user.nama_ortu_or_wali if user.nama_ortu_or_wali else "-",
                "picture": url_for(".static", filename="img/siswa/foto/" + user.pic)
                if user.pic
                else None,
                "pic_name": user.pic if user.pic else "-",
                "telp": user.no_telp if user.no_telp else "-",
                "qr_code": url_for(
                    ".static", filename="img/siswa/qr_code/" + user.qr_code
                )
                if user.qr_code
                else None,
                "active": "Aktif" if user.user.is_active == "1" else "Non-Aktif",
                "join": format_datetime_id(user.user.join_date)
                if user.user.join_date
                else "-",
                "type": user.user.group.upper(),
                "last_update": format_indo(user.user.update_date)
                if user.user.update_date
                else "-",
                "last_login": format_datetime_id(user.user.user_last_login)
                if user.user.user_last_login
                else "-",
                "logout": user.user.user_logout if user.user.user_logout else "-",
            }
        )
        # file = path_file + user.pic if user.pic else ""
        # print(file)
    return jsonify(data=data), HTTP_200_OK


@siswa.route("/get-siswa-kelas/<kelas_id>")
def get_by_kelas(kelas_id):
    # model = db.session.query(UserModel, SiswaModel)\
    #                   .join(SiswaModel).all()
    base = BaseModel(SiswaModel)
    model = base.get_all_filter_by(kelas_id=kelas_id)
    data = []
    for user in model:
        data.append(
            {
                "id": user.user.id,
                "nisn": user.user.username,
                "first_name": user.first_name.title(),
                "last_name": user.last_name.title(),
                "gender": user.gender.title(),
                "kelas": user.kelas.kelas if user.kelas_id else "-",
                "tempat_lahir": user.tempat_lahir.title() if user.tempat_lahir else "-",
                # 'tgl_lahir': user.tgl_lahir if user.tgl_lahir else '-',
                "tgl_lahir": format_indo(user.tgl_lahir) if user.tgl_lahir else "-",
                "agama": user.agama.title() if user.agama else "-",
                "alamat": user.alamat.title() if user.alamat else "-",
                "nama_ortu": user.nama_ortu_or_wali if user.nama_ortu_or_wali else "-",
                "picture": url_for(".static", filename="img/siswa/foto/" + user.pic)
                if user.pic
                else None,
                "pic_name": user.pic if user.pic else "-",
                "telp": user.no_telp if user.no_telp else "-",
                "qr_code": url_for(
                    ".static", filename="img/siswa/qr_code/" + user.qr_code
                )
                if user.qr_code
                else None,
                "active": "Aktif" if user.user.is_active == "1" else "Non-Aktif",
                "join": format_datetime_id(user.user.join_date)
                if user.user.join_date
                else "-",
                "type": user.user.group.upper(),
                "last_update": format_indo(user.user.update_date)
                if user.user.update_date
                else "-",
                "last_login": format_datetime_id(user.user.user_last_login)
                if user.user.user_last_login
                else "-",
                "logout": user.user.user_logout if user.user.user_logout else "-",
            }
        )
    return jsonify(data=data), HTTP_200_OK


# @siswa.route("/single/<>", methods=["GET", "PUT", "DELETE"])
@siswa.route("/single", methods=["GET", "PUT", "DELETE"])
@jwt_required()
def get_single():
    # base_user = BaseModel(UserModel)
    # user = base_user.get_one_or_none(id=id)
    id = get_jwt_identity().get("id")
    base = BaseModel(SiswaModel)
    model = base.get_one_or_none(user_id=id)
    sql_wali = WaliKelasModel.query.filter_by(kelas_id=model.kelas_id).first()
    hari = format_indo(datetime.date(datetime.today()))
    if request.method == "GET":
        if not model:
            return jsonify(msg="Data user tidak ditemukan."), HTTP_404_NOT_FOUND
        return (
            jsonify(
                id=model.user.id,
                nisn=model.user.username,
                first_name=model.first_name.title(),
                last_name=model.last_name.title(),
                kelas=model.kelas.kelas if model.kelas.kelas else None,
                kelas_id=model.kelas_id if model.kelas_id else None,
                gender=model.gender.title() if model.gender else None,
                tempat_lahir=model.tempat_lahir.title() if model.tempat_lahir else None,
                tgl_lahir=str(model.tgl_lahir) if model.tgl_lahir else None,
                agama=model.agama.title() if model.agama else None,
                alamat=model.alamat.title() if model.alamat else None,
                nama_ortu=model.nama_ortu_or_wali.title()
                if model.nama_ortu_or_wali
                else None,
                telp=model.no_telp if model.no_telp else None,
                qr_code=url_for(
                    ".static", filename="img/siswa/qr_code/" + model.qr_code
                )
                if model.qr_code
                else None,
                picture=url_for("siswa.static", filename="img/siswa/foto/" + model.pic)
                if model.pic
                else None,
                wali_kelas=f"{sql_wali.guru.first_name} {sql_wali.guru.last_name}",
                hari=hari,
            ),
            HTTP_200_OK,
        )

    elif request.method == "PUT":
        if not model:
            return jsonify(msg="Data not found."), HTTP_404_NOT_FOUND
        else:
            nisn = request.json.get("nisn")
            first_name = request.json.get("first_name")
            last_name = request.json.get("last_name")
            gender = request.json.get("gender")
            tmpt_lahir = request.json.get("tempat")
            tgl_lahir = request.json.get("tgl")
            alamat = request.json.get("alamat")
            agama = request.json.get("agama")
            telp = request.json.get("telp")
            kelas = request.json.get("kelas")
            nama_ortu = request.json.get("nama_ortu")
            # active = request.json.get('active')

            model.user.username = nisn
            model.firs_name = first_name
            model.last_name = last_name
            model.gender = gender
            model.tempat_lahir = tmpt_lahir
            model.tgl_lahir = tgl_lahir
            # model.tgl_lahir = string_format(tgl_lahir)
            model.alamat = alamat
            model.agama = agama
            model.no_telp = telp
            model.kelas_id = kelas
            model.nama_ortu_or_wali = nama_ortu
            model.user.update_date = utc_makassar()
            # model.user.is_active = active

            base.edit()

            baseKelas = BaseModel(KelasModel)
            kelasModel = baseKelas.get_one(id=kelas)
            countSiswaGender = (
                db.session.query(func.count(SiswaModel.kelas_id))
                .filter(SiswaModel.kelas_id == kelas)
                .filter(SiswaModel.gender == gender)
                .scalar()
            )
            countSiswaAll = (
                db.session.query(func.count(SiswaModel.kelas_id))
                .filter(SiswaModel.kelas_id == kelas)
                .scalar()
            )

            if gender == "laki-laki":
                kelasModel.jml_laki = countSiswaGender
            elif gender == "perempuan":
                kelasModel.jml_perempuan = countSiswaGender

            kelasModel.jml_seluruh = countSiswaAll
            baseKelas.edit()

            return (
                jsonify(msg=f"Update data {model.first_name} successfull."),
                HTTP_200_OK,
            )

    elif request.method == "DELETE":
        if not model:
            return jsonify(msg="Data Not Found."), HTTP_404_NOT_FOUND
        else:
            # base.delete(model)
            # # base_user.delete(user)
            """
            Check file before delete user and file
            """
            dir_file = os.getcwd() + "/app/api/static/img/siswa/foto/"
            qr_file = os.getcwd() + "/app/api/static/img/siswa/qr_code"
            # file = dir_file + model.pic

            if model.pic and model.qr_code:
                file = os.path.join(dir_file, model.pic)
                file_qr = os.path.join(qr_file, model.qr_code)
                os.unlink(file)
                sleep(2)
                os.unlink(file_qr)
                base_user = BaseModel(UserModel)
                model_user = base_user.get_one(id=id)
                base.delete(model_user)
                return jsonify(msg="Data has been deleted."), HTTP_204_NO_CONTENT
            elif model.qr_code or model.pic:
                file_qr = (
                    os.path.join(qr_file, model.qr_code) if model.qr_code else None
                )
                file = os.path.join(dir_file, model.pic) if model.pic else None
                if file_qr is not None:
                    os.unlink(file_qr)
                    base_user = BaseModel(UserModel)
                    model_user = base_user.get_one(id=id)
                    base.delete(model_user)
                    return jsonify(msg="Data has been deleted."), HTTP_204_NO_CONTENT

                os.unlink(file)
                base_user = BaseModel(UserModel)
                model_user = base_user.get_one(id=id)
                base.delete(model_user)
                return jsonify(msg="Data has been deleted."), HTTP_204_NO_CONTENT
            else:
                base_user = BaseModel(UserModel)
                model_user = base_user.get_one(id=id)
                base.delete(model_user)
                return jsonify(msg="Data has been deleted."), HTTP_204_NO_CONTENT


# generate qr code
@siswa.route("/generate-qc", methods=["GET", "PUT"])
def generate_qc():
    base = BaseModel(SiswaModel)
    id = request.args.get("id")
    model = base.get_one(user_id=id)

    if not model:
        return jsonify(msg="User not found."), HTTP_404_NOT_FOUND
    else:
        qc = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L)
        qc.add_data(model.user.username)
        qc_img = qc.make_image(
            image_factory=StyledPilImage, module_drawer=HorizontalBarsDrawer(), fit=True
        )
        enc_file_name = hashlib.md5(
            secure_filename(model.user.username).encode("utf-8")
        ).hexdigest()
        first_name = (
            model.first_name
            if len(model.first_name) != 2
            else model.last_name.split(" ", 1)[0]
        )
        path_file = (
            qc_folder
            + model.kelas.kelas
            + "_"
            + first_name.lower()
            + "_"
            + enc_file_name
            + ".png"
        )
        qc_img.save(path_file)

        model.qr_code = (
            model.kelas.kelas + "_" + first_name.lower() + "_" + enc_file_name + ".png"
        )

        base.edit()

        return (
            jsonify(
                id=model.user.id,
                nisn=model.user.username,
                qr_code=url_for(
                    ".static",
                    filename="img/siswa/qr_code/" + model.qr_code,
                ),
            ),
            HTTP_200_OK,
        )


# upload photos
@siswa.put("upload-photo")
@siswa.post("upload-photo")
def upload_photo():
    base = BaseModel(SiswaModel)
    id = request.args.get("id")
    model = base.get_one(user_id=id)
    if not model:
        return jsonify(msg="Data not found"), HTTP_404_NOT_FOUND
    else:
        f = request.files["images"]

        first_name = (
            model.first_name
            if len(model.first_name) != 2
            else model.last_name.split(" ", 1)[0]
        )
        user_first_name = first_name.replace(" ", "_").lower()
        up_risize = upload_resize_photo(f, user_first_name, model.kelas.kelas)

        # upload_file = uploads(f, user_first_name, model.kelas.kelas)
        # if upload_file["status"] == "ok":
        #     model.pic = upload_file["photo_name"]
        #     base.edit()
        #     return jsonify(msg="upload photo success"), HTTP_200_OK

        if up_risize["status"] == "Ok":
            model.pic = up_risize["filename"]
            base.edit()
            return jsonify(msg="Unggah Foto Berhasil."), HTTP_200_OK


# GET SISWA BY NISN
"""
    URL ini hanya di akses oleh guru,
    ketika melakukan absensi, dengan
    mengambil nisn sebagai [query paramater]
"""


@siswa.get("single-siswa")
def get_siswa_by_nisn():
    nisn = request.args.get("nisn")
    sql_user = UserModel.query.filter_by(username=nisn).first()
    sql_semester = SemesterModel.query.filter_by(is_active=1).first()
    today = format_date_today(datetime.today())

    if sql_user:
        sql_siswa = SiswaModel.query.filter_by(user_id=sql_user.id).first()

        return (
            jsonify(
                nisn=sql_user.username,
                first_name=sql_siswa.first_name.title(),
                last_name=sql_siswa.last_name.title(),
                gender=sql_siswa.gender,
                kelas=sql_siswa.kelas.kelas,
                picture=url_for(".static", filename=f"img/siswa/foto/{sql_siswa.pic}")
                if sql_siswa.pic
                else sql_siswa.pic,
                semester=sql_semester.semester.title(),
                today=today,
            ),
            HTTP_200_OK,
        )
    else:
        return jsonify(msg="QR Code tidak sah"), HTTP_404_NOT_FOUND


@siswa.get("daftar-mapel")
@jwt_required()
def mapel_kelas():
    user_id = get_jwt_identity().get("id")
    sql_siswa = SiswaModel.query.filter_by(user_id=user_id).first()
    sql_semester = SemesterModel.query.filter_by(is_active=1).first()
    sql_mapel = (
        MengajarModel.query.filter_by(kelas_id=sql_siswa.kelas_id)
        .join(MapelModel)
        .join(SemesterModel)
        .filter(MengajarModel.semester_id == sql_semester.id)
        .group_by(MengajarModel.mapel_id)
        .order_by(MapelModel.mapel.asc())
        .all()
    )
    data = []
    for i in sql_mapel:
        data.append(
            {
                "id": i.mapel.id,
                "mapel": i.mapel.mapel,
                "kelas": i.kelas.kelas,
                "nama_guru": f"{i.guru.first_name} {i.guru.last_name}",
            }
        )
    response = make_response(jsonify(data))

    return response, HTTP_200_OK


@siswa.get("jadwal-belajar")
def getJadwalByHari():
    kelasId = request.args.get("kelasId")
    hariId = request.args.get("hariId")
    sql_semester = (
        db.session.query(SemesterModel).filter(SemesterModel.is_active == "1").scalar()
    )
    sql_mengajar = (
        db.session.query(MengajarModel)
        .filter(MengajarModel.kelas_id == kelasId)
        .filter(MengajarModel.semester_id == sql_semester.id)
        .filter(MengajarModel.hari_id == hariId)
    )

    data = []
    for i in sql_mengajar:
        data.append(
            {
                "id": i.id,
                "hari": i.hari.hari.title(),
                "mapel": i.mapel.mapel.title(),
                "jamMulai": i.jam_mulai,
                "jamSelesai": i.jam_selesai,
                "jamKe": i.jam_ke,
            }
        )

    return (
        jsonify(
            status="success",
            data=data,
        ),
        HTTP_200_OK,
    )


# @siswa.route("/daftar-pelanggar")
# @jwt_required()
# def get_daftar_pelanggar():
#     sql_pelanggar = (
#         db.session.query(
#             PelanggaranModel,
#             func.sum(JenisPelanggaranModel.poin_pelanggaran),
#         )
#         .join(JenisPelanggaranModel)
#         .join(SiswaModel)
#         .group_by(PelanggaranModel.siswa_id)
#         .order_by(func.sum(JenisPelanggaranModel.poin_pelanggaran.desc))
#         .limit(6)
#     )

#     data = []
#     new_data = []

#     if sql_pelanggar:
#         for i, poin in sql_pelanggar:
#             data.append(
#                 dic_data(
#                     id=i.id,
#                     poin=poin,
#                     nama_siswa=f"{i.siswa.first_name.title()} {i.siswa.last_name.title()}",
#                 )
#             )

#         for index, val in enumerate(data, start=1):
#             new_data.append(
#                 dic_data(
#                     urut=index,
#                     id=val["id"],
#                     poin=val["poin"],
#                     nama_siswa=val["nama_siswa"],
#                 )
#             )
#         return jsonify(data=new_data), HTTP_200_OK

#     else:
#         return jsonify(msg="Belum ada siswa yang melanggar"), HTTP_404_NOT_FOUND


@siswa.route("/jadwal-harian")
@jwt_required()
def get_jadwal_harian():
    hari = today_()
    user_id = get_jwt_identity().get("id")
    sql_siswa = SiswaModel.query.filter_by(user_id=user_id).first()
    sql_semester = (
        db.session.query(SemesterModel).filter(SemesterModel.is_active == 1).first()
    )
    sql_jadwal = (
        db.session.query(MengajarModel)
        .join(HariModel)
        .filter(MengajarModel.hari_id == HariModel.id)
        .filter(MengajarModel.kelas_id == sql_siswa.kelas_id)
        .filter(MengajarModel.semester_id == sql_semester.id)
        .filter(HariModel.hari == hari)
        .all()
    )
    data = []
    if sql_jadwal:
        for i in sql_jadwal:
            data.append(
                dic_data(
                    id=i.id,
                    mapel=i.mapel.mapel.title(),
                    mulai=i.jam_mulai,
                    selesai=i.jam_selesai,
                    jam_ke=i.jam_ke,
                    guru=f"{i.guru.first_name.title()} {i.guru.last_name.title()}",
                )
            )

        return jsonify(data=data), HTTP_200_OK
    return jsonify(msg="Jadwal hari ini tidak tersedia."), HTTP_404_NOT_FOUND


@siswa.route("/jadwal-pelajaran")
@jwt_required()
def get_jadwal_pelajaran():
    user_id = get_jwt_identity().get("id")
    sql_siswa = SiswaModel.query.filter_by(user_id=user_id).first()
    sql_sms = SemesterModel.query.filter_by(is_active=1).first()
    sql_jadwal = (
        db.session.query(MengajarModel)
        .filter(MengajarModel.kelas_id == sql_siswa.kelas_id)
        .filter(MengajarModel.semester_id == sql_sms.id)
        .group_by(MengajarModel.mapel_id)
        .order_by(MengajarModel.hari_id.asc())
        .all()
    )

    group_data = {}

    if sql_jadwal:
        for i in sql_jadwal:
            hari = i.hari.hari.title()

            if hari in group_data:
                group_data[hari].append(
                    dic_data(
                        id=i.id,
                        mapel=i.mapel.mapel,
                        mulai=i.jam_mulai,
                        selesai=i.jam_selesai,
                        jam_ke=i.jam_ke,
                        hari=i.hari.hari.title(),
                        guru=f"{i.guru.first_name.title()} {i.guru.last_name.title()}",
                    )
                )
            else:
                group_data[hari] = [
                    dic_data(
                        id=i.id,
                        mapel=i.mapel.mapel,
                        mulai=i.jam_mulai,
                        selesai=i.jam_selesai,
                        jam_ke=i.jam_ke,
                        hari=i.hari.hari.title(),
                        guru=f"{i.guru.first_name.title()} {i.guru.last_name.title()}",
                    )
                ]

        return jsonify(group_data), HTTP_200_OK
    else:
        return jsonify(msg="Data tidak ada."), HTTP_404_NOT_FOUND


@siswa.get("/riwayat-absen")
@jwt_required()
def riwayat_absen():
    user_id = get_jwt_identity().get("id")
    sql_user = SiswaModel.query.filter_by(user_id=user_id).first()
    sql_semester = SemesterModel.query.filter_by(is_active=1).first()
    sql_mengajar = (
        db.session.query(MengajarModel)
        .filter(MengajarModel.semester_id == sql_semester.id)
        .all()
    )
    sql_absen = (
        db.session.query(AbsensiModel)
        .filter(AbsensiModel.siswa_id == sql_user.user_id)
        .filter(AbsensiModel.mengajar_id.in_(k.id for k in sql_mengajar))
        .order_by(AbsensiModel.tgl_absen.asc())
        .all()
    )

    map_data = dict()
    if sql_absen:
        for item in sql_absen:
            mapel = item.mengajar.mapel.mapel

            if mapel in map_data:
                map_data[mapel].append(
                    dic_data(
                        id=item.id,
                        semester=item.mengajar.semester.semester,
                        nama=item.siswa.first_name + " " + item.siswa.last_name,
                        tgl_absen=format_indo(item.tgl_absen),
                        ket=item.ket,
                    )
                )
            else:
                map_data[mapel] = [
                    dic_data(
                        id=item.id,
                        semester=item.mengajar.semester.semester,
                        nama=item.siswa.first_name + " " + item.siswa.last_name,
                        tgl_absen=format_indo(item.tgl_absen),
                        ket=item.ket,
                    )
                ]

        map_data2 = dict()
        for k, v in map_data.items():
            mapel = k
            for index, item in enumerate(iterable=v, start=1):
                if mapel in map_data2:
                    map_data2[mapel].append(
                        dic_data(
                            id=item["id"],
                            tgl_absen=item["tgl_absen"],
                            ket=item["ket"],
                            urutan=index,
                        )
                    )
                else:
                    map_data2[mapel] = [
                        dic_data(
                            id=item["id"],
                            tgl_absen=item["tgl_absen"],
                            ket=item["ket"],
                            urutan=index,
                        )
                    ]

            """
            - Cara dibawah ini menggungakan jumlah data
            # for index, item in enumerate(iterable=v, start=1):
            #     if mapel in map_data2:
            #         map_data2[mapel][0]["data"].append(
            #             dic_data(
            #                 id=item["id"],
            #                 tgl_absen=item["tgl_absen"],
            #                 ket=item["ket"],
            #                 urutan=index,
            #             )
            #         )
            #     else:
            #         map_data2[mapel] = [
            #             dic_data(
            #                 jumlah_data=len(v),
            #                 data=[
            #                     dic_data(
            #                         id=item["id"],
            #                         tgl_absen=item["tgl_absen"],
            #                         ket=item["ket"],
            #                         urutan=index,
            #                     )
            #                 ],
            #             )
            #         ]

            """
        return jsonify(map_data2), HTTP_200_OK
    else:
        return jsonify(msg="Data tidak ada."), HTTP_404_NOT_FOUND


@siswa.route("/riwayat-pelanggaran")
@jwt_required()
def riwayat_pelanggaran():
    user_id = get_jwt_identity().get("id")
    sql_siswa = SiswaModel.query.filter_by(user_id=user_id).first()
    sql_pelanggaran = (
        db.session.query(PelanggaranModel)
        .filter(
            PelanggaranModel.siswa_id == sql_siswa.user_id,
        )
        .all()
    )

    data = []

    if sql_pelanggaran:
        for item in sql_pelanggaran:
            data.append(
                dic_data(
                    id=item.id,
                    nama_siswa=f"{item.siswa.first_name.title()} {item.siswa.last_name.title()}",
                    pelapor=f"{item.pelapor}",
                    note=item.jenis_pelanggaran.jenis_pelanggaran,
                    tgl_melanggar=format_indo(item.tgl_report),
                )
            )
        return jsonify(status="ok", data=data), HTTP_200_OK

    return jsonify(msg="Tidak ada pelanggaran."), HTTP_404_NOT_FOUND


@siswa.route("/get-siswa/single-object", methods=["GET", "PUT", "DELETE"])
def getSiswaSingleObject():
    user_id = request.args.get("siswa", type=int)

    sql_siswa = db.session.query(SiswaModel).filter_by(user_id=user_id).first()
    if request.method == "GET":
        data = dict()
        if sql_siswa:
            data.update(
                id=sql_siswa.user_id,
                nisn=sql_siswa.user.username,
                first_name=sql_siswa.first_name.title(),
                last_name=sql_siswa.last_name.title(),
                kelas_id=sql_siswa.kelas_id,
                kelas=sql_siswa.kelas.kelas,
                # kelas=sql_siswa.kelas.kelas,
            )

            return jsonify(data)

        else:
            msg = f"Data dengan ID {user_id} tidak ditemukan!"

            return jsonify(msg=msg), HTTP_404_NOT_FOUND

    # return jsonify(msg=f"Data dengan ID {user_id} tidak ditemukan!")

    # return jsonify(id=sql_siswa.id)
