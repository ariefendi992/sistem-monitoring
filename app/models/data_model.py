from app.extensions import db
import sqlalchemy as sa
import sqlalchemy.orm as sql
from sqlalchemy.orm import backref
from app.models.master_model import *
from datetime import datetime
from sqlalchemy import Integer, String, ForeignKey, Column, Text, true
from sqlalchemy.orm import relationship
from app.models.user_details_model import GuruModel
import typing as t


class AbsensiModel(db.Model):
    __tablename__ = "data_absensi"
    id = sa.Column(sa.Integer, primary_key=True)
    mengajar_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(
            "master_jadwal_mengajar.id", onupdate="CASCADE", ondelete="CASCADE"
        ),
    )
    mengajar = sql.relationship(
        "MengajarModel", backref=backref("mengajar_guru", cascade="all, delete-orphan")
    )
    siswa_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("detail_siswa.user_id", ondelete="CASCADE", onupdate="CASCADE"),
    )
    siswa = sql.relationship("SiswaModel", backref="data_siswa")
    tgl_absen = sa.Column(sa.Date)
    ket = sa.Column(sa.String(16), nullable=True)
    # pertemuan_ke = sa.Column(sa.String(2), nullable=True)

    def __init__(self, mengajar_id=None, siswa_id=None, tgl_absen=None, ket=None):
        self.mengajar_id = mengajar_id
        self.siswa_id = siswa_id
        self.tgl_absen = tgl_absen
        self.ket = ket
        # self.pertemuan_ke = pertemuan

    def __repr__(self):
        return "{}".format(self.ket)


class PelanggaranModel(db.Model):
    __tablename__ = "data_pelanggaran"
    id = sa.Column(sa.Integer, primary_key=True)
    siswa_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("detail_siswa.user_id", ondelete="CASCADE", onupdate="CASCADE"),
    )
    siswa = sql.relationship("SiswaModel", backref="siswa_melanggar")
    jenis_pelanggaran_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(
            "data_jenis_pelanggaran.id", onupdate="CASCADE", ondelete="CASCADE"
        ),
    )
    jenis_pelanggaran = sql.relationship(
        "JenisPelanggaranModel2", backref="jenisPelanggaran"
    )
    guru_id = sa.Column(sa.ForeignKey("detail_guru.user_id"))
    guru = relationship("GuruModel", backref="pelanggaran")
    note = sa.Column(sa.Text(), nullable=True)
    tgl_report = sa.Column(sa.Date, nullable=False)
    status = sa.Column(sa.String(128), nullable=True)
    # pembinaan = relationship(
    #     "PembinaanModel",
    #     back_populates="pelanggaran",
    # )

    def __init__(
        self,
        siswaId: int,
        pelapor_id: int,
        jenisPelanggaran_id: int,
        note: str = None,
        status: str = None,
    ):
        self.siswa_id = siswaId
        self.jenis_pelanggaran_id = jenisPelanggaran_id
        self.guru_id = pelapor_id
        self.note = note
        self.tgl_report = datetime.date(datetime.today())
        self.status = status

    def __repr__(self):
        return self.pelapor


class JenisPelanggaranModel2(db.Model):
    __tablename__ = "data_jenis_pelanggaran"
    id = Column(Integer, primary_key=True)
    jenis_pelanggaran = Column(sa.Text())
    status = Column(String(64), nullable=True)

    def __init__(self, jenisPelanggaran: str, status: str = "1") -> str:
        self.jenis_pelanggaran = jenisPelanggaran
        self.status = status

    def __repr__(self):
        return f"ID Jenis Pelanggaran2 : {self.id}"

    def fetchAll():
        query = JenisPelanggaranModel2.query.all()

        return query

    def fetchOne(id: int) -> int:
        query = JenisPelanggaranModel2.query.filter_by(id=id).first()
        return query


class PembinaanModel(db.Model):
    """Spesifikasi Penggunaan

    -  Gunakan datetime.data() untuk tgl_bina dana tgl_evaluasi
        Contoh:
            t = PembinaanModel(user_id=1, bina=1, evalusai = 0, tgl_evaluasi=datetime.date(datetime.today()))


    """

    __tablename__ = "data_pembinaan"
    id = sa.Column(sa.Integer, primary_key=True)
    bina = sa.Column(sa.Integer)
    tgl_bina = sa.Column(sa.Date, nullable=True)
    pelanggaran_id = sa.Column(
        sa.ForeignKey("data_pelanggaran.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    pelanggaran = db.relationship(
        "PelanggaranModel",
        backref="pembinaan",
    )
    siswa_id = db.Column(
        sa.ForeignKey("detail_siswa.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    siswa = db.relationship("SiswaModel", backref="pembinaan")
    status = db.Column(db.String(2))

    def __init__(
        self,
        bina: int,
        pelanggaran_id: int,
        siswa_id: int,
        status: str,
        tgl_bina: datetime,
    ) -> str:
        self.bina = bina
        self.pelanggaran_id = pelanggaran_id
        self.siswa_id = siswa_id
        # self.tgl_bina = datetime.date(datetime.today())
        self.tgl_bina = tgl_bina
        self.status = status

    def __repr__(self):
        data = f"id : {self.id}"
        return data


class TataTertibModel(db.Model):
    __tablename__ = "data_tata_tertib"
    id = db.Column(db.Integer, primary_key=True)
    tata_tertib = db.Column(db.String(255))
    status = db.Column(db.String(16), nullable=True)

    def __init__(
        self,
        tata_tertib: str = None,
    ) -> str:
        self.tata_tertib = tata_tertib

    def __repr__(self) -> str:
        return f"id : {self.id}"
