from calendar import monthrange
from datetime import datetime
from flask import make_response, request, flash, render_template, Blueprint
from flask_login import current_user, login_required
from sqlalchemy import func, and_
from app.lib.date_time import format_indo
from app.lib.filters import hari_minggu, hari_sabtu
from app.models.data_model import (
    AbsensiModel,
    JenisPelanggaranModel2,
    PelanggaranModel,
    PembinaanModel,
)
from app.models.master_model import (
    HariModel,
    KepsekModel,
    MengajarModel,
    SemesterModel,
    TahunAjaranModel,
    WaliKelasModel,
)
from app.models.user_details_model import GuruModel, SiswaModel
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
    count_siswa = SiswaModel.query.filter_by(kelas_id=sql_wali_().kelas_id).count()
    count_laki2 = SiswaModel.query.filter_by(
        kelas_id=sql_wali_().kelas_id, gender="laki-laki"
    ).count()
    count_perempuan = SiswaModel.query.filter_by(
        kelas_id=sql_wali_().kelas_id, gender="perempuan"
    ).count()

    sql_pelanggaran = (
        db.session.query(PelanggaranModel)
        .join(SiswaModel)
        .filter(SiswaModel.kelas_id == sql_wali_().kelas_id)
        .group_by(PelanggaranModel.siswa_id)
        .order_by(SiswaModel.first_name.asc())
        .all()
    )

    data = dict(
        laki2=count_laki2,
        perempuan=count_perempuan,
        siswa=count_siswa,
    )

    return render_template(
        "guru_wali_kelas/index_wali_kelas.html",
        sql_wali_=sql_wali_(),
        data=data,
        pelanggaran=sql_pelanggaran,
        PM=PelanggaranModel.query,
        BM=PembinaanModel.query,
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
    form = FormRekapAbsenWali()
    data = dict()

    if request.method == "POST" and form.validate_on_submit():
        tahun = form.tahun.data.tgl_absen
        bulan = form.bulan.data
        sql_absen = (
            db.session.query(AbsensiModel)
            .join(SiswaModel)
            .filter(
                and_(
                    func.year(AbsensiModel.tgl_absen) == tahun,
                    func.month(AbsensiModel.tgl_absen) == bulan.id,
                    SiswaModel.kelas_id == sql_wali_().kelas_id,
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
            sql_siswa = SiswaModel.query
            sql_ket = AbsensiModel.query
            month_range = monthrange(year=int(tahun.year), month=int(bulan.id))
            data.update(
                wali=f"{sql_wali_().guru.first_name.title()} {sql_wali_().guru.last_name.title()}",
                nipWali=sql_wali_().guru.user.username,
                kepsek=f"{sql_kepsek.guru.first_name.title()} {sql_kepsek.guru.last_name.title()}",
                nipKepsek=sql_kepsek.guru.user.username,
                tahunAjaran=[i.mengajar.tahun_ajaran.th_ajaran for i in sql_absen][0],
                semester=[i.mengajar.semester.semester.upper() for i in sql_absen][0],
                monthRange=month_range[1],
                countSiswa=sql_siswa.filter_by(kelas_id=sql_wali_().kelas_id).count(),
                countSiswaL=sql_siswa.filter_by(
                    kelas_id=sql_wali_().kelas_id, gender="laki-laki"
                ).count(),
                countSiswaP=sql_siswa.filter_by(
                    kelas_id=sql_wali_().kelas_id, gender="perempuan"
                ).count(),
                bulan=bulan,
                intBulan=bulan.id,
                tahun=tahun.year,
                today=datetime.date(datetime.today()),
                kelas=sql_wali_().kelas.kelas,
            )

            render = render_template(
                "laporan/result_absensi.html",
                AM=AbsensiModel,
                data=data,
                ket=sql_ket,
                func=func,
                absen=sql_absen,
                and_=and_,
                sabtu=hari_sabtu,
                minggu=hari_minggu,
            )

            response = make_response(render)
            return response

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
    form = FormSelectMapel()
    data = dict()

    if request.method == "POST" and form.validate_on_submit():
        mapel = form.mapel.data
        bulan = form.bulan.data
        tahun = form.tahun.data

        sql_absen = (
            db.session.query(AbsensiModel)
            .join(SiswaModel)
            .join(MengajarModel)
            .filter(
                and_(
                    SiswaModel.kelas_id == sql_wali_().kelas_id,
                    func.month(AbsensiModel.tgl_absen) == bulan.id,
                    func.year(AbsensiModel.tgl_absen) == tahun.tgl_absen.year,
                    MengajarModel.mapel_id == mapel.id,
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
                        MengajarModel.mapel_id == mapel.id,
                        func.month(AbsensiModel.tgl_absen) == bulan.id,
                        func.year(AbsensiModel.tgl_absen) == tahun.tgl_absen.year,
                        SiswaModel.kelas_id == sql_wali_().kelas_id,
                    )
                )
                .group_by(AbsensiModel.tgl_absen)
                .order_by(AbsensiModel.tgl_absen.asc())
            )

            sql_siswa = SiswaModel.query.filter_by(kelas_id=sql_wali_().kelas_id)

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
                kelas=sql_wali_().kelas.kelas,
                mapel=mapel,
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

    response = make_response(
        render_template(
            "guru_wali_kelas/modul/rekap_kehadiran/rekap_by_mapel.html",
            sql_wali_=sql_wali_(),
            form=form,
        )
    )
    return response


@wali_kelas.route("pelanggaran-siswa")
@login_required
def get_pelanggaran_siswa():
    id = request.args.get("id")
    detail_data = PelanggaranModel.query.filter_by(siswa_id=id).first()
    sql_jenisP = JenisPelanggaranModel2.query.all()
    sql_pelapor = GuruModel.query.all()
    riwayat_pelanggaran = (
        db.session.query(PelanggaranModel)
        .filter(PelanggaranModel.siswa_id == detail_data.siswa_id)
        .all()
    )

    render = render_template(
        "guru_bk/modul/pelanggaran/detail-all-pelanggaran.html",
        sql_wali_=sql_wali_(),
        detail=detail_data,
        riwayat=riwayat_pelanggaran,
        format=format_indo,
        jp=sql_jenisP,
        pelapor=sql_pelapor,
    )
    response = make_response(render)
    return response


@wali_kelas.route("/jadwal-pelajaran-siswa")
@login_required
def get_jadwal_siswa():
    sql_semester = SemesterModel.query.filter_by(is_active="1").first()
    sql_tahun_ajaran = TahunAjaranModel.query.filter_by(is_active="1").first()

    sql_jadwal = db.session.query(MengajarModel).filter_by(
        semester_id=sql_semester.id,
        tahun_ajaran_id=sql_tahun_ajaran.id,
        kelas_id=sql_wali_().kelas_id,
    )

    sql_hari = db.session.query(HariModel).all()

    render = render_template(
        "guru_wali_kelas/modul/jadwal/jadwal_siswa.html",
        sql_wali_=sql_wali_(),
        sqlHari=sql_hari,
        jadwal=sql_jadwal,
        MM=MengajarModel,
    )

    response = make_response(render)
    return response
