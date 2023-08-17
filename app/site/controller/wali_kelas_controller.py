from calendar import monthrange
from datetime import datetime
from flask import (
    Flask,
    make_response,
    url_for,
    request,
    redirect,
    flash,
    render_template,
    Blueprint,
)
from flask_login import current_user, login_required
from sqlalchemy import func
from app.models.data_model import AbsensiModel
from app.models.master_model import (
    KepsekModel,
    MapelModel,
    MengajarModel,
    NamaBulanModel,
    WaliKelasModel,
)
from app.models.user_details_model import SiswaModel
from app.site.forms.form_letter_report import FormRekapAbsenWali, FormSelectMapel
from ...extensions import db

wali_kelas = Blueprint(
    "wali_kelas",
    __name__,
    static_folder="../static/",
    url_prefix="/wali-kelas/",
    template_folder="../templates/",
)

query = lambda sql: sql


def sql_wali_():
    sql = query(
        sql=db.session.query(WaliKelasModel)
        .filter(WaliKelasModel.guru_id == current_user.id)
        .first()
    )
    return sql


@wali_kelas.route("/index")
@login_required
def index():
    return render_template(
        "guru_wali_kelas/index_wali_kelas.html", sql_wali_=sql_wali_()
    )


@wali_kelas.route("data-siswa")
@login_required
def data_siswa():
    sql_siswa = (
        db.session.query(SiswaModel)
        .filter(SiswaModel.kelas_id == sql_wali_().kelas_id)
        .all()
    )

    response = make_response(
        render_template(
            "guru_wali_kelas/modul/siswa/data_siswa.html",
            sql_siswa=sql_siswa,
            sql_wali_=sql_wali_(),
        )
    )
    return response


@wali_kelas.route("rekap-absen", methods=["GET", "POST"])
@login_required
def rekap_absen():
    data = {}
    data["kelas"] = sql_wali_().kelas.kelas
    data["wali_kelas"] = f"{sql_wali_().guru.first_name} {sql_wali_().guru.last_name}"
    data["nip_wali"] = sql_wali_().guru.user.username

    sql_kepsek = KepsekModel.query.filter_by(status=1).first()
    data["kepsek"] = f"{sql_kepsek.guru.first_name} {sql_kepsek.guru.last_name}"
    data["nip_kepsek"] = f"{sql_kepsek.guru.user.username}"
    form = FormRekapAbsenWali()
    sql_bulan = NamaBulanModel.query
    sql_tahun = AbsensiModel.query.group_by(func.year(AbsensiModel.tgl_absen)).all()

    for i in sql_bulan.all():
        form.bulan.choices.append((i.id, i.nama_bulan.upper()))

    for i in sql_tahun:
        form.tahun.choices.append((i.tgl_absen.year, i.tgl_absen.year))

    if request.method == "POST" and form.validate_on_submit():
        bulan_id = request.form.get("bulan")
        tahun = request.form.get("tahun")

        sql_siswa = (
            db.session.query(AbsensiModel)
            .filter(AbsensiModel.mengajar_id == MengajarModel.id)
            .filter(AbsensiModel.siswa_id == SiswaModel.user_id)
            .filter(SiswaModel.kelas_id == sql_wali_().kelas_id)
            .filter(func.month(AbsensiModel.tgl_absen) == bulan_id)
            .filter(func.year(AbsensiModel.tgl_absen) == tahun)
            .group_by(AbsensiModel.siswa_id)
            .order_by(SiswaModel.first_name.asc())
            .all()
        )

        sql_ket = db.session.query(AbsensiModel)

        month_range = monthrange(int(tahun), int(bulan_id))
        data["month_range"] = month_range[1]
        data["bulan"] = sql_bulan.filter_by(id=bulan_id).first().nama_bulan
        data["today"] = datetime.date(datetime.today())
        data["semester"] = (
            min([i.mengajar.semester.semester for i in sql_siswa])
            if sql_siswa
            else None
        )
        data["ta"] = (
            min([i.mengajar.tahun_ajaran.th_ajaran for i in sql_siswa])
            if sql_siswa
            else None
        )
        if sql_siswa:
            response = make_response(
                render_template(
                    "admin/letter_report/result_rekap_bulan.html",
                    sql_siswa=sql_siswa,
                    data=data,
                    sql_ket=sql_ket,
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

    response = make_response(
        render_template(
            "guru_wali_kelas/modul/rekap_kehadiran/rekap_by_kelas.html",
            form=form,
            sql_wali_=sql_wali_(),
        )
    )
    return response


@wali_kelas.route("rekap-absen/mapel", methods=["GET", "POST"])
@login_required
def rekap_absen_mapel():
    data = {}
    form = FormSelectMapel()
    sql_mapel = MapelModel.query
    sql_bulan = NamaBulanModel.query
    sql_tahun = AbsensiModel.query.group_by(func.year(AbsensiModel.tgl_absen))
    sql_kepsek = KepsekModel.query.filter_by(status=1).first()
    for i in sql_mapel.all():
        form.mapel.choices.append((i.id, i.mapel.upper()))

    for i in sql_bulan.all():
        form.bulan.choices.append((i.id, i.nama_bulan.upper()))

    for i in sql_tahun.all():
        form.tahun.choices.append((i.tgl_absen.year, i.tgl_absen.year))

    if form.validate_on_submit() and request.method == "POST":
        mapel_id = form.mapel.data
        bulan_id = request.form.get("bulan")
        tahun = form.tahun.data

        sql_kehadiran = (
            db.session.query(AbsensiModel)
            .join(MengajarModel)
            .join(SiswaModel)
            .filter(AbsensiModel.mengajar_id == MengajarModel.id)
            .filter(func.month(AbsensiModel.tgl_absen) == bulan_id)
            .filter(func.year(AbsensiModel.tgl_absen) == tahun)
            .filter(MengajarModel.kelas_id == sql_wali_().kelas_id)
            .filter(MengajarModel.mapel_id == mapel_id)
            .group_by(AbsensiModel.siswa_id)
            .order_by(SiswaModel.first_name.asc())
        )

        if sql_kehadiran.all():
            for i in sql_kehadiran.all():
                data["kelas"] = i.siswa.kelas.kelas
                data["mapel"] = i.mengajar.mapel.mapel
                data["semester"] = i.mengajar.semester.semester
                data["tahun_ajaran"] = i.mengajar.tahun_ajaran.th_ajaran
                data["mengajar_id"] = i.mengajar_id
                data["bulan"] = min(
                    [k.nama_bulan for k in sql_bulan if k.id == i.tgl_absen.month]
                )
                data[
                    "guru"
                ] = f"{i.mengajar.guru.first_name} {i.mengajar.guru.last_name}"
            #########
            data["today"] = datetime.date(datetime.today())
            data["kepsek"] = f"{sql_kepsek.guru.first_name} {sql_kepsek.guru.last_name}"
            data["nip_kepsek"] = sql_kepsek.guru.user.username
            data["nip_guru"] = f"{i.mengajar.guru.user.username}"

            sql_tgl_absen = (
                db.session.query(AbsensiModel)
                .filter(AbsensiModel.mengajar_id == MengajarModel.id)
                # .filter(MengajarModel.guru_id == current_user.id)
                .filter(MengajarModel.mapel_id == mapel_id)
                .filter(MengajarModel.kelas_id == sql_wali_().kelas_id)
                .filter(func.month(AbsensiModel.tgl_absen) == bulan_id)
                .filter(func.year(AbsensiModel.tgl_absen) == tahun)
                .group_by(func.day(AbsensiModel.tgl_absen))
            )

            response = make_response(
                render_template(
                    "guru/modul/absen/rekap_kehadiran.html",
                    data=data,
                    sql_tgl_absen=sql_tgl_absen,
                    sql_kehadiran=sql_kehadiran,
                    AbsensiModel=AbsensiModel,
                )
            )

            return response
        else:
            flash(
                f"Ma'af..!\\nData yang dimaksud tidak ada. Silahkan periksa kembali.",
                "error",
            )

    response = make_response(
        render_template(
            "guru_wali_kelas/modul/rekap_kehadiran/rekap_by_mapel.html",
            sql_wali_=sql_wali_(),
            form=form,
        )
    )
    return response
