from calendar import monthrange
import string
import click
from flask import (
    Blueprint,
    abort,
    app,
    render_template,
    request,
    redirect,
    flash,
    Blueprint,
    make_response,
    url_for,
)
from jinja2 import TemplateNotFound
from pytz import utc
from app.models.user_details_model import SiswaModel
from flask_login import login_required, current_user
from app.models.master_model import GuruBKModel
from app.models.data_model import *
from app.site.forms.form_absen import FormSelectAbsensi
from app.site.forms.form_guru_bk import *
from sqlalchemy import func, or_, and_
from app.lib.date_time import format_indo, utc_makassar
from app.lib.filters import *
from builtins import enumerate
from app.site.forms.form_laporan import FormLaporanPelanggaran

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


@guru_bk.route("/data-pelanggaran/delete-jenis-pelanggaran")
@login_required
def delete_jenis_pelanggaran():
    if current_user.is_authenticated:
        if current_user.id == get_guru_bk().guru_id:
            id = request.args.get("id", type=int)

            model = JenisPelanggaranModel2
            query = model.fetchOne(id=id)

            db.session.delete(query)
            db.session.commit()

            flash("Jenis Pelanggaran telah dihapus!", "success")
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

            if request.method == "POST" and form.validate_on_submit():
                tata_tertib = form.tataTertib.data
                sql_update.tata_tertib = tata_tertib
                db.session.commit()

                flash("Tata-Tertib telah diperbaharui!", "success")

                return redirect(url_for("guru_bk.get_tata_tertib"))

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
        if current_user.id == get_guru_bk().guru_id:
            form = FormSelectAbsensi()
            dt_kelas = KelasModel.query.all()
            dt_bulan = NamaBulanModel.query.all()
            dt_year = AbsensiModel.query.group_by(
                func.year(AbsensiModel.tgl_absen)
            ).all()

            for i in dt_kelas:
                form.kelas.choices.append((i.id, i.kelas))

            for i in dt_bulan:
                form.bulan.choices.append((i.id, i.nama_bulan.title()))

            for i in dt_year:
                form.tahun.choices.append((i.tgl_absen.year, i.tgl_absen.year))

            if form.validate_on_submit():
                kelas = request.form.get("kelas")
                bulan = request.form.get("bulan")
                tahun = request.form.get("tahun")

                dt_siswa = (
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

                if dt_siswa:
                    dt_wali = WaliKelasModel.query.filter_by(kelas_id=kelas).first()
                    dt_kepsek = KepsekModel.query.filter_by(status=1).first()
                    dt_ket = db.session.query(AbsensiModel)
                    month_range = monthrange(int(tahun), int(bulan))

                    data = {}
                    data["bulan"] = (
                        NamaBulanModel.query.filter_by(id=bulan).first().nama_bulan
                    )
                    data["kelas"] = KelasModel.query.filter_by(id=kelas).first().kelas
                    data[
                        "wali_kelas"
                    ] = f"{dt_wali.guru.first_name} {dt_wali.guru.last_name}"
                    data["nip_wali"] = dt_wali.guru.user.username
                    data["semester"] = min(
                        [i.mengajar.semester.semester for i in dt_siswa]
                    )
                    data["ta"] = min(
                        [i.mengajar.tahun_ajaran.th_ajaran for i in dt_siswa]
                    )
                    data["month_range"] = month_range[1]
                    data["today"] = datetime.date(datetime.today())
                    data[
                        "kepsek"
                    ] = f"{dt_kepsek.guru.first_name} {dt_kepsek.guru.last_name}"

                    data["nip_kepsek"] = dt_kepsek.guru.user.username

                    return render_template(
                        "admin/letter_report/result_rekap_bulan.html",
                        AbsensiModel=AbsensiModel,
                        sql_siswa=dt_siswa,
                        data=data,
                        db=db,
                        func=func,
                        sql_ket=dt_ket,
                    )

                else:
                    flash("Data tidak ditemukan, harap periksa kembali!", "warning")
                    response = make_response(
                        render_template(
                            "admin/letter_report/rekap_bulan.html", form=form
                        )
                    )
                    return response

            response = make_response(
                render_template(
                    "admin/letter_report/rekap_bulan.html",
                    form=form,
                    guru_bk=get_guru_bk(),
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
