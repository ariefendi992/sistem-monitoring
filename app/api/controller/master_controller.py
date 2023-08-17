import time
from flask import Blueprint, jsonify, request
from app.models.user_details_model import SiswaModel
from app.models.master_model import *
from app.lib.base_model import BaseModel
from app.lib.status_code import *
from sqlalchemy import func

master = Blueprint("master", __name__, url_prefix="/api/v2/master")


class Kelas:
    @master.route("/kelas/create", methods=["POST", "GET"])
    def create():
        kelas = request.json.get("kelas")

        base = BaseModel(KelasModel(kelas=kelas))
        kelas_check = base.get_one_or_none(kelas=kelas)
        if kelas_check:
            return jsonify(msg="Data Class has been already exists."), HTTP_409_CONFLICT
        else:
            base.create()
            return (
                jsonify(msg=f"Data kelas {base.model.kelas} telah ditambahkan."),
                HTTP_201_CREATED,
            )

    @master.route("/kelas/get-all", endpoint="kelas_all", methods=["GET"])
    def get_all():
        base = BaseModel(KelasModel)
        model = base.get_all()

        data = []
        for kelas in model:
            data.append(
                {
                    "id": kelas.id,
                    "kelas": kelas.kelas,
                    "laki": kelas.jml_laki,
                    "perempuan": kelas.jml_perempuan,
                    "jum_seluruh": kelas.jml_seluruh,
                }
            )

        return jsonify({"data": data}), HTTP_200_OK

    @master.route("/kelas/get-one/<int:id>", methods=["GET", "PUT", "DELETE"])
    def get_one(id):
        base = BaseModel(KelasModel)
        model = base.get_one_or_none(id=id)

        if request.method == "GET":
            if model is not None:
                return jsonify(
                    id=model.id,
                    kelas=model.kelas,
                    laki=model.jml_laki,
                    perempuan=model.jml_perempuan,
                    seluruh=model.jml_seluruh,
                )
            else:
                return jsonify(msg="Data not found."), HTTP_404_NOT_FOUND

        elif request.method == "PUT":
            kelas = request.json.get("kelas")
            laki = request.json.get("laki")
            perempuan = request.json.get("perempuan")
            seluruh = request.json.get("seluruh")

            # class_check = base.get_one_or_none(kelas=kelas)
            # if class_check:
            #     return jsonify(msg=f'Data dengan {kelas} sudah ada.')
            # else:
            model.kelas = kelas
            model.jml_laki = laki
            model.jml_perempuan = perempuan
            model.jml_seluruh = seluruh
            base.edit()
            return (
                jsonify(msg=f"Data Kelas {model.kelas} telah diperbaharui."),
                HTTP_200_OK,
            )

        elif request.method == "DELETE":
            base.delete(model)
            return jsonify(msg="Data has been deleted."), HTTP_204_NO_CONTENT

    @master.route("/kelas/update-jumlah/<int:id>", methods=["PUT", "GET"])
    def update_jumlah(id):
        base = BaseModel(KelasModel)
        model = base.get_one(id=id)
        i = model.id
        countSiswaLaki = (
            db.session.query(func.count(SiswaModel.kelas_id))
            .filter(SiswaModel.kelas_id == model.id)
            .filter(SiswaModel.gender == "laki-laki")
            .scalar()
        )
        countSiswaPerempuan = (
            db.session.query(func.count(SiswaModel.kelas_id))
            .filter(SiswaModel.kelas_id == model.id)
            .filter(SiswaModel.gender == "perempuan")
            .scalar()
        )
        countAllSiswa = (
            db.session.query(func.count(SiswaModel.kelas_id))
            .filter(SiswaModel.kelas_id == model.id)
            .scalar()
        )
        model.jml_perempuan = countSiswaPerempuan
        model.jml_laki = countSiswaLaki
        model.jml_seluruh = countAllSiswa

        base.edit()

        return jsonify(id=i, kelas=model.kelas, l=countSiswaLaki, p=countSiswaPerempuan)


class Mapel(object):
    # @master.add_url_rule('/mapel/create', methods=['POST','GET'])
    @master.route("/mapel/create", endpoint="mapel", methods=["POST", "GET"])
    def create():
        mapel = request.json.get("mapel")

        base = BaseModel(MapelModel(mapel=mapel))
        mapel_check = base.get_one_or_none(mapel=mapel)
        if mapel_check:
            return jsonify(msg="Data Class has been already exists."), HTTP_409_CONFLICT
        else:
            base.create()
            return (
                jsonify(
                    msg=f"Data mata pelajaran {base.model.mapel} telah di tambahkan."
                ),
                HTTP_201_CREATED,
            )

    @master.route("/mapel/get-all", endpoint="mapel-all", methods=["GET"])
    def get_all():
        base = BaseModel(MapelModel)
        model = base.get_all()

        data = []
        for mapel in model:
            data.append({"id": mapel.id, "mapel": mapel.mapel})

        return jsonify({"data": data}), HTTP_200_OK

    @master.route(
        "/mapel/get-one/<int:id>",
        endpoint="mapel-single",
        methods=["GET", "PUT", "DELETE"],
    )
    def get_one(id):
        base = BaseModel(MapelModel)
        model = base.get_one_or_none(id=id)

        if request.method == "GET":
            if model is not None:
                return jsonify(id=model.id, mapel=model.mapel)
            else:
                return jsonify(msg="Data not found."), HTTP_404_NOT_FOUND

        elif request.method == "PUT":
            mapel = request.json.get("mapel")

            mapel_check = base.get_one_or_none(mapel=mapel)
            if mapel_check:
                return jsonify(msg=f"Data dengan {mapel} sudah ada.")
            else:
                model.mapel = mapel
                base.edit()
                return (
                    jsonify(msg=f"Data mapel {model.mapel}, telah di perbaharui."),
                    HTTP_200_OK,
                )

        elif request.method == "DELETE":
            if not model:
                return (
                    jsonify(msg="Data Mata Pelajaran tidak ada di database."),
                    HTTP_404_NOT_FOUND,
                )
            else:
                base.delete(model)
                return jsonify(msg="Data has been deleted."), HTTP_204_NO_CONTENT


class Hari(object):
    @master.route("/hari/create", endpoint="hari", methods=["POST", "GET"])
    def create():
        hari = request.json.get("hari")

        base = BaseModel(HariModel(hari=hari))
        hari_check = base.get_one_or_none(hari=hari)
        if hari_check:
            return jsonify(msg="Data Class has been already exists."), HTTP_409_CONFLICT
        else:
            base.create()
            return (
                jsonify(msg=f"Data Hari {base.model.hari} telah ditambahkan."),
                HTTP_201_CREATED,
            )

    @master.route("/hari/get-all", endpoint="hari-all", methods=["GET"])
    def get_all():
        base = BaseModel(HariModel)
        model = base.get_all()

        data = []
        for hari in model:
            data.append({"id": hari.id, "hari": hari.hari.title()})

        return jsonify(data=data), HTTP_200_OK

    @master.route(
        "/hari/get-one/<int:id>",
        endpoint="hari-single",
        methods=["GET", "PUT", "DELETE"],
    )
    def get_one(id):
        base = BaseModel(HariModel)
        model = base.get_one_or_none(id=id)

        if request.method == "GET":
            if model is not None:
                return jsonify(id=model.id, hari=model.hari)
            else:
                return jsonify(msg="Data not found."), HTTP_404_NOT_FOUND

        elif request.method == "PUT":
            hari = request.json.get("hari")

            class_check = base.get_one_or_none(hari=hari)
            if class_check:
                return jsonify(msg=f"Data dengan {hari} sudah ada.")
            else:
                model.hari = hari
                base.edit()
                return jsonify(id=model.id, hari=model.hari), HTTP_200_OK

        elif request.method == "DELETE":
            base.delete(model)
            return jsonify(msg="Data has been deleted."), HTTP_204_NO_CONTENT


class TahunAjaran(object):
    @master.route("/ajaran/create", endpoint="ajaran", methods=["POST", "GET"])
    def create():
        ajaran = request.json.get("ajaran")
        status = request.json.get("status")

        base = BaseModel(TahunAjaranModel(ajaran=ajaran, status=status))
        ajaran_check = base.get_one_or_none(th_ajaran=ajaran)
        if ajaran_check:
            return jsonify(msg="Data Class has been already exists."), HTTP_409_CONFLICT
        else:
            base.create()
            return (
                jsonify(
                    msg=f"Data tahun ajaran {base.model.th_ajaran} telah ditambahkan."
                ),
                HTTP_201_CREATED,
            )

    @master.route("/ajaran/get-all", endpoint="ajaran-all", methods=["GET"])
    def get_all():
        base = BaseModel(TahunAjaranModel)
        model = base.get_all()

        data = []
        for ajaran in model:
            data.append(
                {
                    "id": ajaran.id,
                    "th_ajaran": ajaran.th_ajaran,
                    "status": True if ajaran.is_active == "1" else False,
                }
            )

        return jsonify({"data": data}), HTTP_200_OK

    @master.route(
        "/ajaran/get-one/<int:id>",
        endpoint="ajaran-single",
        methods=["GET", "PUT", "DELETE"],
    )
    def get_one(id):
        base = BaseModel(TahunAjaranModel)
        model = base.get_one_or_none(id=id)

        if request.method == "GET":
            if model is not None:
                return jsonify(
                    id=model.id,
                    ajaran=model.th_ajaran,
                    status=True if model.is_active == "1" else False,
                )
            else:
                return jsonify(msg="Data tahun ajaran not found."), HTTP_404_NOT_FOUND

        elif request.method == "PUT":
            ajaran = request.json.get("ajaran")
            status = request.json.get("status")

            # class_check = base.get_one_or_none(th_ajaran=ajaran)
            # if class_check:
            #     return jsonify(msg=f'Data dengan {ajaran} sudah ada.')
            # else:
            model.th_ajaran = ajaran
            model.is_active = status
            base.edit()
            return (
                jsonify(msg=f"Data tahun ajaran {model.th_ajaran} telah diperbaharui"),
                HTTP_200_OK,
            )

        elif request.method == "DELETE":
            base.delete(model)
            return jsonify(msg="Data has been deleted."), HTTP_204_NO_CONTENT


class Semester(object):
    @master.route("/semester/create", endpoint="semester", methods=["POST", "GET"])
    def create():
        semester = request.json.get("semester")
        active = request.json.get("status")

        base = BaseModel(SemesterModel(semester, active))
        sms_check = base.get_one_or_none(semester=semester)
        if sms_check:
            return jsonify(msg="Data Class has been already exists."), HTTP_409_CONFLICT
        else:
            base.create()
            return (
                jsonify(msg=f"Data Semester {base.model.semester} telah di tambahkan."),
                HTTP_201_CREATED,
            )

    @master.route("/semester/get-all", endpoint="semester-all", methods=["GET"])
    def get_all():
        base = BaseModel(SemesterModel)
        model = base.get_all()

        data = []
        for sms in model:
            data.append(
                {
                    "id": sms.id,
                    "semester": sms.semester,
                    "status": True if sms.is_active == "1" else False,
                }
            )

        return jsonify({"data": data}), HTTP_200_OK

    @master.route(
        "/semester/get-one/<int:id>",
        endpoint="semester-single",
        methods=["GET", "PUT", "DELETE"],
    )
    def get_one(id):
        base = BaseModel(SemesterModel)
        model = base.get_one_or_none(id=id)

        if request.method == "GET":
            if model is not None:
                return jsonify(
                    id=model.id,
                    semester=model.semester,
                    status=True if model.is_active == "1" else False,
                )
            else:
                return jsonify(msg="Data not found."), HTTP_404_NOT_FOUND

        elif request.method == "PUT":
            # semester = request.json.get('semester')
            active = request.json.get("status")

            # class_check = base.get_one_or_none(semester=semester)
            if not model:
                return (
                    jsonify(msg=f"Data dengan semester tidak ditemukan."),
                    HTTP_404_NOT_FOUND,
                )
            else:
                # model.semester = semester
                model.is_active = active
                base.edit()
                return (
                    jsonify(msg=f"Data Semester {model.semester} telah diperbaharui"),
                    HTTP_200_OK,
                )

        elif request.method == "DELETE":
            base.delete(model)
            return jsonify(msg="Data has been deleted."), HTTP_204_NO_CONTENT


class Jam(object):
    @master.route("/jam/create", endpoint="jam", methods=["POST", "GET"])
    def create():
        jam = request.json.get("jam")
        if jam == "":
            return (
                jsonify(msg="Gagal input data, karena form inputan belum dipilih."),
                HTTP_400_BAD_REQUEST,
            )
        base = BaseModel(JamMengajarModel(jam=jam))
        jam_check = base.get_one_or_none(jam=jam)
        if jam_check:
            return jsonify(msg="Data has been already exists."), HTTP_409_CONFLICT
        else:
            base.create()
            return (
                jsonify(msg=f"Data jam {base.model.jam} berhasil ditambahkan."),
                HTTP_201_CREATED,
            )

    @master.route("/jam/get-all", endpoint="jam-all", methods=["GET"])
    def get_all():
        base = BaseModel(JamMengajarModel)
        model = base.get_all()

        data = []
        for jam in model:
            data.append({"id": jam.id, "jam": jam.jam})

        return jsonify({"data": data}), HTTP_200_OK

    @master.route(
        "/jam/get-one/<int:id>", endpoint="jam-single", methods=["GET", "PUT", "DELETE"]
    )
    def get_one(id):
        base = BaseModel(JamMengajarModel)
        model = base.get_one_or_none(id=id)

        if request.method == "GET":
            if model is not None:
                return jsonify(id=model.id, jam=model.jam)
            else:
                return jsonify(msg="Data not found."), HTTP_404_NOT_FOUND

        elif request.method == "PUT":
            jam = request.json.get("jam")

            model.jam = jam
            base.edit()
            return jsonify(msg=f"Data jam {model.jam} telah diperbaharui."), HTTP_200_OK

        elif request.method == "DELETE":
            base.delete(model)
            return jsonify(msg="Data has been deleted."), HTTP_204_NO_CONTENT


class WaliKelas(object):
    @master.route("/wali-kelas/create", endpoint="wali-kelas", methods=["POST", "GET"])
    def create():
        guru_id = request.json.get("guru_id")
        kelas_id = request.json.get("kelas_id")

        if guru_id == "" or kelas_id == "":
            return (
                jsonify(
                    msg="Gagal input data karena nama guru atau kelas masih kosong"
                ),
                HTTP_400_BAD_REQUEST,
            )

        base = BaseModel(WaliKelasModel(guru_id=guru_id, kelas_id=kelas_id))
        guru_check = base.get_one_or_none(guru_id=guru_id)
        kelas_check = base.get_one_or_none(kelas_id=kelas_id)

        if guru_check:
            return jsonify(msg="Data has been already exists."), HTTP_409_CONFLICT

        elif guru_check and kelas_check:
            return jsonify(msg="Data has been already exists."), HTTP_409_CONFLICT

        elif guru_check or kelas_check:
            return jsonify(msg="Data has been already exists."), HTTP_409_CONFLICT

        else:
            base.create()
            return (
                jsonify(
                    msg=f"Data Wali Kelas {base.model.guru.first_name} telah ditambahkan."
                ),
                HTTP_201_CREATED,
            )

    @master.route("/wali-kelas/get-all", endpoint="wali-kelas-all", methods=["GET"])
    def get_all():
        base = BaseModel(WaliKelasModel)
        model = base.get_all()

        data = []
        for wali in model:
            data.append(
                {
                    "id": wali.id,
                    "nip": wali.guru.user.username,
                    "first_name": wali.guru.first_name,
                    "last_name": wali.guru.last_name,
                    "kelas": wali.kelas.kelas,
                }
            )

        return jsonify(data=data), HTTP_200_OK

    @master.route(
        "/wali-kelas/get-one/<int:id>",
        endpoint="wali-kelas-single",
        methods=["GET", "PUT", "DELETE"],
    )
    def get_one(id):
        base = BaseModel(WaliKelasModel)
        model = base.get_one_or_none(id=id)

        if request.method == "GET":
            if model is not None:
                return (
                    jsonify(
                        id=model.id,
                        first_name=model.guru.first_name,
                        last_name=model.guru.last_name,
                        kelas=model.kelas.kelas,
                    ),
                    HTTP_200_OK,
                )
            else:
                return jsonify(msg="Data not found."), HTTP_404_NOT_FOUND

        elif request.method == "PUT":
            guru_id = request.json.get("guru_id")
            kelas_id = request.json.get("kelas_id")

            model.guru_id = guru_id
            model.kelas_id = kelas_id
            base.edit()
            return (
                jsonify(
                    msg=f"Data Wali Kelas {model.guru.first_name} telah di perbaharui."
                ),
                HTTP_200_OK,
            )

        elif request.method == "DELETE":
            base.delete(model)
            return jsonify(msg="Data has been deleted."), HTTP_204_NO_CONTENT


class KepalaSekolah(object):
    @master.route("/kepsek/create", endpoint="kepsek-create", methods=["POST", "GET"])
    def create():
        guru_id = request.json.get("guru_id")

        base = BaseModel(KepsekModel(guruId=guru_id))
        guru_check = base.get_one_or_none(guru_id=guru_id)

        if guru_check:
            return jsonify(msg="Data has been already exists."), HTTP_409_CONFLICT
        else:
            base.create()
            return (
                jsonify(
                    msg=f"Data Kepala Sekolah {base.model.guru.first_name} telah ditambahkan."
                ),
                HTTP_201_CREATED,
            )

    @master.route("/kepsek/get-all", endpoint="kepsek-all", methods=["GET"])
    def get_all():
        base = BaseModel(KepsekModel)
        model = base.get_all()

        data = []
        for _ in model:
            data.append(
                {
                    "id": _.id,
                    "nip": _.guru.user.username,
                    "first_name": _.guru.first_name,
                    "last_name": _.guru.last_name,
                    "status": "aktif" if _.status == "1" else "tidak aktif",
                }
            )

        return jsonify(data=data), HTTP_200_OK

    @master.route(
        "/kepsek/get-one/<int:id>",
        endpoint="kepsek-single",
        methods=["GET", "PUT", "DELETE"],
    )
    def get_one(id):
        base = BaseModel(KepsekModel)
        model = base.get_one_or_none(id=id)

        if request.method == "GET":
            if model is not None:
                return (
                    jsonify(
                        id=model.id,
                        first_name=model.guru.first_name,
                        last_name=model.guru.last_name,
                        status=model.status,
                    ),
                    HTTP_200_OK,
                )
            else:
                return jsonify(msg="Data not found."), HTTP_404_NOT_FOUND

        elif request.method == "PUT":
            guru_id = request.json.get("guru_id")
            status = request.json.get("status")

            model.guru_id = guru_id
            model.status = status
            base.edit()

            return (
                jsonify(
                    msg=f"Data Kepala Sekolah {model.guru.first_name} telah diperbaharui."
                ),
                HTTP_200_OK,
            )

        elif request.method == "DELETE":
            base.delete(model)
            return jsonify(msg="Data has been deleted."), HTTP_204_NO_CONTENT


class GuruBK(object):
    @master.route("/guru-bk/create", endpoint="guru-bk-create", methods=["POST", "GET"])
    def create():
        guru_id = request.json.get("guru_id")
        status = request.json.get("status")

        base = BaseModel(GuruBKModel(guruId=guru_id, status=status))
        guru_check = base.get_one_or_none(guru_id=guru_id)

        if guru_check:
            return jsonify(msg="Data has been already exists."), HTTP_409_CONFLICT
        else:
            base.create()
            return (
                jsonify(
                    msg=f"Data Guru BK {base.model.guru.first_name} telah ditambahkan."
                ),
                HTTP_201_CREATED,
            )

    @master.route("/guru-bk/get-all", endpoint="guru-bk-all", methods=["GET"])
    def get_all():
        base = BaseModel(GuruBKModel)
        model = base.get_all()

        data = []
        for _ in model:
            data.append(
                {
                    "id": _.id,
                    "nip": _.guru.user.username,
                    "first_name": _.guru.first_name,
                    "last_name": _.guru.last_name,
                    "status": "aktif" if _.status == "1" else "tidak",
                }
            )

        return jsonify(data=data), HTTP_200_OK

    @master.route(
        "/guru-bk/get-one/<int:id>",
        endpoint="guru-bk-single",
        methods=["GET", "PUT", "DELETE"],
    )
    def get_one(id):
        base = BaseModel(GuruBKModel)
        model = base.get_one_or_none(id=id)

        if request.method == "GET":
            if model is not None:
                return (
                    jsonify(
                        id=model.id,
                        first_name=model.guru.first_name,
                        last_name=model.guru.last_name,
                    ),
                    HTTP_200_OK,
                )
            else:
                return jsonify(msg="Data not found."), HTTP_404_NOT_FOUND

        elif request.method == "PUT":
            status = request.json.get("status")

            model.status = status
            base.edit()

            return (
                jsonify(
                    msg=f"Data Guru BK {model.guru.first_name} telah diperbaharui."
                ),
                HTTP_200_OK,
            )

        elif request.method == "DELETE":
            base.delete(model)
            return jsonify(msg="Data has been deleted."), HTTP_204_NO_CONTENT


class JadwalMengajar:
    @master.route("jadwal-mengajar/create", endpoint="create-jadwal", methods=["POST"])
    def create():
        # kodeMengajar = "MPL-" + str(time.time()).rsplit(".", 1)[1]
        kodeMengajar = request.json.get("kode_mengajar")
        tahunAjaranId = request.json.get("tahun_ajaran_id")
        semesterId = request.json.get("semeter_id")
        guruId = request.json.get("guru_id")
        mapel_id = request.json.get("mapel_id")
        hariId = request.json.get("hari_id")
        kelasId = request.json.get("kelas_id")
        jamMulai = request.json.get("jam_mulai")
        jamSelesai = request.json.get("jam_selesai")
        jamKe = request.json.get("jam_ke")

        base = BaseModel(
            MengajarModel(
                kodeMengajar=kodeMengajar,
                guruId=guruId,
                hariId=hariId,
                jamMulai=jamMulai,
                jamSelesai=jamSelesai,
                kelasId=kelasId,
                semesterId=semesterId,
                tahunAjaranId=tahunAjaranId,
                mapelId=mapel_id,
                jamKe=jamKe,
            )
        )

        kdMengajar = base.get_one(kode_mengajar=kodeMengajar)
        if kdMengajar:
            return (
                jsonify(
                    msg="Kode Mengajar sudah ada, refresh halaman untuk mendapatkan kode baru"
                ),
                HTTP_409_CONFLICT,
            )
        else:
            base.create()

            return (
                jsonify(
                    msg=f"Data jadwal mengajar dengan koden : {base.model.kode_mengajar} telah di tambahkan"
                ),
                HTTP_201_CREATED,
            )

    @master.route("jadwal-mengajar/get-all", endpoint="get-jadwal")
    def get_all():
        base = BaseModel(MengajarModel)
        model = base.get_all()
        data = []
        for i in model:
            data.append(
                {
                    "id": i.id,
                    "kode_mengajar": i.kode_mengajar,
                    "first_name": i.guru.first_name,
                    "last_name": i.guru.last_name,
                    "mapel": i.mapel.mapel,
                    "jam_ke": i.jam_ke,
                    "hari": i.hari.hari,
                    "jam_mulai": i.jam_mulai,
                    "jam_selesai": i.jam_selesai,
                    "kelas": i.kelas.kelas,
                    "semester": i.semester.semester,
                    "tahun_ajaran": i.tahun_ajaran.th_ajaran,
                }
            )

        return jsonify(data=data), HTTP_200_OK

    @master.route(
        "jadwal-mengajar/get-one/<int:id>",
        endpoint="single-jadwal",
        methods=["GET", "PUT", "DELETE"],
    )
    def get_one(id):
        base = BaseModel(MengajarModel)
        model = base.get_one(id=id)

        if not model:
            return (
                jsonify(msg=f"Data yang maksud tidak ditemukan/belum ada."),
                HTTP_404_NOT_FOUND,
            )

        if request.method == "GET":
            return (
                jsonify(
                    id=model.id,
                    kode_mengajar=model.kode_mengajar,
                    guru_id=model.guru_id,
                    first_name=model.guru.first_name,
                    last_name=model.guru.last_name,
                    mapel=model.mapel.mapel,
                    mapel_id=model.mapel_id,
                    jam_ke=model.jam_ke,
                    hari_id=model.hari_id,
                    hari=model.hari.hari,
                    jam_mulai=model.jam_mulai,
                    jam_selesai=model.jam_selesai,
                    kelas_id=model.kelas_id,
                    kelas=model.kelas.kelas,
                    semester=model.semester.semester,
                    tahun_ajaran=model.tahun_ajaran.th_ajaran,
                ),
                HTTP_200_OK,
            )

        elif request.method == "PUT":
            guruId = request.json.get("guru_id")
            hariId = request.json.get("hari_id")
            mapelId = request.json.get("mapel_id")
            jamMulai = request.json.get("jam_mulai")
            jamSelesai = request.json.get("jam_selesai")
            kelasId = request.json.get("kelas_id")
            # semesterId = request.json.get("semeter_id")
            # tahunAjaranId = request.json.get("tahun_ajaran_id")
            jamKe = request.json.get("jam_ke")

            model.guru_id = guruId
            model.mapel_id = mapelId
            model.hari_id = hariId
            model.jam_mulai = jamMulai
            model.jam_selesai = jamSelesai
            model.kelas_id = kelasId
            # model.semester_id = semesterId
            # model.tahun_ajaran_id = tahunAjaranId
            model.jam_ke = jamKe
            base.edit()

            return (
                jsonify(
                    msg=f"Data jadwal mengajar {model.kode_mengajar} telah diperbaharui."
                ),
                HTTP_200_OK,
            )

        elif request.method == "DELETE":
            base.delete(model)
            return jsonify(msg="Data has been deleted."), HTTP_204_NO_CONTENT


class MonthName:
    @master.get("/month/get-all", endpoint="get-month")
    def get_all():
        base = BaseModel(NamaBulanModel)
        month = base.get_all()

        data = []
        for i in month:
            data.append({"id": i.id, "bulan": i.nama_bulan})
        # for i in month:
        #     data.append(month=i.nama_bulan)

        return jsonify(data), HTTP_200_OK

    @master.route("/month/add", methods=["GET", "POST"])
    def add_month():
        nama_bulan = request.json.get("bulan")

        base = BaseModel(NamaBulanModel(bulan=nama_bulan))
        check_duplicate = base.get_one(nama_bulan=nama_bulan)

        if check_duplicate:
            return (
                jsonify(
                    msg=f"Data nama bulan : {nama_bulan} yang di input sudah ada.!"
                ),
                HTTP_409_CONFLICT,
            )
        else:
            base.create()
            return (
                jsonify(msg=f"Data bulan {nama_bulan} telah berhasil di input."),
                HTTP_201_CREATED,
            )

    @master.route("/month/get-single/<int:id>", methods=["GET", "PUT", "DELETE"])
    def get_single(id):
        base = BaseModel(NamaBulanModel)
        bulan = base.get_one(id=id)

        if request.method == "GET":
            return jsonify(id=bulan.id, bulan=bulan.nama_bulan), HTTP_200_OK

        elif request.method == "PUT":
            nama_bulan = request.json.get("bulan")

            bulan.nama_bulan = nama_bulan
            base.edit()

            return (
                jsonify(msg=f"Data bulan {bulan.nama_bulan} telah diperbaharui.!"),
                HTTP_200_OK,
            )

        elif request.method == "DELETE":
            base.delete(bulan)
            return jsonify(msg=f"Data has been deleted.!"), HTTP_204_NO_CONTENT


class TahunData:
    @master.route("year/get-all")
    def get_all_tahun():
        base = BaseModel(TahunModel)
        tahun = base.get_all()

        data = []
        for i in tahun:
            data.append(
                {
                    "id": i.id,
                    "tahun": i.tahun,
                    "status": i.status,
                }
            )

        return jsonify(data), HTTP_200_OK

    @master.route("year/add", methods=["GET", "POST"])
    def add_tahun():
        tahun = request.json.get("tahun")
        status = request.json.get("status")

        base = BaseModel(TahunModel(tahun=tahun, status=status))
        check_year = base.get_one(tahun=tahun)
        if check_year:
            return (
                jsonify(
                    msg=f"Data tahun {tahun} telah ada dalam database, silah input tahun lainnya."
                ),
                HTTP_409_CONFLICT,
            )
        else:
            base.create()

            return (
                jsonify(
                    msg=f'Data tahun {base.model.tahun}, dengan status {"aktif" if base.model.status =="1" else "tidak aktif"} telah ditambahkan.!'
                ),
                HTTP_201_CREATED,
            )

    @master.route("year/get-single/<int:id>", methods=["GET", "PUT", "DELETE"])
    def get_single_tahun(id):
        base = BaseModel(TahunModel)
        sql = base.get_one(id=id)

        if sql:
            if request.method == "GET":
                return (
                    jsonify(id=sql.id, tahun=sql.tahun, status=sql.status),
                    HTTP_200_OK,
                )
            elif request.method == "PUT":
                status = request.json.get("status")
                sql.status = status

                base.edit()

                return (
                    jsonify(msg=f"Status tahun {sql.tahun} telah diperbaharui!"),
                    HTTP_200_OK,
                )
            elif request.method == "DELETE":
                base.delete(sql)
                return jsonify(msg="Data has been deleted!"), HTTP_204_NO_CONTENT
        else:
            return (
                jsonify(
                    msg=f"Data dengan ID yang dimaksud tidak ditemukan dalam database!"
                ),
                HTTP_404_NOT_FOUND,
            )
