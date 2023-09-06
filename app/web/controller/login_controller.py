import json
import os
from flask import (
    Blueprint,
    flash,
    request,
    redirect,
    render_template,
    url_for,
    session,
    make_response,
)
from app.api.controller.master_controller import WaliKelas
from app.models.master_model import WaliKelasModel
from app.models.user_details_model import *
from app.web.forms.form_auth import FormLogin
from flask_login import login_user, current_user, login_required, logout_user
from urllib.parse import urljoin, urlparse
from app.models.user_model import *
from app.lib.date_time import utc_makassar
from app.extensions import db

auth2 = Blueprint("auth2", __name__, url_prefix="/", template_folder="../templates/")

JSON_FILE = os.getcwd() + "/data.json"


def write_json(data, filename=JSON_FILE):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc


@auth2.get("/")
def index():
    if current_user.is_authenticated:
        if current_user.group == "admin":
            if "next" in session and session["next"]:
                if is_safe_url(session["next"]):
                    return redirect(session["next"])
            else:
                response = make_response(redirect(url_for("admin2.index")))
                return response
        elif current_user.group == "guru":
            if "next" in session and session["next"]:
                if is_safe_url(session["next"]):
                    return redirect(session["next"])
            else:
                response = make_response(redirect(url_for("guru2.index")))
                return response
        elif current_user.group == "bk":
            if "next" in session and session["next"]:
                if is_safe_url(session["next"]):
                    return redirect(session["next"])
            else:
                response = make_response(redirect(url_for("guru_bk.index")))
                return response

    return redirect(url_for("auth2.login"))


@auth2.route("/login", methods=["GET", "POST"])
def login():
    form = FormLogin()
    if request.method == "POST" and form.validate_on_submit():
        username = request.form.get("username")
        password = request.form.get("password")
        level = request.form.get("level")
        remember = request.form.get("remember")
        sql_user = UserModel.query.filter_by(username=username).first()

        if not sql_user:
            flash(
                message="Username yang di input salah.! silahkan periksa kembali.",
                category="error",
            )
        else:
            sql_check_password = UserModel.check_pswd(sql_user.password, password)
            if sql_check_password:
                if (
                    level == "admin"
                    and sql_user.group == "admin"
                    and sql_user.is_active == "1"
                ):
                    login_user(user=sql_user, remember=remember)
                    sql_admin = AdminModel.query.filter_by(
                        user_id=current_user.id
                    ).first()

                    session["first_name"] = sql_admin.first_name.upper()
                    session["last_name"] = sql_admin.last_name.upper()

                    sql_user.user_last_login = utc_makassar()

                    db.session.commit()

                    flash(
                        message=f"Login Sukses...\\nHi.. {sql_admin.first_name.title()} {sql_admin.last_name.title()} Selamat Datang Di Sistem Monitoring Siswa.",
                        category="success",
                    )

                    if "next" in session and session["next"]:
                        if is_safe_url(session["next"]):
                            return redirect(session["next"])
                    else:
                        response = make_response(redirect(url_for("admin2.index")))
                        return response
                elif (
                    sql_user.group == "guru"
                    and level == "guru"
                    and sql_user.is_active == "1"
                ):
                    login_user(user=sql_user, remember=remember)
                    sql_guru = GuruModel.query.filter_by(
                        user_id=current_user.id
                    ).first()
                    session["first_name"] = sql_guru.first_name.upper()
                    session["last_name"] = sql_guru.last_name.upper()

                    sql_user.user_last_login = utc_makassar()

                    db.session.commit()

                    flash(
                        message=f"Login Sukses...\\nHi.. {sql_guru.first_name} {sql_guru.last_name} Selamat Datang Di Sistem E-Monitoring.",
                        category="success",
                    )

                    if "next" in session and session["next"]:
                        if is_safe_url(session["next"]):
                            return redirect(session["next"])
                    else:
                        response = make_response(redirect(url_for("guru2.index")))
                        return response

                elif (
                    sql_user.group == "bk"
                    and level == "bk"
                    and sql_user.is_active == "1"
                ):
                    login_user(user=sql_user, remember=remember)
                    sql_guru = GuruModel.query.filter_by(
                        user_id=current_user.id
                    ).first()
                    session["first_name"] = sql_guru.first_name.upper()
                    session["last_name"] = sql_guru.last_name.upper()

                    sql_user.user_last_login = utc_makassar()
                    db.session.commit()

                    flash(
                        message=f"Login Sukses...\\nHi.. {sql_guru.first_name} {sql_guru.last_name} Selamat Datang Di Sistem Monitoring Siswa.",
                        category="success",
                    )

                    if "next" in session and session["next"]:
                        if is_safe_url(session["next"]):
                            return redirect(session["next"])
                    else:
                        response = make_response(redirect(url_for("guru_bk.index")))
                        return response

                else:
                    if sql_user.is_active == "0":
                        flash(
                            "Ma'af..!\\nUntuk sementara waktu hak akses anda sendang di tangguhkan.",
                            "error",
                        )

                    else:
                        flash(
                            f"Ma'af..! Login Gagal.\\nSilahkan Periksa Kembali Username Dan Level Pengguna Anda.",
                            "error",
                        )

            else:
                flash(
                    message=f"Ma'af...!\\nKata sandi salah. Periksa kembali kata sandi.",
                    category="error",
                )

    session["next"] = request.args.get("next")
    print(session["next"])
    response = make_response(render_template("auth/login.html", form=form))

    return response


@auth2.route("sign-out")
@login_required
def logout():
    session.clear()
    logout_user()
    return redirect(url_for("auth2.index"))
