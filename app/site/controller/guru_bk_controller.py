from calendar import monthrange
import string
import click
from flask import (
    Blueprint,
    abort,
    render_template,
    request,
    redirect,
    flash,
    Blueprint,
    make_response,
    url_for,
)
from jinja2 import TemplateError, TemplateNotFound
from app.api.controller.master_controller import Kelas
from app.models.user_details_model import SiswaModel
from flask_login import login_required, current_user
from app.models.master_model import GuruBKModel
from app.models.data_model import *
from app.site.forms.form_guru import (
    FormEditGuru,
    FormGetProfileGuru,
    FormUpdatePassword,
)
from app.site.forms.form_guru_bk import *
from sqlalchemy import func, and_
from app.lib.date_time import format_indo, utc_makassar
from app.lib.filters import *
from builtins import enumerate
from app.site.forms.form_laporan import FormLaporanPelanggaran
from app.site.forms.form_letter_report import FormRekapAbsen

guru_bk = Blueprint(
    "guru_bk",
    __name__,
    static_folder="../static/",
    template_folder="../templates/",
    url_prefix="/guru-bk",
    cli_group="bk",
)


methods = ["GET", "POST"]


@guru_bk.cli.command("create")
@click.argument("name")
def create(name):
    ...


def get_guru_bk() -> GuruBKModel:
    sql = GuruBKModel.query.filter_by(guru_id=current_user.id).first()
    return sql


@guru_bk.route("/index")
@login_required
def index():
    if current_user.is_authenticated:
        if current_user.group == "bk":
            count_siswa = SiswaModel.query.count()
            count_siswa_melanggar = PelanggaranModel.query.group_by(
                PelanggaranModel.siswa_id
            ).count()
            count_binaan = PembinaanModel.query.group_by(
                PembinaanModel.siswa_id
            ).count()
            response = make_response(
                render_template(
                    "guru_bk/index_bk.html",
                    siswa=count_siswa,
                    melanggar=count_siswa_melanggar,
                    pembinaan=count_binaan,
                )
            )
            return response
        else:
            return abort(404)


@guru_bk.route("/data-pelanggaran", methods=methods)
@login_required
def fetch_data_pelanggaran():
    if current_user.is_authenticated:
        if current_user.id == get_guru_bk().guru_id:
            data = (
                db.session.query(
                    PelanggaranModel,
                    func.count(PelanggaranModel.jenis_pelanggaran_id)
                    # func.max(PelanggaranModel.status),
                    # func.max(PelanggaranModel.id),
                )
                .group_by(PelanggaranModel.siswa_id)
                .order_by(PelanggaranModel.siswa_id.desc())
            )

            return render_template(
                "guru_bk/modul/pelanggaran/data-pelanggar.html",
                guru_bk=get_guru_bk(),
                data=data,
            )

        else:
            abort(404)

    return "<h2>Masalah pada autentikasi</h2>"


@guru_bk.route("/data-pelanggaran/add-pelanggaran", methods=methods)
@login_required
def add_data_pelanggar():
    if current_user.is_authenticated:
        if current_user.id == get_guru_bk().guru_id:
            form = FormTambahPelanggar(request.form)
            sql_kelas = KelasModel.query.all()
            sql_jenis = JenisPelanggaranModel2.query.filter_by(status="1").all()
            sql_siswa = SiswaModel.query.all()
            for i in sql_kelas:
                form.kelas.choices.append((i.id, i.kelas))
            for i in sql_jenis:
                form.jenisPelanggaran.choices.append((i.id, i.jenis_pelanggaran))

            if request.method == "POST" and form.validate_on_submit():
                siswa_id = request.form.get("siswa")
                jenis_id = request.form.get("jenisPelanggaran")
                pelapor = form.pelapor.data.user_id
                note = request.form.get("catatan").capitalize()

                """
                    Melakukan pengecekan siswa, apabila telah melakukan pelanggaran
                    lebih dari 3X maka update semua status menjadi `Perlu Pembinaan`.
                    pengecekan di lakukan sebelum merender halaman `Data Pelanggaran`
                """

                check_siswa = PelanggaranModel.query.filter_by(siswa_id=siswa_id)

                if check_siswa.first():
                    status = f"Pelanggaran Ke-{check_siswa.count() + 1}"
                    insert_pelanggar = PelanggaranModel(
                        siswaId=siswa_id,
                        jenisPelanggaran_id=jenis_id,
                        note=note,
                        status=status,
                        pelapor_id=pelapor,
                    )

                else:
                    status = f"Pelanggaran Ke-1"
                    insert_pelanggar = PelanggaranModel(
                        siswaId=siswa_id,
                        jenisPelanggaran_id=jenis_id,
                        note=note,
                        status=status,
                        pelapor_id=pelapor,
                    )

                db.session.add(insert_pelanggar)
                db.session.commit()

                response = make_response(
                    redirect(url_for("guru_bk.fetch_data_pelanggaran"))
                )
                flash(f"Data Pelanggar Berhasil Di Tambahkan.", "success")
                return response
            else:
                response = make_response(
                    render_template(
                        "guru_bk/modul/pelanggaran/tambah-pelanggar.html",
                        guru_bk=get_guru_bk(),
                        form=form,
                        sql_siswa=sql_siswa,
                    )
                )
                return response
        else:
            return abort(404)


@guru_bk.route("/detail-pelanggaran")
@login_required
def detail_pelanggaran():
    if current_user.is_authenticated:
        if current_user.id == get_guru_bk().guru_id:
            siswa_id = request.args.get("siswa")
            pelanggaran_id = request.args.get("pelanggaran")

            identitas = PelanggaranModel.query.filter_by(siswa_id=siswa_id).first()
            data = (
                db.session.query(PelanggaranModel)
                .filter(PelanggaranModel.siswa_id == siswa_id)
                .filter(PelanggaranModel.jenis_pelanggaran_id == pelanggaran_id)
                .all()
            )

            page = render_template(
                "guru_bk/modul/pelanggaran/detail-pelanggaran.html",
                guru_bk=get_guru_bk(),
                data=data,
                detail=identitas,
                format=format_indo,
            )
            return page

        else:
            abort(404)
    else:
        return "Masalah pada autentikasi..."


@guru_bk.get("/data-pelanggaran/detail-all")
@login_required
def detail_all_pelanggaran():
    try:
        if current_user.is_authenticated:
            if current_user.id == get_guru_bk().guru_id:
                id = request.args.get("id")

                detail_data = PelanggaranModel.query.filter_by(siswa_id=id).first()
                sql_jenisP = JenisPelanggaranModel2.query.all()
                sql_pelapor = GuruModel.query.all()
                riwayat_pelanggaran = (
                    db.session.query(PelanggaranModel)
                    .filter(PelanggaranModel.siswa_id == detail_data.siswa_id)
                    .all()
                )

                return render_template(
                    "guru_bk/modul/pelanggaran/detail-all-pelanggaran.html",
                    detail=detail_data,
                    riwayat=riwayat_pelanggaran,
                    format=format_indo,
                    guru_bk=get_guru_bk(),
                    jp=sql_jenisP,
                    pelapor=sql_pelapor,
                )

            else:
                return abort(404)
        else:
            return "<h2>Masalah pada autentikasi</h2>"

    except TemplateNotFound:
        abort(404)


@guru_bk.route("/data-pelanggaran/edit", methods=["GET", "POST"])
@login_required
def edit_pelanggaran():
    if current_user.is_authenticated:
        if current_user.group == "bk":
            id = request.args.get("pelanggaran")
            siswa_id = request.args.get("siswa")

            jp = request.form.get("jenisPelanggaran")
            tgl = request.form.get("tgl")
            pelapor = request.form.get("pelapor")
            note = request.form.get("catatan")

            sql_update = PelanggaranModel.query.filter_by(id=id).first()

            if request.method == "POST":
                # print(jp)
                # print(tgl)
                # print(pelapor)
                # print(note)
                sql_update.jenis_pelanggaran_id = jp
                sql_update.tgl_report = tgl
                sql_update.guru_id = pelapor
                sql_update.note = note.lower()

                db.session.commit()

                flash("Data pelanggaran telah diperbaharui.", "success")
                direct = redirect(url_for(".detail_all_pelanggaran", id=siswa_id))
                response = make_response(direct)
                return response
        else:
            abort(404)

    else:
        return "Terjadi masalah login akun."


@guru_bk.route("/data-pelanggaran/delete", methods=["GET", "POST"])
@login_required
def delete_data_pelanggaran():
    if current_user.is_authenticated:
        if current_user.id == get_guru_bk().guru_id:
            id = request.args.get("pelanggaran")
            siswa_id = request.args.get("siswa", type=int)
            sql_pelanggaran = PelanggaranModel.query.filter_by(id=id).first()

            sql_pembinaan = PembinaanModel.query.filter_by(pelanggaran_id=id).first()

            db.session.delete(sql_pembinaan)
            db.session.delete(sql_pelanggaran)
            db.session.commit()

            flash(f"Data Telah Di Hapus!", "success")
            response = make_response(
                redirect(url_for(".detail_all_pelanggaran", id=siswa_id))
            )
            return response
        else:
            return abort(404)
    else:
        return "<h2>Masalah pada autentikasi</h2>"


@guru_bk.route("/data-pelanggaran/atur", methods=methods)
@login_required
def atur_pelanggaran():
    if current_user.is_authenticated:
        if current_user.id == get_guru_bk().guru_id:
            form = FormJenisPelanggaran(request.form)
            model = JenisPelanggaranModel2
            data = model.fetchAll()
            return render_template(
                "guru_bk/modul/pelanggaran/atur_pelanggaran.html",
                guru_bk=get_guru_bk(),
                form=form,
                data=data,
                rq=request,
            )
        else:
            return abort(404)
    else:
        return "<h2>Masalah pada autentikasi</h2>"


@guru_bk.route("/data-pelanggaran/tambah-jenis-pelanggaran", methods=methods)
@login_required
def add_jenis_pelanggaran():
    if current_user.is_authenticated:
        if current_user.id == get_guru_bk().guru_id:
            form = FormJenisPelanggaran(request.form)
            data = JenisPelanggaranModel2.fetchAll()

            if request.method == "POST" and form.validate_on_submit():
                jp = form.jenisPelanggaran.data.title()
                status = form.status.data
                query = JenisPelanggaranModel2(jenisPelanggaran=jp, status=status)

                db.session.add(query)
                db.session.commit()
                flash("Jenis Pelanggaran telah ditambahkan!", "success")

                return redirect(url_for("guru_bk.atur_pelanggaran"))
            return render_template(
                "guru_bk/modul/pelanggaran/atur_pelanggaran.html",
                guru_bk=get_guru_bk(),
                form=form,
                data=data,
                rq=request,
            )
        else:
            abort(404)
    return "<h2>Masalah pada autentikasi</h2>"


@guru_bk.route("/data-pelanggaran/edit-jenis-pelanggaran", methods=methods)
@login_required
def get_one_jenis_pelanggaran():
    if current_user.is_authenticated:
        if current_user.id == get_guru_bk().guru_id:
            form = FormEditJenisPelanggaran(request.form)
            model = JenisPelanggaranModel2
            data = model.fetchAll()
            id = request.args.get("id")
            fetch_one = model.fetchOne(id=id)

            form.jenisPelanggaran.data = fetch_one.jenis_pelanggaran.title()
            form.status.data = "0" if fetch_one.status == "" else fetch_one.status

            if request.method == "POST" and form.validate_on_submit():
                fetch_one.jenis_pelanggaran = request.form.get("jenisPelanggaran")
                fetch_one.status = request.form.get("status")

                db.session.commit()
                flash("Jenis Pelanggaran telah diperbaharui!", "success")
                return redirect(url_for("guru_bk.atur_pelanggaran"))

            return render_template(
                "guru_bk/modul/pelanggaran/atur_pelanggaran.html",
                guru_bk=get_guru_bk(),
                data=data,
                form=form,
                rq=request,
                id=id,
            )
        else:
            abort(404)
    return "<h2>Masalah pada autentikasi</h2>"


@guru_bk.route("/data-pelanggaran/delete-jenis-pelanggaran", methods=methods)
@login_required
def delete_jenis_pelanggaran():
    if current_user.is_authenticated:
        if current_user.id == get_guru_bk().guru_id:
            id = request.args.get("jp", type=int)

            sql = JenisPelanggaranModel2.query.filter_by(id=id).first()

            if not sql:
                flash("Data tidak ditemukan. Status 404", "error")
            else:
                db.session.delete(sql)
                db.session.commit()

                flash("Jenis Pelanggaran telah dihapus!", "success")
                return redirect(url_for("guru_bk.atur_pelanggaran"))
            return redirect(url_for("guru_bk.atur_pelanggaran"))
        else:
            abort(404)
    return "<h2>Masalah pada autentikasi</h2>"


@guru_bk.route("/data-pembinaan", methods=["GET"])
@login_required
def data_pembinaan():
    if current_user.is_authenticated:
        if current_user.id == get_guru_bk().guru_id:
            data = (
                db.session.query(PembinaanModel)
                .group_by(PembinaanModel.siswa_id)
                .order_by(PembinaanModel.siswa_id.desc())
                .all()
            )
            response = make_response(
                render_template(
                    "guru_bk/modul/pembinaan/data-pembinaan.html",
                    guru_bk=get_guru_bk(),
                    data=data,
                )
            )
            return response

        else:
            return abort(404)

    else:
        return "<h2>Masalah pada autentikasi</h2>"


@guru_bk.route("/data-pembinaan/add", methods=["POST", "GET"])
@login_required
def add_proses_pembinaan():
    if current_user.is_authenticated:
        if current_user.id == get_guru_bk().guru_id:
            pel_id = request.args.get("pelanggaran")
            siswa_id = request.args.get("siswa")
            status = str(object="0")
            bina = int
            check = PembinaanModel.query

            if check.filter_by(pelanggaran_id=pel_id).first():
                flash("Data siswa dengan pelanggaran tersebut telah dibina.", "error")
                return redirect(url_for(".fetch_data_pelanggaran"))
            else:
                if not check.filter_by(siswa_id=siswa_id).first():
                    bina = 1
                else:
                    bina = check.filter_by(siswa_id=siswa_id).count() + 1

                tgl_bina = datetime.date(datetime.today())

                if check.filter_by(status="0", siswa_id=siswa_id).first():
                    flash(
                        "Ma'af tidak bisa menambahkan data, selesaikan terlebih dahulu binaan sebelumnya!",
                        "error",
                    )

                    return redirect(url_for(".fetch_data_pelanggaran"))

                else:
                    payload = PembinaanModel(
                        bina,
                        pelanggaran_id=pel_id,
                        siswa_id=siswa_id,
                        status=status,
                        tgl_bina=tgl_bina,
                    )

                    db.session.add(payload)
                    db.session.commit()

                flash("Data pembinaan telah ditambahkan", "success")
            page = url_for("guru_bk.data_pembinaan")

            resp = make_response(redirect(page))
            return resp
        else:
            abort(404)

    else:
        return "Masalah pada autentikasi..."


@guru_bk.route("/data-pembinaan/update-status", methods=["GET", "POST", "PUT"])
@login_required
def pembinaan_update_status():
    if current_user.is_authenticated:
        if current_user.group == "bk":
            id = request.args.get("pembinaan", type=int)

            sql = PembinaanModel.query.filter_by(id=id).first()

            date_format = utc_makassar()
            sql.status = "1"
            sql.tgl_bina = date_format
            db.session.commit()
            flash("Siswa telah dibina.", "success")
            direct = redirect(url_for(".data_pembinaan"))
            response = make_response(direct)
            return response

        else:
            abort(404)

    else:
        return "Terjadi masalah pada autentikasi."


@guru_bk.route("add-tata-tertib", methods=["GET", "POST"])
@login_required
def add_tata_tertib():
    if current_user.is_authenticated:
        if current_user.group == "bk":
            form = FormTambahTTertib(request.form)

            data = TataTertibModel.query.all()

            if request.method == "POST" and form.validate_on_submit():
                t_tertib = form.tataTertib.data

                data = TataTertibModel(tata_tertib=" ".join(t_tertib.split()))

                db.session.add(data)
                db.session.commit()
                flash("Tata tertib telah ditambahkan!", "success")

                return redirect(url_for("guru_bk.get_tata_tertib"))
            # return redirect(url_for("guru_bk.get_tata_tertib", form=form))

            return render_template(
                "guru_bk/modul/tata_tertib/get_tata_tertib.html",
                guru_bk=get_guru_bk(),
                form=form,
                data=data,
            )
        else:
            abort(404)

    return "Masalah pada autentikasi!"


@guru_bk.route("/tata-tertib", methods=["GET", "POST"])
@login_required
def get_tata_tertib():
    if current_user.is_authenticated:
        if current_user.id == get_guru_bk().guru_id:
            form = FormTambahTTertib()
            utama = TataTertibModel.query.all()
            data = TataTertibModel.query.all()
            alfabet = list(string.ascii_lowercase)

            return render_template(
                "guru_bk/modul/tata_tertib/get_tata_tertib.html",
                guru_bk=get_guru_bk(),
                data=data,
                utama=utama,
                alfabet=alfabet,
                enumerate=enumerate,
                form=form,
                request=request,
            )
        else:
            return abort(404)
    return "<h2>Masalah pada autentikasi</h2>"


@guru_bk.route("/get-single-tata-tertib", methods=["GET", "POST"])
@login_required
def get_one_tata_tertib():
    if current_user.is_authenticated:
        if current_user.id == get_guru_bk().guru_id:
            form = FormTambahTTertib(request.form)

            id = request.args.get("tataTertib")
            data = TataTertibModel.query.all()

            sql_update = TataTertibModel.query.filter_by(id=id).first()

            if sql_update:
                form.tataTertib.data = sql_update.tata_tertib

            return render_template(
                "guru_bk/modul/tata_tertib/get_tata_tertib.html",
                guru_bk=get_guru_bk(),
                form=form,
                data=data,
                id=id,
            )
        else:
            return abort(404)

    return "<h2>Masalah pada autentikasi</h2>"


@guru_bk.route("/tata-tertib/update", methods=methods)
@login_required
def update_tata_tertib():
    try:
        if current_user.is_authenticated:
            if current_user.group == "bk":
                id = request.args.get("tataTertib", type=int)
                tata_tertib = request.form.get("tataTertib")
                print(f"Tata Tertib == {tata_tertib}")
                sql_update = TataTertibModel.query.filter_by(id=id).first()

                if sql_update:
                    sql_update.tata_tertib = tata_tertib
                    db.session.commit()
                    flash("Tata tertib telah diperbaharui.", "success")
                else:
                    flash("Terjadi kesalahan, tata tertib gagal diperbaharui.", "error")

                direct = redirect(url_for(".get_tata_tertib"))
                response = make_response(direct)

                return response

            else:
                return abort(404)

    except TemplateError:
        return abort(401)


@guru_bk.route("/tata-tertib/delete")
@login_required
def delete_tata_tertib():
    if current_user.is_authenticated:
        if current_user.group == "bk":
            tata_tertib_id = request.args.get("tata_tertib", type=int)
            sql_data = TataTertibModel.query.filter_by(id=tata_tertib_id).first()

            if not sql_data:
                flash("Data yang dimaksud tidak ditemuka.", "error")

            db.session.delete(sql_data)
            db.session.commit()
            flash("Data telah dihapus dari database.", "success")
            redirect_ = redirect(url_for(".get_tata_tertib"))
            response = make_response(redirect_)
            return response
        else:
            abort(404)
    return "Terjadi masalah pada autentikasi."


@guru_bk.route("/laporan-kehadiran", methods=["GET", "POST"])
@login_required
def laporan_kehadiran():
    if current_user.is_authenticated:
        if current_user.group == "bk":
            form = FormRekapAbsen()

            if form.validate_on_submit():
                sql_wali = WaliKelasModel.query.filter_by(
                    kelas_id=form.kelas.data.id
                ).first()

                sql_absen = (
                    db.session.query(AbsensiModel)
                    .join(SiswaModel)
                    .filter(
                        and_(
                            func.month(AbsensiModel.tgl_absen) == form.bulan.data.id,
                            func.year(AbsensiModel.tgl_absen)
                            == form.tahun.data.tgl_absen.year,
                        )
                    )
                    .filter(SiswaModel.kelas_id == form.kelas.data.id)
                    .group_by(AbsensiModel.siswa_id)
                    .order_by(SiswaModel.first_name.asc())
                    .all()
                )

                sql_kepsek = KepsekModel.query.filter_by(status="1").first()

                sql_ket = AbsensiModel.query
                sql_siswa = SiswaModel.query

                data_absen = []
                data = dict()
                if sql_absen:
                    for i in sql_absen:
                        data_absen.append(
                            dict(
                                id=i.id,
                                nama=f"{i.siswa.first_name.title()} {i.siswa.last_name.title()}",
                                semester=i.mengajar.semester.semester.upper(),
                            )
                        )

                    month_range = monthrange(
                        int(form.tahun.data.tgl_absen.year), int(form.bulan.data.id)
                    )
                    data.update(
                        kelas=form.kelas.data,
                        bulan=form.bulan.data,
                        intBulan=form.bulan.data.id,
                        tahun=form.tahun.data.tgl_absen.year,
                        wali=f"{sql_wali.guru.first_name.title()} {sql_wali.guru.last_name.title()}",
                        nipWali=sql_wali.guru.user.username,
                        semester=[i.mengajar.semester.semester for i in sql_absen][
                            0
                        ].upper(),
                        tahunAjaran=[
                            i.mengajar.tahun_ajaran.th_ajaran for i in sql_absen
                        ][0],
                        monthRange=month_range[1],
                        today=datetime.date(datetime.today()),
                        kepsek=f"{sql_kepsek.guru.first_name.title()} {sql_kepsek.guru.last_name.title()}",
                        nipKepsek=sql_kepsek.guru.user.username,
                        countSiswa=sql_siswa.filter_by(
                            kelas_id=form.kelas.data.id
                        ).count(),
                        countSiswaL=sql_siswa.filter_by(
                            kelas_id=form.kelas.data.id, gender="laki-laki"
                        ).count(),
                        countSiswaP=sql_siswa.filter_by(
                            kelas_id=form.kelas.data.id, gender="perempuan"
                        ).count(),
                    )
                else:
                    flash("Data absensi siswa yang dimaksud tidak ditemukan.", "error")
                    response = make_response(
                        render_template(
                            "laporan/form_rekap_absensi.html",
                            form=form,
                        )
                    )
                    return response

                render = render_template(
                    "laporan/result_absensi.html",
                    data=data,
                    absen=sql_absen,
                    ket=sql_ket,
                    func=func,
                    AM=AbsensiModel,
                    and_=and_,
                    sabtu=hari_sabtu,
                    minggu=hari_minggu,
                )
                response = make_response(render)
                return render

            response = make_response(
                render_template(
                    "laporan/form_rekap_absensi.html",
                    form=form,
                )
            )
            return response
        else:
            abort(404)

    return "Masalah pada autentiasi!"


@guru_bk.route("/laporan-pelanggaran", methods=["POST", "GET"])
@login_required
def laporan_pelanggaran():
    if current_user.is_authenticated:
        if current_user.id == get_guru_bk().guru_id:
            form = FormLaporanPelanggaran()

            if form.kelas.data:
                form.siswa.query = SiswaModel.query.filter_by(
                    kelas_id=form.kelas.data.id
                ).all()
            else:
                form.siswa.query = SiswaModel.query.filter(None).all()

            sql_pelanggaran = (
                PelanggaranModel.query.filter_by(
                    siswa_id=form.siswa.data.user_id if form.siswa.data else None
                )
                # .group_by(PelanggaranModel.siswa_id)
            )
            sql_wali = WaliKelasModel.query.filter_by(
                kelas_id=form.siswa.data.kelas_id if form.siswa.data else None
            ).first()

            count_pembinaan = PembinaanModel.query.filter_by(
                siswa_id=form.siswa.data.user_id if form.siswa.data else None
            ).count()

            if form.validate_on_submit():
                # print(form.kelas.data.id)
                # print(form.siswa.data.user_id)

                if not sql_pelanggaran:
                    flash("Data yang dimaksud belum melakukan pelanggaran.", "error")

                return render_template(
                    "laporan/laporan_pelanggaran.html",
                    guru_bk=get_guru_bk(),
                    form=form,
                    pelanggaran=sql_pelanggaran.all(),
                    count_pelanggaran=sql_pelanggaran.count(),
                    count_pembinaan=count_pembinaan,
                    wali=sql_wali,
                )

            return render_template(
                "laporan/laporan_pelanggaran.html",
                guru_bk=get_guru_bk(),
                form=form,
                pelanggaran=sql_pelanggaran.all(),
                count_pelanggaran=sql_pelanggaran.count(),
                count_pembinaan=count_pembinaan,
                wali=sql_wali,
            )

        else:
            abort(404)

    return "Terjadi masalah pada autentikasi!"


@guru_bk.route("/get-siswa")
def get_siswa():
    kelas_id = request.args.get("kelas")
    sql_siswa = SiswaModel.query.filter_by(kelas_id=kelas_id).all()

    # return [
    #     f"<option value={siswa.user_id}>{siswa.first_name.title()} {siswa.last_name.title()}</option>"
    #     for siswa in sql_siswa
    # ]
    return render_template("helper/opt_siswa.html", siswa=sql_siswa)


@guru_bk.route("/result-pelanggaran", methods=["GET", "POST"])
@login_required
def result_pelanggaran():
    if current_user.is_authenticated:
        if current_user.group == "bk":
            siswa_id = request.args.get("siswa")
            count_pembinaan = (
                db.session.query(PembinaanModel)
                .filter(PembinaanModel.siswa_id == siswa_id)
                .order_by(PembinaanModel.siswa_id.desc())
                .first()
            )

            siswa = SiswaModel.query.filter_by(user_id=siswa_id).first()
            today = datetime.date(datetime.today())

            result_pelanggaran = db.session.query(PelanggaranModel).filter_by(
                siswa_id=siswa_id
            )

            rendered = render_template(
                "laporan/result_pelanggaran2.html",
                siswa=siswa,
                bina=count_pembinaan,
                pelanggaran=result_pelanggaran,
                today=today,
            )

            response = make_response(rendered)
            # response.headers["Content-Type"] = "application/pdf"
            # response.headers["Content-Disposition"] = "inline; filename=output.pdf"

            return response
        else:
            abort(404)

    return "Masalah pada autentikasi."


@guru_bk.route("/akun/profil", methods=methods)
@login_required
def profil_bk():
    if current_user.is_authenticated:
        if current_user.group == "bk":
            form = FormGetProfileGuru()

            sql_one = GuruModel.query.filter_by(user_id=current_user.id).first()

            form.nip.data = sql_one.user.username
            form.fullname.data = (
                f"{sql_one.first_name.title()} {sql_one.last_name.title()}"
            )
            form.gender.data = sql_one.gender
            form.agama.data = sql_one.agama
            form.alamat.data = sql_one.alamat.title() if sql_one.alamat else "-"
            form.telp.data = sql_one.telp if sql_one.telp else "-"

            render = render_template("akun/profile_guru.html", form=form)
            response = make_response(render)
            return response

        else:
            return abort(404)
    return abort(401)


@guru_bk.route("/akun/profil/update", methods=methods)
@login_required
def update_profil():
    if current_user.is_authenticated:
        if current_user.group == "bk":
            form = FormGetProfileGuru()

            sql_one = GuruModel.query.filter_by(user_id=current_user.id).first()
            sql_one.user.username = form.nip.data
            first_name = ""
            last_name = ""
            first_name, *last_name = form.fullname.data.split()
            if len(last_name) == 0:
                last_name = first_name
            elif len(last_name) != 0:
                last_name = " ".join(last_name)
            sql_one.first_name = first_name
            sql_one.last_name = last_name
            sql_one.agama = form.agama.data
            sql_one.gender = form.gender.data.lower()
            sql_one.alamat = form.alamat.data
            sql_one.telp = form.telp.data

            db.session.commit()

            direct = redirect(url_for(".index"))
            response = make_response(direct)
            flash("Data diri telah diperbaharui.", "success")

            return response
        else:
            return abort(404)
    else:
        return abort(401)


@guru_bk.route("/akun/kata-sandi", methods=methods)
@login_required
def password_bk():
    if current_user.is_authenticated:
        if current_user.group == "bk":
            form = FormUpdatePassword()
            render = render_template("akun/update_password.html", form=form)
            response = make_response(render)
            return response
        else:
            return abort(404)

    return abort(401)


@guru_bk.route("/akun/kata-sandi/update", methods=methods)
@login_required
def update_password():
    if current_user.is_authenticated:
        if current_user.group == "bk":
            form = FormUpdatePassword()

            sql_update = UserModel.query.filter_by(id=current_user.id).first()

            password = UserModel.generate_pswd(form.password.data)
            sql_update.password = password

            db.session.commit()
            direct = redirect(url_for(".index"))
            response = make_response(direct)

            flash("Passsword telah diperbaharui.", "success")
            return response
        else:
            return abort(404)

    return abort(401)
