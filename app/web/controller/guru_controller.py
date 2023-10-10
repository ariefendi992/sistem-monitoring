from calendar import c
from re import I
from flask import (
    abort,
    make_response,
    request,
    Blueprint,
    redirect,
    session,
    url_for,
    flash,
    render_template,
)
from flask_login import current_user, login_required
from sqlalchemy import and_, func
from app.web.forms.form_absen import AbsensiForm
from app.web.forms.form_letter_report import FormSelectKehadiranSiswa
from ...extensions import db
from app.lib.base_model import BaseModel
from app.models.user_details_model import GuruModel, SiswaModel
from app.web.forms.form_guru import FormGetProfileGuru, FormUpdatePassword
from ...models.user_login_model import *
from ...models.master_model import (
    KelasModel,
    KepsekModel,
    MengajarModel,
    HariModel,
    NamaBulanModel,
    SemesterModel,
    TahunAjaranModel,
    WaliKelasModel,
)
from app.lib.date_time import tomorrow_, today_
from werkzeug.security import generate_password_hash, check_password_hash
from ...models.data_model import AbsensiModel
from datetime import datetime
from sqlalchemy import exists
from app.lib.db_statement import DBStatement

dbs = DBStatement()


guru2 = Blueprint(
    "guru2",
    __name__,
    url_prefix="/guru-site",
    static_folder="../static/",
    template_folder="../templates/",
)

day = lambda sql: sql
query = lambda sql: sql


def get_kelas_today():
    sql = day(
        sql=(
            db.session.query(MengajarModel)
            .join(HariModel)
            .join(SemesterModel)
            .filter(MengajarModel.guru_id == current_user.id)
            .filter(MengajarModel.hari_id == HariModel.id)
            .filter(HariModel.hari == today_())
            .filter(SemesterModel.is_active == 1)
            .order_by(MengajarModel.jam_mulai)
            .all()
        )
    )
    return sql


def get_kelas_tomorrow():
    sql = (
        db.session.query(MengajarModel)
        .join(HariModel)
        .filter(MengajarModel.guru_id == current_user.id)
        .filter(MengajarModel.hari_id == HariModel.id)
        .filter(HariModel.hari == tomorrow_())
        .all()
    )
    return sql


def check_wali():
    sql = query(
        sql=db.session.query(WaliKelasModel)
        .filter(WaliKelasModel.guru_id == current_user.id)
        .first()
    )
    return sql


@guru2.route("/")
@login_required
def index():
    if current_user.group == "guru" and session["tipe_akun"] == "guru_mapel":
        sqlToday = day(
            sql=(
                db.session.query(MengajarModel)
                .join(HariModel)
                .join(SemesterModel)
                .filter(MengajarModel.guru_id == current_user.id)
                .filter(MengajarModel.hari_id == HariModel.id)
                .filter(HariModel.hari == today_())
                .filter(SemesterModel.is_active == "1")
                .order_by(MengajarModel.jam_mulai)
                .all()
            )
        )
        baseJadwal = BaseModel(MengajarModel)
        mengajar = baseJadwal.get_all_filter_by(
            baseJadwal.model.hari_id.asc(), guru_id=current_user.id
        )
        wali_kelas = check_wali()

        get_one_semester = SemesterModel.query.filter_by(is_active="1").first()
        get_one_tahun_ajaran = TahunAjaranModel.query.filter_by(is_active="1").first()

        count_kelas_ajar = MengajarModel.query.filter_by(
            guru_id=current_user.id,
            semester_id=get_one_semester.id,
            tahun_ajaran_id=get_one_tahun_ajaran.id,
        ).count()

        count_ajar_today = (
            MengajarModel.query.filter_by(
                guru_id=current_user.id,
                semester_id=get_one_semester.id,
                tahun_ajaran_id=get_one_tahun_ajaran.id,
            )
            .join(HariModel)
            .filter_by(hari=today_())
            .count()
        )
        count_ajar_besok = (
            MengajarModel.query.filter_by(
                guru_id=current_user.id,
                semester_id=get_one_semester.id,
                tahun_ajaran_id=get_one_tahun_ajaran.id,
            )
            .join(HariModel)
            .filter_by(hari=tomorrow_())
            .count()
        )

        user = dbs.get_one(GuruModel, user_id=current_user.id)
        session.update(
            first_name=user.first_name.title(), last_name=user.last_name.title()
        )

        return render_template(
            "guru/index_guru.html",
            sqlJadwal=mengajar,
            sqlToday=sqlToday,
            wali_kelas=wali_kelas,
            count_kelas=count_kelas_ajar,
            count_today=count_ajar_today,
            count_besok=count_ajar_besok,
        )
    else:
        abort(401)


@guru2.route("/profile")
@login_required
def profile_guru():
    if current_user.group == "guru" and session["tipe_akun"] == "guru_mapel":
        baseJadwal = BaseModel(MengajarModel)
        mengajar = baseJadwal.get_all_filter_by(
            baseJadwal.model.hari_id.asc(), guru_id=current_user.id
        )
        base = BaseModel(GuruModel)
        guru = base.get_one(user_id=current_user.id)
        form = FormGetProfileGuru()
        form.nip.data = guru.user.username
        form.fullname.data = guru.first_name.title() + " " + guru.last_name.title()
        form.gender.data = guru.gender
        form.agama.data = guru.agama
        form.alamat.data = guru.alamat.title()
        form.telp.data = guru.telp
        sqlToday = get_kelas_today()

        user = dbs.get_one(GuruModel, user_id=current_user.id)
        session.update(
            first_name=user.first_name.title(), last_name=user.last_name.title()
        )
        return render_template(
            "akun/profile_guru.html",
            sql=guru,
            form=form,
            sqlJadwal=mengajar,
            sqlToday=sqlToday,
            wali_kelas=check_wali(),
        )
    else:
        abort(401)


@guru2.route("/profile/<int:id>", methods=["GET", "POST"])
@login_required
def update_profile(id):
    if current_user.group == "guru" and session["tipe_akun"] == "guru_mapel":
        base = BaseModel(GuruModel)
        guru = base.get_one(user_id=id)
        form = FormGetProfileGuru(request.form)
        nip = form.nip.data
        fullname = form.fullname.data
        gender = form.gender.data
        agama = form.agama.data
        alamat = form.alamat.data
        telp = form.telp.data
        first_name = ""
        last_name = ""
        first_name, *last_name = fullname.split()
        if len(last_name) == 0:
            last_name = first_name
        elif len(last_name) != 0:
            last_name = " ".join(last_name)
        guru.user.username = nip
        guru.first_name = first_name
        guru.last_name = last_name
        guru.gender = gender
        guru.agama = agama
        guru.alamat = alamat
        guru.telp = telp

        base.edit()

        user = dbs.get_one(GuruModel, user_id=current_user.id)
        session.update(
            first_name=user.first_name.title(), last_name=user.last_name.title()
        )
        flash(f"Data profil anda terlah diperbaharui.", "info")
        return redirect(url_for("guru2.profile_guru"))

    else:
        return abort(401)


@guru2.route("update-password", methods=["POST", "GET", "PUT"])
@login_required
def update_pswd():
    if current_user.group == "guru" and session["tipe_akun"] == "guru_mapel":
        base = BaseModel(GuruModel)
        guru = base.get_one(user_id=current_user.id)
        form = FormUpdatePassword()
        if form.validate_on_submit() and request.method == "POST":
            password = request.form.get("password")
            check_pswd = check_password_hash(guru.user.password, password)
            if check_pswd:
                flash(
                    f"Pastikan password baru anda tidak boleh sama dengan password sebelumnya.!",
                    "error",
                )
            else:
                pswd_hash = generate_password_hash(password)
                guru.user.password = pswd_hash
                base.edit()
                flash(f"Password akun anda telah berhasil di perbaharui.!", "info")

                return redirect(url_for("guru2.index"))

        user = dbs.get_one(GuruModel, user_id=current_user.id)
        session.update(
            first_name=user.first_name.title(), last_name=user.last_name.title()
        )
        return render_template(
            "akun/update_password.html", form=form, wali_kelas=check_wali()
        )
    else:
        return abort(401)


@guru2.route("jadwal-mengajar")
@login_required
def jadwal_mengajar():
    if current_user.group == "guru" and session["tipe_akun"] == "guru_mapel":
        # mengajar = base.get_all_filter_by(
        #     base.model.hari_id.asc(), guru_id=current_user.id
        # )
        sql_mengajar = (
            db.session.query(MengajarModel)
            .join(SemesterModel)
            .filter(SemesterModel.is_active == 1)
            .filter(MengajarModel.guru_id == current_user.id)
            # .order_by(MengajarModel.hari_id.asc())
            # .order_by(MengajarModel.jam_mulai.asc())
            # .all()
        )
        """GET WITH GENERAL FUNCTION"""
        # sqlToday = get_kelas_today()
        # sqlTomorrow = get_kelas_tomorrow()

        """GET WITH LAMBDA FUNCTION"""
        sqlToday = day(
            sql=(
                db.session.query(MengajarModel)
                .join(HariModel)
                .join(SemesterModel)
                .filter(MengajarModel.guru_id == current_user.id)
                .filter(MengajarModel.hari_id == HariModel.id)
                .filter(HariModel.hari == today_())
                .filter(SemesterModel.is_active == 1)
                .order_by(MengajarModel.jam_mulai)
                .all()
            )
        )
        sqlTomorrow = day(
            sql=(
                db.session.query(MengajarModel)
                .join(HariModel)
                .join(SemesterModel)
                .filter(MengajarModel.guru_id == current_user.id)
                .filter(MengajarModel.hari_id == HariModel.id)
                .filter(HariModel.hari == tomorrow_())
                .filter(SemesterModel.is_active == 1)
                .all()
            )
        )

        sql_hari = (
            db.session.query(MengajarModel)
            .join(SemesterModel)
            .filter(SemesterModel.is_active == "1")
            .filter(MengajarModel.guru_id == current_user.id)
            .group_by(MengajarModel.hari_id)
            .order_by(MengajarModel.hari_id.asc())
        )

        user = dbs.get_one(GuruModel, user_id=current_user.id)
        session.update(
            first_name=user.first_name.title(), last_name=user.last_name.title()
        )

        return render_template(
            "guru/modul/jadwal_mengajar/jadwal_mengajar.html",
            # sqlJadwal=mengajar,
            sqlJadwal=sql_mengajar,
            sqlToday=sqlToday,
            sqlTomorrow=sqlTomorrow,
            wali_kelas=check_wali(),
            sqlHari=sql_hari,
            MM=MengajarModel,
        )
    else:
        return abort(401)


@guru2.route("/absensi-pelajaran/<int:mengajar_id>", methods=["GET", "POST"])
@login_required
def absensi(mengajar_id):
    if current_user.group == "guru" and session["tipe_akun"] == "guru_mapel":
        form = AbsensiForm()
        """
            mengambil smua data pada tabel master mengajar dengan filter by mengajar id
            sebagai parameter, dan menyimpan data mengajar pada dictionary data mengajar
        """
        base_mengajar = BaseModel(MengajarModel)
        mengajar = base_mengajar.get_all_filter_by(id=mengajar_id)

        # pertemuan = 0
        # if sql_pertemuan == 0:
        #     pertemuan += 1
        # else:
        #     pertemuan = sql_pertemuan + 1

        data_mengajar = {}
        for i in mengajar:
            data_mengajar["kelas_id"] = i.kelas_id
            data_mengajar["kelas"] = i.kelas.kelas
            data_mengajar["mengajar_id"] = i.id
            data_mengajar["mapel_id"] = i.mapel_id
            data_mengajar["mapel"] = i.mapel.mapel

        """
            mengambil semua data siswa dengan filter kelas id pada tabel siswa
            dan di join dengan kelas id pada tabel master mengajar. Dan data
        """
        # base_siswa = BaseModel(SiswaModel)
        # siswa = base_siswa.get_all_filter_by(kelas_id=data_mengajar["kelas_id"])
        siswa = (
            db.session.query(SiswaModel)
            # .join(AbsensiModel)
            # .filter(AbsensiModel.tgl_absen == AbsensiModel.tgl_absen)
            .filter(SiswaModel.kelas_id == data_mengajar["kelas_id"])
            .filter(
                ~exists(AbsensiModel.siswa_id)
                .where(SiswaModel.user_id == AbsensiModel.siswa_id)
                .where(AbsensiModel.tgl_absen == datetime.date(datetime.today()))
                .where(AbsensiModel.mengajar_id == mengajar_id)
            )
            .all()
        )

        sql_pertemuan = (
            db.session.query(AbsensiModel)
            .join(MengajarModel)
            .filter(
                and_(
                    # AbsensiModel.mengajar_id==mengajar_id,
                    # MengajarModel.guru_id == current_user.id,
                    AbsensiModel.siswa_id
                    == [
                        i.user_id
                        for i in SiswaModel.query.filter_by(
                            kelas_id=data_mengajar["kelas_id"]
                        ).all()
                    ][0],
                    MengajarModel.mapel_id == data_mengajar["mapel_id"],
                )
            )
            .count()
        )

        data_mengajar.update(
            count_pertemuan=sql_pertemuan + 1 if sql_pertemuan != 0 else 1
        )

        """
            mengambil semua id dan nama kelas pada tabel kelas melalui tabel siswa
            yang sudah di relasikan dengan tabel kelas, lalu di simpan dalam
            variabel dictionoary data.
        """
        data = {}
        for i in siswa:
            data["kelas_id"] = i.kelas_id
            data["kelas"] = i.kelas.kelas

        """
            Mengambil semua data pada Tabel Mengajar
            dengan filter berdasarkan hari dan guru id
        """
        sqlToday = day(
            sql=(
                db.session.query(MengajarModel)
                .join(HariModel)
                .join(SemesterModel)
                .filter(MengajarModel.guru_id == current_user.id)
                .filter(MengajarModel.hari_id == HariModel.id)
                .filter(HariModel.hari == today_())
                .filter(SemesterModel.is_active == 1)
                .order_by(MengajarModel.jam_mulai)
                .all()
            )
        )
        date = datetime.date(datetime.today())

        # """
        #     MENAMBIL DATA ABSEN PERHARI DENGAN FILTER BERDASARKAN TANGGAL PERHARI
        #     UNTUK FILTER PERTEMUAN-KE N JIKA TANGGALNYA MASIH SAMA ATAU DI HARI YANG
        #     SAMA PADA ABSEN MAKA PERTEMUAN KE TIDAK AKAN BERUBAH
        # """
        # sqlTglAbsen = day(
        #     sql=db.session.query(AbsensiModel)
        #     .join(SiswaModel)
        #     .filter(AbsensiModel.tgl_absen == date)
        #     .filter(AbsensiModel.siswa_id == SiswaModel.user_id)
        #     .first()
        # )

        """
            MENGHITUNG PERTEMUAN SETIAP SUDAH MELAKUKAN ABSEN, DAN HASIL
            KALKULASI DARI PERTEMUAN AKAN TER-TAMBAH SECARA OTOMATIS
            ZDI PERTEMUAN SELANJUTNYA
        """

        absen = []

        if request.method == "POST":
            for n in range(1, len(siswa) + 1):
                siswa_id = request.form.get(f"userId-{n}")
                mengajar_id = request.form.get(f"mengajarId")
                tgl_absen = request.form["today"]

                ket = request.form.get(f"ket-{n}")

                count_pertemuan = (
                    db.session.query(AbsensiModel)
                    .join(MengajarModel)
                    .filter(AbsensiModel.siswa_id == siswa_id)
                    .filter(MengajarModel.mapel_id == data_mengajar["mapel_id"])
                    .count()
                )
                if count_pertemuan == 0:
                    pertemuan = 1
                else:
                    pertemuan = count_pertemuan + 1

                absen.append(ket)
                base_absesn = BaseModel(
                    AbsensiModel(
                        mengajar_id=mengajar_id,
                        siswa_id=siswa_id,
                        tgl_absen=tgl_absen,
                        ket=ket,
                        pertemuanKe=pertemuan,
                    )
                )

                if None in absen:
                    pass
                else:
                    sqlPertemuan = day(
                        sql=db.session.query(AbsensiModel)
                        .filter(AbsensiModel.mengajar_id == mengajar_id)
                        .filter(
                            AbsensiModel.tgl_absen == datetime.date(datetime.today())
                        )
                        .filter(AbsensiModel.siswa_id == siswa_id)
                        .count()
                    )
                    if sqlPertemuan > 0:
                        flash(
                            "Ma'af.! Absen kehadiran hari ini telah di input", "error"
                        )
                    else:
                        base_absesn.create()
                        flash(
                            f"Kelas : {data.get('kelas')} telah selesai melaukan absen kehadiran. untuk mengubah kehadiran",
                            "success",
                        )
            return redirect(
                url_for("guru2.data_kehadiran", mengajar=data_mengajar["mengajar_id"])
            )

        user = dbs.get_one(GuruModel, user_id=current_user.id)
        session.update(
            first_name=user.first_name.title(), last_name=user.last_name.title()
        )
        return render_template(
            "guru/modul/absen/absensi.html",
            model=siswa,
            sqlToday=sqlToday,
            data=data,
            form=form,
            today=date,
            data_mengajar=data_mengajar,
            wali_kelas=check_wali(),
        )
    else:
        return abort(401)


@guru2.route("update-absensi/<int:mengajar_id>", methods=["GET", "POST"])
@login_required
def update_absen(mengajar_id):
    if current_user.group == "guru" and session["tipe_akun"] == "guru_mapel":
        data = {}
        """
        Mengambil semua data pada Tabel Mengajar
        dengan filter berdasarkan hari dan guru id
        """
        sqlToday = day(
            sql=(
                db.session.query(MengajarModel)
                .join(HariModel)
                .join(SemesterModel)
                .filter(MengajarModel.guru_id == current_user.id)
                .filter(MengajarModel.hari_id == HariModel.id)
                .filter(HariModel.hari == today_())
                .filter(SemesterModel.is_active == "1")
                .order_by(MengajarModel.jam_mulai)
                .all()
            )
        )

        base_mengjar = BaseModel(MengajarModel)
        sql_mengajar = base_mengjar.get_all_filter_by(id=mengajar_id)
        for i in sql_mengajar:
            data["mengajar_id"] = i.id
            data["kelas_id"] = i.kelas_id
            data["kelas"] = i.kelas.kelas
            data["mapel"] = i.mapel.mapel

        base_siswa = BaseModel(SiswaModel)
        sql_siswa = base_siswa.get_all_filter_by(kelas_id=data["kelas_id"])

        base_absensi = BaseModel(AbsensiModel)
        sql_absensi = base_absensi.get_all_filter_by(mengajar_id=mengajar_id)

        if request.method == "POST":
            for i in range(1, len(sql_absensi) + 1):
                ket = request.form.get(f"ket-{i}")
                siswa_id = request.form.get(f"siswaID-{i}")

                sql_update_absen = (
                    db.session.query(AbsensiModel)
                    .filter(AbsensiModel.mengajar_id == mengajar_id)
                    .filter(AbsensiModel.siswa_id == siswa_id)
                    .scalar()
                )

                sql_update_absen.ket = ket

                db.session.commit()

            flash(f"Anda telah melakukan perubahan absensi siswa.", "info")

            return redirect(url_for("guru2.absensi", mengajar_id=mengajar_id))

        user = dbs.get_one(GuruModel, user_id=current_user.id)
        session.update(
            first_name=user.first_name.title(), last_name=user.last_name.title()
        )

        return render_template(
            "guru/modul/absen/update_absensi.html",
            sqlToday=sqlToday,
            sql_absensi=sql_absensi,
            data=data,
            sql_siswa=sql_siswa,
            wali_kelas=check_wali(),
        )
    else:
        return abort(401)


@guru2.route("/daftar-hadir", methods=["GET", "POST"])
@login_required
def daftar_kehadiran():
    if current_user.group == "guru" and session["tipe_akun"] == "guru_mapel":
        form = FormSelectKehadiranSiswa()
        data = dict()

        if form.validate_on_submit():
            bulan = form.bulan.data
            tahun = form.tahun.data
            kelas = form.kelas.data

            sql_absen = (
                db.session.query(AbsensiModel)
                .join(SiswaModel)
                .join(MengajarModel)
                .filter(
                    and_(
                        SiswaModel.kelas_id == kelas.id,
                        func.month(AbsensiModel.tgl_absen) == bulan.id,
                        func.year(AbsensiModel.tgl_absen) == tahun.tgl_absen.year,
                        MengajarModel.guru_id == current_user.id,
                    )
                )
                .group_by(AbsensiModel.siswa_id)
                .order_by(SiswaModel.first_name.asc())
                .all()
            )

            if not sql_absen:
                flash(
                    "Ma'af!\\nData yang dimaksud tidak ditemukan. Coba periksa kembali..!",
                    "error",
                )
            else:
                sql_kepsek = KepsekModel.query.filter_by(status="1").first()

                sql_tgl_pertemuan = (
                    db.session.query(AbsensiModel)
                    .join(SiswaModel)
                    .join(MengajarModel)
                    .filter(
                        and_(
                            func.month(AbsensiModel.tgl_absen) == bulan.id,
                            func.year(AbsensiModel.tgl_absen) == tahun.tgl_absen.year,
                            SiswaModel.kelas_id == kelas.id,
                            MengajarModel.guru_id == current_user.id,
                        )
                    )
                    .group_by(AbsensiModel.tgl_absen)
                    .order_by(AbsensiModel.tgl_absen.asc())
                )

                sql_siswa = SiswaModel.query.filter_by(kelas_id=kelas.id)

                data.update(
                    kepsek=f"{sql_kepsek.guru.first_name.title()} {sql_kepsek.guru.last_name.title()}",
                    nipKepsek=sql_kepsek.guru.user.username,
                    guru=[
                        f"{i.mengajar.guru.first_name.title()} {i.mengajar.guru.last_name.title()}"
                        for i in sql_absen
                    ][0],
                    nipGuru=[i.mengajar.guru.user.username for i in sql_absen][0],
                    tahunAjaran=[
                        i.mengajar.tahun_ajaran.th_ajaran for i in sql_tgl_pertemuan
                    ][0],
                    semester=[
                        i.mengajar.semester.semester.title() for i in sql_tgl_pertemuan
                    ][0],
                    bulan=bulan.nama_bulan.title(),
                    today=datetime.date(datetime.today()),
                    kelas=[i.siswa.kelas.kelas for i in sql_absen][0],
                    mapel=[i.mengajar.mapel.mapel.title() for i in sql_absen][0],
                    countPertemuan=sql_tgl_pertemuan.count(),
                    countSiswa=sql_siswa.count(),
                    countSiswaL=sql_siswa.filter_by(gender="laki-laki").count(),
                    countSiswaP=sql_siswa.filter_by(gender="perempuan").count(),
                )

                render = render_template(
                    "laporan/result_absen_mapel.html",
                    data=data,
                    absen=sql_absen,
                    tglPertemuan=sql_tgl_pertemuan,
                    AM=AbsensiModel,
                )
                response = make_response(render)
                return response

        user = dbs.get_one(GuruModel, user_id=current_user.id)
        session.update(
            first_name=user.first_name.title(), last_name=user.last_name.title()
        )

        render = render_template(
            "guru/modul/absen/daftar_hadir.html",
            wali_kelas=check_wali(),
            form=form,
        )
        response = make_response(render)
        return response
    else:
        abort(401)


@guru2.route("/rekap-kehadiran", methods=["GET", "POST"])
@login_required
def rekap_kehadiran():
    if current_user.group == "guru" and session["tipe_akun"] == "guru_mapel":
        data = {}
        form = FormSelectKehadiranSiswa()
        data["filename"] = "rekap-data"
        sql_kelas = (
            MengajarModel.query.filter_by(guru_id=current_user.id)
            .group_by("kelas_id")
            .order_by(MengajarModel.kelas_id.asc())
            .all()
        )
        sql_bulan = NamaBulanModel.query.all()
        sql_tahun = AbsensiModel.query.group_by(func.year(AbsensiModel.tgl_absen)).all()
        sql_kepsek = KepsekModel.query.filter_by(status=1).first()
        sql_guru = GuruModel.query.filter_by(user_id=current_user.id).first()
        for i in sql_kelas:
            form.kelas.choices.append((i.id, i.kelas))
        for i in sql_bulan:
            form.bulan.choices.append((i.id, i.nama_bulan.upper()))

        for i in sql_tahun:
            form.tahun.choices.append((i.tgl_absen.year, i.tgl_absen.year))

        if request.method == "POST" and form.validate_on_submit():
            kelas = request.form.get("kelas")
            bulan = request.form.get("bulan")
            tahun = request.form.get("tahun")
            sql_kehadiran = (
                db.session.query(AbsensiModel)
                .join(MengajarModel)
                .join(SiswaModel)
                .filter(AbsensiModel.mengajar_id == MengajarModel.id)
                .filter(func.month(AbsensiModel.tgl_absen) == bulan)
                .filter(func.year(AbsensiModel.tgl_absen) == tahun)
                .filter(MengajarModel.kelas_id == kelas)
                .filter(MengajarModel.guru_id == current_user.id)
                .group_by(AbsensiModel.siswa_id)
                .order_by(SiswaModel.first_name.asc())
            )

            for i in sql_kehadiran.all():
                data["kelas"] = i.siswa.kelas.kelas
                data["mapel"] = i.mengajar.mapel.mapel
                data["semester"] = i.mengajar.semester.semester
                data["tahun_ajaran"] = i.mengajar.tahun_ajaran.th_ajaran
                data["mengajar_id"] = i.mengajar_id
                data["bulan"] = min(
                    [k.nama_bulan for k in sql_bulan if k.id == i.tgl_absen.month]
                )

            data["today"] = datetime.date(datetime.today())
            data["kepsek"] = f"{sql_kepsek.guru.first_name} {sql_kepsek.guru.last_name}"
            data["nip_kepsek"] = sql_kepsek.guru.user.username
            data["guru"] = f"{sql_guru.first_name} {sql_guru.last_name}"
            data["nip_guru"] = f"{sql_guru.user.username}"

            sql_tgl_absen = (
                db.session.query(AbsensiModel)
                .filter(AbsensiModel.mengajar_id == MengajarModel.id)
                .filter(MengajarModel.guru_id == current_user.id)
                .filter(MengajarModel.kelas_id == kelas)
                .filter(func.month(AbsensiModel.tgl_absen) == bulan)
                .filter(func.year(AbsensiModel.tgl_absen) == tahun)
                .group_by(func.day(AbsensiModel.tgl_absen))
            )

            if sql_kehadiran.all():
                response = make_response(
                    render_template(
                        "guru/modul/absen/rekap_kehadiran.html",
                        sqlToday=get_kelas_today(),
                        sql_kehadiran=sql_kehadiran,
                        data=data,
                        sql_tgl_absen=sql_tgl_absen,
                        AbsensiModel=AbsensiModel,
                        func=func,
                    )
                )
                return response
            else:
                flash(
                    "Ma'af!\\nData yang dimaksud tidak ditemukan. Coba periksa kembali..!",
                    "error",
                )
        user = dbs.get_one(GuruModel, user_id=current_user.id)
        session.update(
            first_name=user.first_name.title(), last_name=user.last_name.title()
        )
        response = make_response(
            render_template(
                "guru/modul/absen/daftar_hadir.html",
                data=data,
                form=form,
                wali_kelas=check_wali(),
            )
        )
        return response

    abort(401)


@guru2.route("data-kehadiran-siswa")
@login_required
def data_kehadiran():
    if current_user.group == "guru" and session["tipe_akun"] == "guru_mapel":
        hari = today_()
        data = dict()
        mengajar_id = request.args.get("mengajar", type=int)
        sql_mengajar = db.session.query(MengajarModel).filter_by(id=mengajar_id).all()

        for i in sql_mengajar:
            data.update(id=i.id)

        sql_daftar_kelas = (
            db.session.query(MengajarModel)
            .join(HariModel)
            .join(SemesterModel)
            .filter(
                and_(
                    MengajarModel.guru_id == current_user.id,
                    SemesterModel.is_active == "1",
                    HariModel.hari == hari,
                )
            )
            .order_by(MengajarModel.jam_ke.asc())
        )

        user = dbs.get_one(GuruModel, user_id=current_user.id)
        session.update(
            first_name=user.first_name.title(), last_name=user.last_name.title()
        )

        render = render_template(
            "guru/modul/absen/daftar_hadir_harian.html",
            wali_kelas=check_wali(),
            data=data,
            sqlToday=sql_daftar_kelas.all(),
        )

        user = dbs.get_one(GuruModel, user_id=current_user.id)
        session.update(
            first_name=user.first_name.title(), last_name=user.last_name.title()
        )

        response = make_response(render)
        return response
    else:
        abort(401)


@guru2.route("get-data-kehadiran")
@login_required
def get_data_kehadiran():
    if current_user.group == "guru" and session["tipe_akun"] == "guru_mapel":
        today = datetime.date(datetime.today())
        data = dict()
        mengajar_id = request.args.get("mengajar", type=int)

        sql_absen = (
            db.session.query(AbsensiModel).join(MengajarModel)
            # .join(HariModel)
            .filter(
                and_(
                    AbsensiModel.mengajar_id == mengajar_id,
                    AbsensiModel.tgl_absen == today,
                    MengajarModel.guru_id == current_user.id,
                    # HariModel.hari == hari,
                ),
            )
        )

        user = dbs.get_one(GuruModel, user_id=current_user.id)
        session.update(
            first_name=user.first_name.title(), last_name=user.last_name.title()
        )

        render = render_template("helper/daftar_hadir_siswa.html", data=sql_absen)
        response = make_response(render)
        return response
    abort(401)
