from calendar import monthrange
import string
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
from app.models.user_details_model import SiswaModel
from flask_login import login_required, current_user
from app.models.master_model import GuruBKModel
from app.models.data_model import *
from app.site.forms.form_absen import FormSelectAbsensi
from app.site.forms.form_guru_bk import *
from sqlalchemy import func, or_, and_
from app.lib.date_time import format_indo
from app.lib.filters import *
from builtins import enumerate
from app.site.forms.form_laporan import FormLaporanPelanggaran

guru_bk = Blueprint(
    "guru_bk",
    __name__,
    static_folder="../static/",
    template_folder="../templates/",
    url_prefix="/guru-bk",
)


methods = ["GET", "POST"]


def get_guru_bk() -> GuruBKModel:
    sql = GuruBKModel.query.filter_by(guru_id=current_user.id).first()
    return sql


@guru_bk.route("/index")
@login_required
def index():
    if current_user.is_authenticated:
        if current_user.id == get_guru_bk().guru_id:
            response = make_response(
                render_template("guru_bk/index_bk.html", guru_bk=get_guru_bk())
            )
            return response
        else:
            return abort(404)


# @guru_bk.route("data-pelanggaran", methods=["GET", "POST"])
# @login_required
# def data_pelanggar():
#     if current_user.is_authenticated:
#         if current_user.id == get_guru_bk().guru_id:
#             # sql_pelanggar = (
#             #     db.session.query(PelanggaranModel)
#             #     .order_by(PelanggaranModel.id.desc())
#             #     .all()
#             # )
#             sql_pelanggar = (
#                 db.session.query(
#                     PelanggaranModel,
#                     func.sum(JenisPelanggaranModel.poin_pelanggaran),
#                 )
#                 .join(JenisPelanggaranModel)
#                 .join(SiswaModel)
#                 .filter(
#                     or_(PelanggaranModel.status == None, PelanggaranModel.status == "")
#                 )
#                 .group_by(PelanggaranModel.siswa_id)
#                 # .order_by(func.sum(JenisPelanggaranModel.poin_pelanggaran.desc))
#                 .order_by(PelanggaranModel.id.desc())
#                 # .limit(6)
#             )
#             # $terbanyak = mysqli_query($connect, "SELECT detail_poin.nis, SUM(pelanggaran.poin) AS poin, siswa.nama_siswa FROM detail_poin JOIN pelanggaran ON detail_poin.id_pelanggaran=pelanggaran.id_pelanggaran JOIN siswa ON detail_poin.nis=siswa.nis GROUP BY detail_poin.nis ORDER BY SUM(pelanggaran.poin) DESC LIMIT 6");

#             sql_poin = (
#                 db.session.query(
#                     PelanggaranModel,
#                     func.sum(JenisPelanggaranModel.poin_pelanggaran),
#                 )
#                 .join(JenisPelanggaranModel)
#                 .join(SiswaModel)
#                 .group_by(PelanggaranModel.siswa_id)
#                 .order_by(func.sum(JenisPelanggaranModel.poin_pelanggaran.desc))
#                 .limit(6)
#             )

#             response = make_response(
#                 render_template(
#                     "guru_bk/modul/pelanggaran/daftar-pelanggar.html",
#                     guru_bk=get_guru_bk(),
#                     sql_pelanggar=sql_pelanggar,
#                     PelanggaranModel=PelanggaranModel,
#                     db=db,
#                     format=format_indo,
#                     sql_poin=sql_poin,
#                 )
#             )
#             return response
#         else:
#             return abort(404)


@guru_bk.route("/data-pelanggaran", methods=methods)
@login_required
def fetch_data_pelanggaran():
    if current_user.is_authenticated:
        if current_user.id == get_guru_bk().guru_id:
            data = (
                db.session.query(
                    PelanggaranModel,
                    func.count(PelanggaranModel.jenis_pelanggaran_id),
                    func.max(PelanggaranModel.status),
                    func.max(PelanggaranModel.id),
                )
                .group_by(PelanggaranModel.siswa_id)
                .order_by(PelanggaranModel.id.asc())
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


@guru_bk.route("/data-pelanggaran/edit", methods=["GET", "POST"])
@login_required
def edit_data_pelanggaran():
    if current_user.is_authenticated:
        if current_user.id == get_guru_bk().guru_id:
            form = FormEditPelanggar()

            id = request.args.get("idx")
            sql_pelanggaran = (
                db.session.query(PelanggaranModel).filter_by(id=id).first()
            )
            sql_jenis = JenisPelanggaranModel2.query.filter_by(status="1").all()
            form.siswa.data = f"{sql_pelanggaran.siswa.first_name.title()} {sql_pelanggaran.siswa.last_name.title()}"
            form.keterangan.data = sql_pelanggaran.note
            if request.method == "POST":
                # siswa_id = request.form.get("siswa")
                # jenis_pelanggaran_id = request.form.get("jenisPelanggaran")
                note = request.form.get("keterangan")

                # sql_pelanggaran.jenis_pelanggaran_id = jenis_pelanggaran_id
                sql_pelanggaran.note = note

                db.session.commit()
                response = make_response(redirect(url_for("guru_bk.data_pelanggar")))
                flash(f"Data Telah Di Perbaharui.", "info")
                return response

            return render_template(
                "guru_bk/modul/pelanggaran/edit-pelanggar.html",
                form=form,
                guru_bk=get_guru_bk(),
                sql_jenis=sql_jenis,
                sql_pelanggaran=sql_pelanggaran,
            )
        else:
            return abort(404)


@guru_bk.route("/data-pelanggaran/delete", methods=["GET", "POST"])
@login_required
def delete_data_pelanggaran():
    if current_user.is_authenticated:
        if current_user.id == get_guru_bk().guru_id:
            id = request.args.get("idx")
            sql_pelanggaran = PelanggaranModel.query.filter_by(id=id).first()

            db.session.delete(sql_pelanggaran)
            db.session.commit()

            response = make_response(redirect(url_for("guru_bk.data_pelanggar")))
            flash(f"Data Telah Di Hapus!", "error")
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
            print(str(request.url_rule))
            print(url_for("guru_bk.atur_pelanggaran"))
            print(str(request.url_rule) == str(url_for("guru_bk.atur_pelanggaran")))
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

            # print(f"{request.url_rule.rule}")

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


@guru_bk.route("/data-binaan", methods=["GET"])
@login_required
def data_pembinaan():
    if current_user.is_authenticated:
        if current_user.id == get_guru_bk().guru_id:
            data = (
                db.session.query(PembinaanModel, func.max(PembinaanModel.bina))
                .join(PelanggaranModel)
                .filter(PembinaanModel.pelanggaran_id == PelanggaranModel.id)
                .group_by(PelanggaranModel.siswa_id)
                .order_by(PembinaanModel.bina.asc())
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


@guru_bk.route("/add-pembinaan", methods=["POST", "GET"])
@login_required
def add_proses_pembinaan():
    if current_user.is_authenticated:
        if current_user.id == get_guru_bk().guru_id:
            pel_id = request.args.get("pel_id")

            check_ = PembinaanModel.query.filter_by(pelanggaran_id=pel_id)

            if check_.first() and check_.first().pelanggaran.siswa_id:
                bina = f"{check_.count() + 1}"

            else:
                bina = 1
            payload = PembinaanModel(bina, pelanggaran_id=pel_id)
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


@guru_bk.get("/detail-all-data")
@login_required
def detail_all_pelanggaran():
    if current_user.is_authenticated:
        if current_user.id == get_guru_bk().guru_id:
            id = request.args.get("id")

            detail_data = PelanggaranModel.query.filter_by(siswa_id=id).first()

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
            )

        else:
            return abort(404)
    else:
        return "<h2>Masalah pada autentikasi</h2>"




@guru_bk.route("add-tata-tertib", methods=["GET", "POST"])
@login_required
def add_tata_tertib():
    if current_user.is_authenticated:
        if current_user.id == get_guru_bk().guru_id:
            form = FormTambahTTertibUtama(request.form)

            if request.method == "POST" and form.validate_on_submit():
                t_tertib = form.tataTertib.data
                
                data = TataTertibModel(tata_tertib=" ".join(t_tertib.split()))

                db.session.add(data)
                db.session.commit()
                flash("Tata tertib telah ditambahkan!", "success")

                return redirect(url_for("guru_bk.get_tata_tertib"))

            return render_template(
                "guru_bk/modul/tata_tertib/add_tata_tertib.html",
                guru_bk=get_guru_bk(),
                form=form,
            )
        else:
            abort(404)
            
    return 'Masalah pada autentikasi!'


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
            )
        else:
            return abort(404)
    return "<h2>Masalah pada autentikasi</h2>"

@guru_bk.route("/get-sub-1", methods=["GET", "POST"])
@login_required
def get_one_tata_tertib():
    if current_user.is_authenticated:
        if current_user.id == get_guru_bk().guru_id:
            form = FormTambahTTertib(request.form)
            t_ = TataTertibModel.query
            for i in t_.all():
                form.pilihTTertib.choices.append((i.id, f"{i.id} - {i.tata_tertib}"))
            id = request.args.get("id")
            data = TataTertibModel.query.filter_by(id=id).first()

            form.tataTertib.data = data.tata_tertib

            if request.method == "POST" and form.validate_on_submit():
                utama_id = form.pilihTTertib.data
                t_tertib = form.tataTertib.data
                data.utama_id = utama_id
                data.tata_tertib = t_tertib

                db.session.commit()

                flash("Sub tata tertib 1 telah diperbaharui!", "success")

                return redirect(url_for("guru_bk.get_tata_tertib"))

            return render_template(
                "guru_bk/modul/tata_tertib/sub_tata_tertib1/edit_tata_tertib.html",
                guru_bk=get_guru_bk(),
                form=form,
                data=data,
            )
        else:
            return abort(404)

    return "<h2>Masalah pada autentikasi</h2>"


# @guru_bk.route("/add-tata-tertib", methods=["POST", "GET"])
# @login_required
# def add_sub_tata_tertib1():
#     if current_user.is_authenticated:
#         if current_user.id == get_guru_bk().guru_id:
#             data_t = TataTertibModel.query.all()
#             form = FormTambahTTertib(request.form)

#             for index, i in enumerate(data_t, start=1):
#                 form.pilihTTertib.choices.append(
#                     (
#                         i.id,
#                         f"{index} - {truncate(i.tata_tertib, length=40, killwords=True)}",
#                     )
#                 )

#             t_tertib = form.tataTertib.data
#             t_id = form.pilihTTertib.data

#             if request.method == "POST" and form.validate_on_submit():
#                 data = SubTataTertibModel1(tata_tertib=t_tertib, t_tertib_id=t_id)

#                 db.session.add(data)
#                 db.session.commit()
#                 flash(
#                     message="Sub tata tertib-1 telah ditambahkan.", category="success"
#                 )
#                 return redirect(url_for("guru_bk.get_tata_tertib"))

#             else:
#                 return render_template(
#                     "guru_bk/modul/tata_tertib/sub_tata_tertib1/add_tata_tertib.html",
#                     guru_bk=get_guru_bk(),
#                     form=form,
#                 )
#         else:
#             return abort(404)

#     return "<h2>Masalah pada autentikasi</h2>"




# @guru_bk.route("/add-sub-tata-tertib", methods=["GET", "POST"])
# @login_required
# def add_sub_ttertib2():
#     if current_user.is_authenticated:
#         if current_user.id == get_guru_bk().guru_id:
#             form = FormTambahSubTTertib(request.form)
#             data_tertib = SubTataTertibModel1.query.all()
#             for i, item in enumerate(data_tertib, start=1):
#                 form.pilihTTertib.choices.append(
#                     (
#                         item.id,
#                         truncate(
#                             s=f"{i}. {item.tata_tertib}",
#                             length=50,
#                             killwords=True,
#                         ),
#                     )
#                 )

#             if request.method == "POST":
#                 ttertib_id = form.pilihTTertib.data
#                 s_ttertib = form.subTataTertib.data

#                 data = SubTataTertibModel2(
#                     sub1_id=int(ttertib_id), tata_tertib=s_ttertib
#                 )

#                 db.session.add(data)
#                 db.session.commit()

#                 flash(
#                     message="Sub tata tertib-2 telah ditambahkan!", category="success"
#                 )
#                 return redirect(url_for("guru_bk.get_tata_tertib"))
#             return render_template(
#                 "guru_bk/modul/tata_tertib/sub_tata_tertib2/add_sub_tata_tertib.html",
#                 guru_bk=get_guru_bk(),
#                 form=form,
#             )
#         else:
#             return abort(404)

#     return "<h2>Masalah pada autentikasi</h2>"


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
                .all()
            )
            sql_wali = WaliKelasModel.query.filter_by(
                kelas_id=form.siswa.data.kelas_id if form.siswa.data else None
            ).first()

            if form.validate_on_submit():
                # print(form.kelas.data.id)
                # print(form.siswa.data.user_id)

                if not sql_pelanggaran:
                    flash("Data yang dimaksud belum melakukan pelanggaran.", "error")

                return render_template(
                    "laporan/laporan_pelanggaran.html",
                    guru_bk=get_guru_bk(),
                    form=form,
                    pelanggaran=sql_pelanggaran,
                    wali=sql_wali,
                )

            return render_template(
                "laporan/laporan_pelanggaran.html",
                guru_bk=get_guru_bk(),
                form=form,
                pelanggaran=sql_pelanggaran,
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

            result_pelanggaran = (
                db.session.query(
                   PelanggaranModel
                )
                .filter_by(siswa_id=siswa_id)
            )

            

            rendered = render_template(
                "laporan/result_pelanggaran.html",
                siswa=siswa,
                bina=count_pembinaan,
                pelanggaran=result_pelanggaran,
                today=today
            )

            response = make_response(rendered)
            # response.headers["Content-Type"] = "application/pdf"
            # response.headers["Content-Disposition"] = "inline; filename=output.pdf"

            return response
        else:
            abort(404)

    return "Masalah pada autentikasi."
