from datetime import datetime
from flask import Blueprint, jsonify, request, url_for
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import and_
from app.lib.base_model import BaseModel
from app.lib.date_time import (
    format_date_today,
    format_datetime_id,
    format_indo,
    today_,
)
from app.lib.status_code import *
from app.models.data_model import AbsensiModel
from app.models.master_model import (
    HariModel,
    MengajarModel,
    SemesterModel,
    TahunAjaranModel,
    WaliKelasModel,
)
from app.models.user_details_model import GuruModel, SiswaModel
from app.models.user_model import UserModel
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

guru = Blueprint(
    "guru", __name__, url_prefix="/api/v2/guru", static_folder="../static/"
)


dic_data = lambda **args: args
single_data = lambda **args: dic_data(data=args)


@guru.route("/get-all")
def get():
    base_model = BaseModel(GuruModel)
    data = []
    for user in base_model.get_all():
        data.append(
            {
                "id": user.user_id,
                "nip": user.user.username,
                "first_name": user.first_name.title(),
                "last_name": user.last_name.title(),
                "gender": user.gender.title(),
                "agama": user.agama.title() if user.agama else "-",
                "alamat": user.alamat.title() if user.alamat else "-",
                "telp": user.telp if user.telp else "-",
                "active": True if user.user.is_active == "1" else False,
                "join": format_indo(user.user.join_date),
                "last_update": format_indo(user.user.update_date)
                if user.user.update_date
                else "-",
                "last_login": format_datetime_id(user.user.user_last_login)
                if user.user.user_last_login
                else "-",
                "type": user.user.group.upper(),
            }
        )
    return jsonify(data), HTTP_200_OK


@guru.route("single/<int:id>", methods=["GET", "PUT", "DELETE"])
def get_single_object(id):
    base = BaseModel(GuruModel)
    guru = base.get_one_or_none(user_id=id)

    if request.method == "GET":
        if not guru:
            return jsonify(msg="Data not found."), HTTP_404_NOT_FOUND
        else:
            return (
                jsonify(
                    id=guru.user.id,
                    nip=guru.user.username,
                    first_name=guru.first_name.title(),
                    last_name=guru.last_name.title(),
                    gender=guru.gender.title(),
                    agama=guru.agama.title(),
                    alamat=guru.alamat.title(),
                    telp=guru.telp,
                ),
                HTTP_200_OK,
            )

    elif request.method == "PUT":
        # NOTE : Check user before request
        if not guru:
            return jsonify(msg="Data is not found."), HTTP_404_NOT_FOUND
        else:
            # NOTE : REQUEST JSON TO SAVE CHANGES
            username = request.json.get("nip")
            first_name = request.json.get("first_name")
            last_name = request.json.get("last_name")
            gender = request.json.get("gender")
            agama = request.json.get("agama")
            alamat = request.json.get("alamat")
            telp = request.json.get("telp")

            guru.user.username = username
            guru.first_name = first_name
            guru.last_name = last_name
            guru.gender = gender
            guru.agama = agama
            guru.alamat = alamat
            guru.telp = telp

            base.edit()
            return (
                jsonify(msg=f"Data Guru: {guru.first_name} berhasil di perbaharui."),
                HTTP_200_OK,
            )

    elif request.method == "DELETE":
        # NOTE : CHECK USER BEFORE REQUEST
        if not guru:
            return jsonify(msg="Data is not found."), HTTP_404_NOT_FOUND
        else:
            base = BaseModel(UserModel)
            user = base.get_one_or_none(id=id)
            base.delete(user)
            return jsonify(msg="Data has been deleted."), HTTP_204_NO_CONTENT


@guru.route("/wali-kelas")
def get_wali_kelas():
    model = BaseModel(WaliKelasModel)
    wali_kelas = model.get_all()

    data = []
    for _ in wali_kelas:
        data.append(
            {
                "first_name": _.guru.first_name,
                "last_name": _.guru.last_name,
                "kelas": _.kelas.kelas,
            }
        )

    return jsonify(data=data), HTTP_200_OK


@guru.route("single-guru", methods=["GET", "PUT", "PATCH"])
@jwt_required()
def get_single_guru():
    """
    NEW GET SINGLE USER GURU VIA MOBILE
    """
    base = BaseModel(GuruModel)
    id = get_jwt_identity().get("id")
    guru = base.get_one_or_none(user_id=id)

    sql_guru_mapel = MengajarModel.query.filter_by(guru_id=id).first()

    if not guru:
        return jsonify(msg="Data Guru tidak ada."), HTTP_404_NOT_FOUND
    else:
        if request.method == "GET":
            return (
                jsonify(
                    id=guru.user.id,
                    nip=guru.user.username,
                    first_name=guru.first_name.title(),
                    last_name=guru.last_name.title(),
                    gender=guru.gender.title() if guru.gender else None,
                    agama=guru.agama.title() if guru.agama else None,
                    alamat=guru.alamat.title() if guru.alamat else None,
                    telp=guru.telp if guru.telp else None,
                    mapel=sql_guru_mapel.mapel.mapel.title(),
                ),
                HTTP_200_OK,
            )
        elif request.method == "PUT" or request.method == "PATCH":
            nip = request.json.get("nip")
            fullname = request.json.get("fullname")
            gender = request.json.get("gender")
            agama = request.json.get("agama")
            alamat = request.json.get("alamat")
            telp = request.json.get("telp")

            first_name, *last_name = fullname.split(" ", 1)

            guru.user.username = nip
            guru.first_name = first_name
            guru.last_name = last_name[0]
            guru.gender = guru.gender if not gender else gender.lower()
            guru.agama = guru.agama if not agama else agama.lower()
            guru.alamat = guru.alamat if not alamat else alamat
            guru.telp = guru.telp if not telp else telp

            base.update()

            return jsonify(msg="Data telah di perbaharui"), HTTP_200_OK


## * NOTE: ABSEN SISWA
# @guru.route("/absen-siswa", methods=["GET", "POST"])
# @jwt_required()
# def absen_siswa():
#     """
#     input absen siswa by guru via mobile (QR CODE)
#     """

#     if request.method == "GET":
#         kelas_id = request.args.get("kelas_id")
#         guru_id = get_jwt_identity().get("id")
#         sql_semester = SemesterModel.query.filter_by(is_active=1).first()

#         sql_mengajar = (
#             db.session.query(MengajarModel)
#             .filter(MengajarModel.guru_id == guru_id)
#             .filter(MengajarModel.kelas_id == kelas_id)
#             .filter(MengajarModel.semester_id == sql_semester.id)
#             .scalar()
#         )

#         if sql_mengajar:
#             return jsonify(mengajar_id=sql_mengajar.id), HTTP_200_OK
#         else:
#             return jsonify(msg="Data tidak ada."), HTTP_404_NOT_FOUND


@guru.get("/single-siswa")
@jwt_required()
def get_single_siswa():
    ## * Mengambil data siswa berdasarkan jadwal
    ## * Jika tidak ada jawdal hari ini maka scan qr tidak valid
    nisn = request.args.get("nisn")
    guru_id = get_jwt_identity().get("id")
    sql_user = UserModel.query.filter_by(username=nisn).first()
    if sql_user:
        sql_siswa = SiswaModel.query.filter_by(user_id=sql_user.id).first()
        sql_semester = SemesterModel.query.filter_by(is_active=1).first()
        sql_th_ajaran = TahunAjaranModel.query.filter_by(is_active=1).first()

        hari = today_()
        today = format_date_today(datetime.today())
        sql_mengajar = (
            db.session.query(MengajarModel)
            .join(HariModel)
            .filter(MengajarModel.guru_id == guru_id)
            .filter(MengajarModel.kelas_id == sql_siswa.kelas_id)
            .filter(MengajarModel.semester_id == sql_semester.id)
            .filter(MengajarModel.tahun_ajaran_id == sql_th_ajaran.id)
            .filter(MengajarModel.hari_id == HariModel.id)
            .filter(HariModel.hari == hari)
            .first()
        )

        if sql_mengajar:
            data = dic_data(
                siswa_id=sql_siswa.user_id,
                nisn=sql_user.username,
                first_name=sql_siswa.first_name.title(),
                last_name=sql_siswa.last_name.title(),
                gender=sql_siswa.gender,
                kelas=sql_siswa.kelas.kelas,
                picture=url_for(".static", filename=f"img/siswa/foto/{sql_siswa.pic}")
                if sql_siswa.pic
                else None,
                semester=sql_semester.semester.title(),
                today=today,
                kelas_id=sql_siswa.kelas_id,
                mengajar_id=sql_mengajar.id,
            )
            return (
                jsonify(status="success", data=data),
                HTTP_200_OK,
            )
        else:
            return jsonify(msg="Tidak ada jadwal hari ini"), HTTP_404_NOT_FOUND
    else:
        return jsonify(msg="QR Code tidak sah."), HTTP_404_NOT_FOUND


@guru.get("/jadwal-harian")
@jwt_required()
def get_jadwal_harian():
    guru_id = get_jwt_identity().get("id")
    hari = today_()
    sql_semester = SemesterModel.query.filter_by(is_active=1).first()
    sql_mengajar = (
        db.session.query(MengajarModel)
        .join(HariModel)
        .filter(MengajarModel.guru_id == guru_id)
        .filter(MengajarModel.hari_id == HariModel.id)
        .filter(MengajarModel.semester_id == sql_semester.id)
        .filter(HariModel.hari == hari)
        .all()
    )
    data = []
    today = format_date_today(datetime.today())
    if sql_mengajar:
        for i in sql_mengajar:
            data.append(
                {
                    "id": i.id,
                    "first_name": i.guru.first_name.title(),
                    "last_name": i.guru.last_name.title(),
                    "kode_mengajar": i.kode_mengajar,
                    "mapel": i.mapel.mapel.title(),
                    "jam_mulai": i.jam_mulai,
                    "jam_selesai": i.jam_selesai,
                    "semester": i.semester.semester.title(),
                    "kelas": i.kelas.kelas,
                    "hari": i.hari.hari.title(),
                    "today": today,
                }
            )

        return jsonify(data=data), HTTP_200_OK

    else:
        return jsonify(msg="Tidak ada jadwal mengajar."), HTTP_404_NOT_FOUND


@guru.get("/jadwal-hari")
@jwt_required()
def get_jadwal_by_hari():
    guru_id = get_jwt_identity().get("id")
    hari = request.args.get("hari")
    sql_semester = SemesterModel.query.filter_by(is_active=1).first()
    sql_mengajar = (
        db.session.query(MengajarModel)
        .join(HariModel)
        .filter(MengajarModel.hari_id == HariModel.id)
        .filter(HariModel.hari == hari)
        .filter(MengajarModel.guru_id == guru_id)
        .filter(MengajarModel.semester_id == sql_semester.id)
        .all()
    )

    data = []
    if sql_mengajar:
        for i in sql_mengajar:
            data.append(
                {
                    "id": i.id,
                    "first_name": i.guru.first_name.title(),
                    "last_name": i.guru.last_name.title(),
                    "kode_mengajar": i.kode_mengajar,
                    "mapel": i.mapel.mapel.title(),
                    "jam_mulai": i.jam_mulai,
                    "jam_selesai": i.jam_selesai,
                    "semester": i.semester.semester.title(),
                    "kelas": i.kelas.kelas,
                    "hari": i.hari.hari.title(),
                }
            )
        return jsonify(status="success", data=data), HTTP_200_OK

    else:
        return jsonify(status="fail", msg="Tidak ada jadwal."), HTTP_404_NOT_FOUND


@guru.get("/jadwal-sepekan")
@jwt_required()
def get_all_jadwal():
    guru_id = get_jwt_identity().get("id")
    sql_semester = SemesterModel.query.filter_by(is_active=1).first()
    sql_mengajar = (
        db.session.query(MengajarModel)
        .join(HariModel)
        .filter(MengajarModel.hari_id == HariModel.id)
        .filter(MengajarModel.guru_id == guru_id)
        .filter(MengajarModel.semester_id == sql_semester.id)
        .all()
    )
    # data = {}
    data = []
    if sql_mengajar:
        for i in sql_mengajar:
            data.append(
                {
                    "id": i.id,
                    "first_name": i.guru.first_name.title(),
                    "last_name": i.guru.last_name.title(),
                    "kode_mengajar": i.kode_mengajar,
                    "mapel": i.mapel.mapel.title(),
                    "jam_mulai": i.jam_mulai,
                    "jam_selesai": i.jam_selesai,
                    "semester": i.semester.semester.title(),
                    "kelas": i.kelas.kelas,
                    "hari": i.hari.hari.title(),
                }
            )
        # if i.hari.hari == "selasa":
        #     selasa.append(
        #         {
        #             "id": i.id,
        #             "first_name": i.guru.first_name.title(),
        #             "last_name": i.guru.last_name.title(),
        #             "kode_mengajar": i.kode_mengajar,
        #             "mapel": i.mapel.mapel.title(),
        #             "jam_mulai": i.jam_mulai,
        #             "jam_selesai": i.jam_selesai,
        #             "semester": i.semester.semester.title(),
        #             "kelas": i.kelas.kelas,
        #             "hari": i.hari.hari.title(),
        #         }
        #     )

        # data.update(senin=senin, selasa=selasa)
        return (
            jsonify(status="success", data=data),
            HTTP_200_OK,
        )

    else:
        return jsonify(status="fail", msg="Tidak ada jadwal."), HTTP_404_NOT_FOUND


@guru.get("daftar-kelas-ajar")
@jwt_required()
def get_kelas_ajar():
    ## * GET KELAS AJAR DENGAN NAMA WALI KELAS
    guru_login_id = get_jwt_identity().get("id")
    sql_mengajar = (
        db.session.query(MengajarModel)
        .filter(MengajarModel.guru_id == guru_login_id)
        .filter(MengajarModel.semester_id == SemesterModel.id)
        .filter(SemesterModel.is_active == "1")
        .order_by(MengajarModel.kelas_id.asc())
        .group_by(MengajarModel.kelas_id)
        .all()
    )

    data = []

    if sql_mengajar:
        for i in sql_mengajar:
            sql_wali = WaliKelasModel.query.filter_by(kelas_id=i.kelas_id).first()
            data.append(
                {
                    "kelas": i.kelas.kelas,
                    "kelas_id": i.kelas_id,
                    "mengajar_id": i.id,
                    "semester": i.semester.semester.upper(),
                    "wali_kelas": sql_wali.guru.first_name.title()
                    + " "
                    + sql_wali.guru.last_name.title(),
                }
            )

        return jsonify(status="success", data=data), HTTP_200_OK

    else:
        return jsonify(msg="Data tidak ada."), HTTP_404_NOT_FOUND


@guru.get("/siswa-kelas")
@jwt_required()
def get_siswa_kelas():
    kelas_id = request.args.get("kelas_id", None)
    sql_wali = (
        db.session.query(WaliKelasModel)
        .filter(WaliKelasModel.kelas_id == kelas_id)
        .first()
    )

    data = {}
    siswa = []
    if sql_wali:
        sql_siswa = db.session.query(SiswaModel).filter(
            SiswaModel.kelas_id == sql_wali.kelas_id
        )
        for i in sql_siswa:
            siswa.append(
                {
                    "siswa_id": i.user_id,
                    "first_name": i.first_name.title(),
                    "last_name": i.last_name.title(),
                    "kelas": i.kelas.kelas,
                    "kelas_id": i.kelas_id,
                }
            )

        data.update(
            siswa=siswa,
            wali_kelas=f"{sql_wali.guru.first_name.title()} {sql_wali.guru.last_name.title()}",
        )

        return (
            jsonify(status="success", data=data, jml_data=sql_siswa.count()),
            HTTP_200_OK,
        )

    else:
        return jsonify(msg="Data tidak ada."), HTTP_404_NOT_FOUND


@guru.route("/absen-siswa", methods=["GET", "POST"])
@jwt_required()
def absen_siswa_guru_mapel():
    mengajar_id = request.json.get("mengajar_id")
    siswa_id = request.json.get("siswa_id")
    tgl_absen = datetime.date(datetime.today())
    ket = request.json.get("keterangan")

    sql_pertemuan = (
        db.session.query(AbsensiModel)
        .filter(AbsensiModel.mengajar_id == mengajar_id)
        .filter(AbsensiModel.tgl_absen == datetime.date(datetime.today()))
        .filter(AbsensiModel.siswa_id == siswa_id)
        .count()
    )

    if request.method == "POST":
        pertemuan = 0
        if sql_pertemuan == 0:
            pertemuan += 1
        else:
            pertemuan = sql_pertemuan + 1
        if sql_pertemuan > 0:
            return jsonify(msg="Telah melakukan absensi hari ini."), HTTP_409_CONFLICT

        else:
            base = BaseModel(
                AbsensiModel(
                    mengajar_id=mengajar_id,
                    siswa_id=siswa_id,
                    tgl_absen=tgl_absen,
                    ket=ket,
                    pertemuanKe=pertemuan,
                )
            )
            base.create()

            return (
                jsonify(
                    status="success",
                    mengajar_id=mengajar_id,
                    siswa_id=siswa_id,
                    tgl_absen=str(tgl_absen),
                    keterangan=ket,
                ),
                HTTP_201_CREATED,
            )

    else:
        return jsonify(msg="Cek API Guru controller absen siswa guru mapel")


@guru.get("/check-password")
@jwt_required()
def check_password():
    user_id = get_jwt_identity().get("id")
    base = BaseModel(UserModel)

    sql_user = base.get_one(id=user_id)

    if not sql_user:
        return jsonify(msg="Data user tidak ditemukan."), HTTP_404_NOT_FOUND
    else:
        password = request.json.get("password")
        check_password = check_password_hash(sql_user.password, password)
        if check_password:
            return jsonify(msg="Kata sandi valid."), HTTP_200_OK
        else:
            return (
                jsonify(msg="Kata sandi tidak valid, silahkan periksa kembali!"),
                HTTP_403_FORBIDDEN,
            )


@guru.route("/update-password", methods=["GET", "PUT"])
@jwt_required()
def update_password():
    user_id = get_jwt_identity().get("id")
    base = BaseModel(UserModel)

    sql_user = base.get_one(id=user_id)

    if not sql_user:
        return jsonify(msg="Data user tidak ditemukan."), HTTP_404_NOT_FOUND
    else:
        password = request.json.get("password")
        if len(password) < 8:
            return (
                jsonify(msg="Panjang karakter minimal 8."),
                HTTP_400_BAD_REQUEST,
            )
        else:
            hash_pswd = generate_password_hash(password=password)
            sql_user.password = hash_pswd
            base.edit()
            return jsonify(msg="Kata sandi telah diperbaharui."), HTTP_200_OK


# @guru.get("/daftar-riwayat-absen")
# @jwt_required()
# def get_daftar_riwayat_absen():
#     guru_id = get_jwt_identity().get("id")
#     sql_mengajar = MengajarModel.query.filter_by(guru_id=guru_id).first()

#     arg = request.args.get("tgl_absen")

#     print(f"REQUEST ARGUMENT ==> {arg}")

#     sql_absen = (
#         db.session.query(AbsensiModel)
#         .filter(AbsensiModel.mengajar_id == sql_mengajar.id)
#         .order_by(AbsensiModel.tgl_absen.desc())
#     )

#     data = []

#     if sql_absen.all():
#         if arg is not None:
#             for i in sql_absen.filter(AbsensiModel.tgl_absen == arg).all():
#                 data.append(
#                     dic_data(
#                         id=i.id,
#                         nama_siswa=f"{i.siswa.first_name} {i.siswa.last_name}",
#                         kelas=i.siswa.kelas.kelas,
#                         mapel=i.mengajar.mapel.mapel,
#                         nama_guru=f"{i.mengajar.guru.first_name} {i.mengajar.guru.last_name}",
#                         tgl_absen=format_indo(i.tgl_absen),
#                         tgl_absens=f"{i.tgl_absen}",
#                     )
#                 )

#             return jsonify(status="sukses", data=data), HTTP_200_OK
#         else:
#             for i in sql_absen:
#                 data.append(
#                     dic_data(
#                         id=i.id,
#                         nama_siswa=f"{i.siswa.first_name} {i.siswa.last_name}",
#                         kelas=i.siswa.kelas.kelas,
#                         mapel=i.mengajar.mapel.mapel,
#                         nama_guru=f"{i.mengajar.guru.first_name} {i.mengajar.guru.last_name}",
#                         tgl_absen=format_indo(i.tgl_absen),
#                     )
#                 )

#                 print(i.tgl_absen)

#             return (
#                 jsonify(
#                     status="sukses",
#                     data=data,
#                 ),
#                 HTTP_200_OK,
#             )
#     else:
#         return jsonify(msg="Data tidak ada."), HTTP_404_NOT_FOUND


# @guru.route("/daftar-tanggal-absensi")
# @jwt_required()
# def daftar_tanggal_absensi():
#     guru_id = get_jwt_identity().get("id")
#     sql_mengajar = MengajarModel.query.filter_by(guru_id=guru_id).first()
#     sql_absen = (
#         db.session.query(AbsensiModel)
#         .filter(AbsensiModel.mengajar_id == sql_mengajar.id)
#         .order_by(AbsensiModel.tgl_absen.desc())
#         .group_by(AbsensiModel.tgl_absen)
#         .all()
#     )

#     data = []
#     if sql_absen:
#         for i in sql_absen:
#             data.append(
#                 dic_data(
#                     tgl_absens=f"{i.tgl_absen}", tgl_absen=format_indo(i.tgl_absen)
#                 )
#             )

#         return jsonify(status="sukses", data=data), HTTP_200_OK

#     else:
#         return jsonify(msg="Data tidak ada."), HTTP_404_NOT_FOUND


@guru.route("/daftar-riwayat")
@jwt_required()
def get_daftar_riwayat():
    guru_id = get_jwt_identity().get("id")
    sql_mengajar = MengajarModel.query.filter_by(guru_id=guru_id).first()
    # sql_absen_by_tgl = (
    #     db.session.query(AbsensiModel)
    #     .filter(AbsensiModel.mengajar_id == sql_mengajar.id)
    #     .order_by(AbsensiModel.tgl_absen.desc())
    #     .all()
    # )
    sql_absen = (
        db.session.query(AbsensiModel)
        .join(MengajarModel)
        .join(SemesterModel)
        .join(TahunAjaranModel)
        .join(SiswaModel)
        .filter(
            and_(
                MengajarModel.guru_id == guru_id,
                SemesterModel.is_active == "1",
                TahunAjaranModel.is_active == "1",
            )
        )
        .order_by(AbsensiModel.tgl_absen.desc())
        .order_by(SiswaModel.kelas_id.asc())
        .all()
    )
    group_data = {}
    group_data2 = {}

    for i in sql_absen:
        tanggal = f"{format_indo(i.tgl_absen)}"

        if tanggal in group_data:
            group_data[tanggal].append(i)
        else:
            group_data[tanggal] = [i]

    for tanggal, items in group_data.items():
        tanggal = tanggal
        for i in items:
            if tanggal in group_data2:
                group_data2[tanggal].append(
                    dic_data(
                        id=i.id,
                        nama_siswa=f"{i.siswa.first_name.title()} {i.siswa.last_name.title()}",
                        kelas=i.siswa.kelas.kelas,
                        ket="Hadir"
                        if i.ket == "H"
                        else "Sakit"
                        if i.ket == "S"
                        else "Izin"
                        if i.ket == "I"
                        else "Alpa",
                        mapel=i.mengajar.mapel.mapel,
                        nama_guru=f"{i.mengajar.guru.first_name} {i.mengajar.guru.last_name}",
                        tgl_absen=format_indo(i.tgl_absen),
                    )
                )
            else:
                group_data2[tanggal] = [
                    dic_data(
                        id=i.id,
                        nama_siswa=f"{i.siswa.first_name} {i.siswa.last_name}",
                        kelas=i.siswa.kelas.kelas,
                        ket="Hadir"
                        if i.ket == "H"
                        else "Sakit"
                        if i.ket == "S"
                        else "Izin"
                        if i.ket == "I"
                        else "Alpa",
                        mapel=i.mengajar.mapel.mapel,
                        nama_guru=f"{i.mengajar.guru.first_name} {i.mengajar.guru.last_name}",
                        tgl_absen=format_indo(i.tgl_absen),
                    )
                ]

    return jsonify(group_data2)
