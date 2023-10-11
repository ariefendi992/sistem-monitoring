from flask import Blueprint, make_response, request, jsonify, current_app
from flask_jwt_extended import (
    get_jwt,
    get_jwt_identity,
    jwt_required,
    create_access_token,
    create_refresh_token,
)
from sqlalchemy import func
from app.extensions import jwt
from app.lib.base_model import BaseModel
from app.lib.date_time import format_datetime_id, format_indo, utc_makassar
from app.lib.db_statement import DBStatement
from app.models.master_model import KelasModel
from app.models.notifikasi_model import NotifikasiSiswaModel
from app.models.user_details_model import *
from app.models.user_model import StatusUserLogin, TokenBlockList, UserModel
from app.extensions import db
from app.lib.status_code import *
from werkzeug.security import generate_password_hash
from app.models.master_model import MengajarModel
from app.lib.date_time import *

dbs = DBStatement()

auth = Blueprint("auth", __name__, url_prefix="/api/v2/auth")


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlockList.id).filter_by(jti=jti).scalar()
    return token is not None


@auth.route(
    "/login",
    methods=["POST", "GET", "PUT"],
)
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    user = BaseModel(UserModel)
    sql_user = user.get_one_or_none(username=username)

    if not sql_user:
        return jsonify({"msg": "Username not found."}), HTTP_401_UNAUTHORIZED
    else:
        chk_pswd = UserModel.check_pswd(sql_user.password, password)
        jwt_refresh_token_exp = current_app.config["JWT_REFRESH_TOKEN_EXPIRES"]
        user_logged_in = BaseModel(StatusUserLogin(sql_user.id, True))

        if chk_pswd:
            """NOTE: LOGIN SISWA"""
            if sql_user.group == "siswa" and sql_user.is_active == "1":
                base_siswa = BaseModel(SiswaModel)
                sql_siswa = base_siswa.get_one_or_none(user_id=sql_user.id)
                user_identity = {
                    "id": sql_user.id,
                    "username": sql_user.username,
                    "first_name": sql_siswa.first_name,
                    "last_name": sql_siswa.last_name,
                }

                data = NotifikasiSiswaModel(sql_siswa.user_id, msg="Login Berhasil...")
                dbs.add_data(data)
                dbs.commit_data()

                access_token = create_access_token(identity=user_identity)
                refresh_token = create_refresh_token(identity=user_identity)
                sql_user.user_last_login = utc_makassar()
                user.edit()

                check_user_status_ = user_logged_in.get_one_or_none(
                    user_login_id=user_logged_in.model.user_login_id
                )

                if check_user_status_:
                    check_user_status_.status_login = True
                    user_logged_in.edit()
                else:
                    user_logged_in.create()

                return (
                    jsonify(
                        id=sql_user.id,
                        username=sql_user.username,
                        first_name=sql_siswa.first_name,
                        last_name=sql_siswa.last_name,
                        access_token=access_token,
                        refresh_token=refresh_token,
                        group=sql_user.group,
                        status_logged_in=user_logged_in.model.status_login,
                        jwt_refresh_token_exp=str(jwt_refresh_token_exp.seconds),
                    ),
                    HTTP_200_OK,
                )
            # NOTE : LOGIN GURU
            elif sql_user.group == "guru" and sql_user.is_active == "1":
                if MengajarModel.query.filter_by(guru_id=sql_user.id).first():
                    sql_user.user_last_login = utc_makassar()
                    base_guru = BaseModel(GuruModel)
                    sql_guru = base_guru.get_one_or_none(user_id=sql_user.id)
                    user_identity = {
                        "id": sql_user.id,
                        "username": sql_user.username,
                        "first_name": sql_guru.first_name,
                        "last_name": sql_guru.last_name,
                        "is_active": sql_user.is_active,
                        "group": sql_user.group,
                    }
                    access_token = create_access_token(identity=user_identity)
                    refresh_token = create_refresh_token(identity=user_identity)
                    user.edit()
                    return (
                        jsonify(
                            {
                                "id": sql_user.id,
                                "username": sql_user.username,
                                "first_name": sql_guru.first_name,
                                "last_name": sql_guru.last_name,
                                # "gender": sql_guru.gender,
                                # "alamat": sql_guru.alamat,
                                "access_token": access_token,
                                "refresh_token": refresh_token,
                                "group": sql_user.group,
                                "is_active": True
                                if sql_user.is_active == "1"
                                else False,
                                "jwt_refresh_token_exp": str(
                                    jwt_refresh_token_exp.seconds
                                ),
                                "status_logged_in": user_logged_in.model.status_login,
                            }
                        ),
                        HTTP_200_OK,
                    )
                else:
                    return (
                        jsonify(msg="Maaf username salah silahkan periksa kembali.!"),
                        HTTP_404_NOT_FOUND,
                    )
            elif sql_user.group == "admin" and sql_user.is_active == "1":
                sql_user.user_last_login = utc_makassar()
                base_admin = BaseModel(AdminModel)
                admin = base_admin.get_one_or_none(user_id=sql_user.id)
                user.edit()
                return (
                    jsonify(
                        id=admin.user_id,
                        username=admin.user.username,
                        group=admin.user.group,
                        first_name=admin.first_name,
                        last_name=admin.last_name,
                        # gender=admin.gender,
                        # alamat=admin.alamat,
                        is_active=True if sql_user.is_active == "1" else False,
                    ),
                    HTTP_200_OK,
                )
            else:
                return (
                    jsonify({"msg": "Akun smntr tidak dapat di akses"}),
                    HTTP_400_BAD_REQUEST,
                )
        else:
            return (
                jsonify(
                    {"msg": "Password not valid. Please check your password login."}
                ),
                HTTP_401_UNAUTHORIZED,
            )


@auth.route("/logout")
@jwt_required(verify_type=False)
def logout():
    jwt = get_jwt()
    jti = jwt["jti"]

    now = utc_makassar()
    id = get_jwt_identity()["id"]
    # db.session.add(TokenBlockList(jti=jti, created_at=now, user_id=id))
    # db.session.commit()

    # model = BaseModel(UserModel)
    # user = model.get_one_or_none(id=id)
    # user.user_logout = utc_makassar()
    # model.edit()

    # status_login_model = BaseModel(StatusUserLogin)
    # check_user_login = status_login_model.get_one_or_none(user_login_id=id)
    # if check_user_login:
    #     check_user_login.status_login = False
    #     status_login_model.edit()
    token_type = jwt["type"]
    token_b = TokenBlockList(jti, now, id)
    token_b.save()

    return (
        jsonify(
            msg=f"Token {token_type} revoked success",
            # status_login=check_user_login.status_login if check_user_login else None,
        ),
        HTTP_200_OK,
    )


@auth.route("/refresh-token", methods=["POST", "GET"])
@jwt_required(refresh=True)
def refresh_token():
    identity = get_jwt_identity()
    access_token = create_access_token(identity, fresh=False)
    refresh_token = create_refresh_token(identity)

    time_exp_token = current_app.config.get("JWT_ACCESS_TOKEN_EXPIRES")

    return (
        jsonify(
            access_token=access_token,
            refresh_token=refresh_token,
            jwt_refresh_token_exp=str(time_exp_token.seconds),
        ),
        HTTP_200_OK,
    )


@auth.route("/create", methods=["POST", "GET", "PUT"])
def create():
    username = request.json.get("username")
    password = request.json.get("password")
    group = request.json.get("group")

    hash_pswd = generate_password_hash(password=password)
    user = BaseModel(
        UserModel(
            username,
            hash_pswd,
            group,
        )
    )
    if group == "siswa" or group == "SISWA":
        first_name = request.json.get("first_name")
        last_name = request.json.get("last_name")
        gender = request.json.get("gender")
        tempat_lahir = request.json.get("tempat_lahir")
        tgl_lahir = request.json.get("tanggal_lahir")
        agama = request.json.get("agama")
        nama_ortu = request.json.get("nama_ortu")
        telp = request.json.get("telp")
        alamat = request.json.get("alamat")
        pic = request.json.get("")
        kelas = request.json.get("kelas_id")

        usrnm = BaseModel(UserModel)
        check_username = usrnm.get_one(username=username)

        if check_username is not None:
            return jsonify(msg=f"Username is already exists"), HTTP_409_CONFLICT
        else:
            user.create()
            siswa = BaseModel(
                SiswaModel(
                    first_name=first_name,
                    last_name=last_name,
                    gender=gender,
                    tempat_lahir=tempat_lahir,
                    tgl_lahir=tgl_lahir,
                    agama=agama,
                    nama_ortu=nama_ortu,
                    telp=telp,
                    alamat=alamat,
                    user_id=user.model.id,
                    kelas=kelas,
                )
            )
            baseKelas = BaseModel(KelasModel)
            kelasModel = baseKelas.get_one(id=kelas)
            siswa.create()

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

            if siswa.model.gender == "laki-laki":
                kelasModel.jml_laki = countSiswaGender
                kelasModel.jml_perempuan = countSiswaPerempuan
            elif siswa.model.gender == "perempuan":
                kelasModel.jml_laki = countSiswaLaki
                kelasModel.jml_perempuan = countSiswaGender

            kelasModel.jml_seluruh = countSiswaAll
            baseKelas.edit()

            return (
                jsonify(
                    msg=f"Data Siswa {siswa.model.first_name} telah berhasil di tambahkan"
                ),
                HTTP_201_CREATED,
            )

    elif group == "guru":
        first_name = request.json.get("first_name")
        last_name = request.json.get("last_name")
        gender = request.json.get("gender")
        alamat = request.json.get("alamat")
        agama = request.json.get("agama")
        telp = request.json.get("telp")

        usrnm = BaseModel(UserModel)
        check_username = usrnm.get_one(username=username)

        if check_username is not None:
            return jsonify(msg="Username is already exists"), HTTP_409_CONFLICT
        else:
            user.create()
            guru = BaseModel(
                GuruModel(
                    first_name=first_name,
                    last_name=last_name,
                    gender=gender,
                    alamat=alamat,
                    agama=agama,
                    user_id=user.model.id,
                    telp=telp,
                )
            )
            guru.create()
            return (
                jsonify(
                    msg=f"Data Guru : {guru.model.first_name} telah berhasil di tambahkan."
                ),
                HTTP_201_CREATED,
            )

    elif group == "admin":
        first_name = request.json.get("first_name")
        last_name = request.json.get("last_name")
        gender = request.json.get("gender")
        alamat = request.json.get("alamat")

        usrnm = BaseModel(UserModel)
        check_username = usrnm.get_one(username=username)

        if check_username is not None:
            return jsonify({"msg": "Username is already exists"}), HTTP_409_CONFLICT
        else:
            user.create()
            user_detail = BaseModel(
                AdminModel(first_name, last_name, gender, alamat, user.model.id)
            )
            user_detail.create()
            return (
                jsonify(
                    msg=f"Data Admin : {user_detail.model.first_name} telah berhasil di tambahkan."
                ),
                HTTP_201_CREATED,
            )


@auth.route("/get-one")
@jwt_required()
def get_one():
    current_user = get_jwt_identity()
    user_id = current_user.get("id")
    # jjwt = get_jwt()['exp']
    if current_user.get("group") == "siswa":
        model = BaseModel(SiswaModel)
        user = model.get_one_or_none(user_id=user_id)
        json_object = {
            "id": user_id,
            "first_name": current_user.get("first_name"),
            "last_name": current_user.get("last_name"),
            "kelas": current_user.get("kelas"),
            "group": current_user.get("group"),
            "is_active": current_user.get("is_active"),
            "gender": user.gender.title(),
        }
        return jsonify(json_object), HTTP_200_OK
    elif current_user.get("group") == "guru":
        model = BaseModel(GuruModel)
        user = model.get_one_or_none(user_id=user_id)
        return (
            jsonify(
                {
                    "id": user_id,
                    "first_name": current_user.get("first_name"),
                    "last_name": current_user.get("last_name"),
                    "group": current_user.get("group"),
                    "is_active": current_user.get("is_active"),
                    "gender": user.gender.title(),
                }
            ),
            HTTP_200_OK,
        )
    elif current_user.get("group") == "admin":
        model = BaseModel(AdminModel)
        user = model.get_one_or_none(user_id=user_id)
        return (
            jsonify(
                {
                    "id": user_id,
                    "first_name": current_user.get("first_name"),
                    "last_name": current_user.get("last_name"),
                    "group": current_user.get("group"),
                    "is_active": current_user.get("is_active"),
                    "gender": user.gender,
                }
            ),
            HTTP_200_OK,
        )


@auth.route("/get-single/<int:id>")
def get_single(id):
    # current_user = get_jwt_identity()
    base = BaseModel(UserModel)
    user = base.get_one_or_none(id=id)
    # jjwt = get_jwt()['exp']
    if user.group == "admin":
        model = BaseModel(AdminModel)
        user = model.get_one_or_none(user_id=user.id)
        print(user.first_name)
        return (
            jsonify(
                {
                    "id": user.user_id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "group": user.user.group,
                    "is_active": user.user.is_active,
                    "gender": user.gender,
                }
            ),
            HTTP_200_OK,
        )


@auth.route("/get-all")
def get_all():
    model = BaseModel(UserModel)
    data = []
    for user in model.get_all():
        if user.group == "siswa" or user.group == "guru":
            data.append(
                {
                    "id": user.id,
                    "username": user.username,
                    "group": user.group,
                    "join": format_indo(user.join_date),
                    "last_update": format_datetime_id(user.update_date)
                    if user.update_date
                    else "-",
                    "last_login": format_datetime_id(user.user_last_login)
                    if user.user_last_login
                    else "-",
                    "is_active": user.is_active,
                }
            )
    return jsonify(data), HTTP_200_OK


@auth.route("/edit-status", methods=["PUT"])
def edit_status():
    base = BaseModel(UserModel)
    id = request.args.get("id")
    model = base.get_one_or_none(id=id)

    status = request.json.get("status")
    model.is_active = status
    model.update_date = utc_makassar()

    base.edit()

    return jsonify(msg="Upadated Success."), HTTP_200_OK


@auth.put("/edit-password")
def edit_password():
    base = BaseModel(UserModel)
    id = request.args.get("id")
    model = base.get_one_or_none(id=id)
    password = request.json.get("password")

    if not model:
        return jsonify(msg="User not found."), HTTP_404_NOT_FOUND
    elif len(password) < 6:
        return jsonify(msg="Password minimal 6 karakter"), HTTP_400_BAD_REQUEST
    else:
        hash_pswd = generate_password_hash(password=password)
        model.password = hash_pswd
        model.update_date = utc_makassar()
        base.edit()
        return jsonify(msg="Upadated Password Succsess."), HTTP_200_OK


@auth.route("/status-logged-in/<user_id>", methods=["GET", "PUT"])
def status_user_login(user_id: int):
    base_model = BaseModel(StatusUserLogin)
    # id = get_jwt_identity()["id"]
    user_login = base_model.get_one_or_none(user_login_id=user_id)

    if user_login:
        if request.method == "GET":
            return (
                jsonify(
                    id=user_login.id,
                    username=user_login.user_login.username,
                    user_id=user_login.user_login_id,
                    status_logged_in=user_login.status_login,
                ),
                HTTP_200_OK,
            )
        elif request.method == "PUT":
            user_login.status_login = request.json.get("status_logged_in")
            base_model.update()
        else:
            return jsonify(msg="Request method salah!")

    return jsonify(msg="Data tidak ditemukan!"), HTTP_404_NOT_FOUND
