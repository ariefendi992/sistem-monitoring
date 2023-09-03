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
from app.models.user_details_model import *
from app.site.forms.form_auth import FormLogin
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
            response = make_response(redirect(url_for("admin2.index")))
            return response
        elif current_user.group == "guru":
            response = make_response(redirect(url_for("guru2.index")))
            return response
        elif current_user.group == "bk":
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
                login_user(user=sql_user, remember=remember)

                if level == "admin" and current_user.group == "admin":
                    sql_admin = AdminModel.query.filter_by(user_id=sql_user.id).first()

                    session["first_name"] = sql_admin.first_name.upper()
                    session["last_name"] = sql_admin.last_name.upper()

                    sql_user.user_last_login = utc_makassar()

                    db.session.commit()

                    flash(
                        message=f"Login Sukses...\\nHi.. {sql_admin.first_name.title()} {sql_admin.last_name.title()} Selamat Datang Di Sistem E-Monitoring.",
                        category="success",
                    )
                    response = make_response(redirect(url_for("admin2.index")))
                    return response
                elif current_user.group == "guru" and level == "guru":
                    sql_guru = GuruModel.query.filter_by(user_id=sql_user.id).first()
                    session["first_name"] = sql_guru.first_name.upper()
                    session["last_name"] = sql_guru.last_name.upper()

                    sql_user.user_last_login = utc_makassar()

                    db.session.commit()
                    flash(
                        message=f"Login Sukses...\\nHi.. {sql_guru.first_name} {sql_guru.last_name} Selamat Datang Di Sistem E-Monitoring.",
                        category="success",
                    )
                    response = make_response(redirect(url_for("guru2.index")))
                    return response

                elif current_user.group == "bk" and level == "bk":
                    sql_guru = GuruModel.query.filter_by(user_id=sql_user.id).first()
                    session["first_name"] = sql_guru.first_name.upper()
                    session["last_name"] = sql_guru.last_name.upper()

                    sql_user.user_last_login = utc_makassar()
                    db.session.commit()

                    flash(
                        message=f"Login Sukses...\\nHi.. {sql_guru.first_name} {sql_guru.last_name} Selamat Datang Di Sistem E-Monitoring.",
                        category="success",
                    )
                    response = make_response(redirect(url_for("guru_bk.index")))
                    return response

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

    response = make_response(render_template("auth/login.html", form=form))
    session["next"] = request.args.get("next")

    return response


@auth2.route("sign-out")
@login_required
def logout():
    session.clear()
    logout_user()
    return redirect(url_for("auth2.index"))
