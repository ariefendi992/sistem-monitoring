from app.extensions import db
import sqlalchemy as sa
from .master_model import *
from sqlalchemy.orm import backref, relationship


class AdminModel(db.Model):
    __tablename__ = "detail_admin"
    id = sa.Column(sa.Integer, primary_key=True)
    first_name = sa.Column(sa.String(128), nullable=False, default="")
    last_name = sa.Column(sa.String(128), nullable=False, default="")
    gender = sa.Column(sa.String(32), nullable=True)
    alamat = sa.Column(sa.String(128), nullable=True)
    telp = db.Column(db.String(20), nullable=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey("auth_user.id", ondelete="CASCADE"))
    user = db.relationship("UserModel", back_populates="admins")

    def __init__(
        self,
        first_name: str | None = None,
        last_name: str | None = None,
        gender: str | None = None,
        alamat: str | None = None,
        telp: str | int | None = None,
        user: str | None = None,
    ) -> str:
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.alamat = alamat
        self.telp = telp
        self.user = user

        # self.user_id = user_id


class SiswaModel(db.Model):
    __tablename__ = "detail_siswa"
    id = sa.Column(sa.Integer, primary_key=True)
    first_name = sa.Column(sa.String(128), nullable=False, default="")
    last_name = sa.Column(sa.String(128), nullable=False, default="")
    gender = sa.Column(sa.String(32), nullable=False)
    tempat_lahir = sa.Column(sa.String(128), nullable=True)
    tgl_lahir = sa.Column(sa.Date(), nullable=True)
    agama = sa.Column(sa.String(128), nullable=False, default=None)
    nama_ortu_or_wali = sa.Column(sa.String(128), nullable=True)
    no_telp = sa.Column(sa.String(16), nullable=True)
    alamat = sa.Column(sa.String(250), nullable=True)
    qr_code = sa.Column(sa.Text(), nullable=True)
    pic: str | None = sa.Column(sa.Text(), nullable=True)
    id_card: str = sa.Column(sa.String(128), nullable=True)
    user_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("auth_user.id", ondelete="CASCADE", onupdate="CASCADE"),
    )
    user = relationship(
        "UserModel", backref=backref("user_siswa", cascade="all, delete-orphan")
    )
    kelas_id = sa.Column(sa.Integer, sa.ForeignKey("master_kelas.id"))
    kelas = relationship("KelasModel", backref="class_siswa")

    def __init__(
        self,
        first_name=None,
        last_name=None,
        gender=None,
        tempat_lahir=None,
        tgl_lahir=None,
        agama=None,
        nama_ortu=None,
        telp=None,
        alamat=None,
        kelas_id=None,
        user_id=None,
        kelas=None,
        pic=None,
    ) -> None:
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.tempat_lahir = tempat_lahir
        self.tgl_lahir = tgl_lahir
        self.agama = agama
        self.nama_ortu_or_wali = nama_ortu
        self.no_telp = telp
        self.alamat = alamat
        self.user_id = user_id
        self.kelas_id = kelas
        self.pic = pic
        self.kelas_id = kelas_id

    def __repr__(self):
        return f"{self.first_name.title()} {self.last_name.title()}"

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def getAll(cls):
        return cls.query.order_by(cls.kelas_id.asc(), cls.first_name.asc()).all()

    @classmethod
    def get_filter_by(cls, **filter):
        return cls.query.filter_by(**filter).first()

    def commit():
        db.session.commit()


class GuruModel(db.Model):
    __tablename__ = "detail_guru"
    id = sa.Column(sa.Integer, primary_key=True)
    first_name = sa.Column(sa.String(128), nullable=False, default="")
    last_name = sa.Column(sa.String(128), nullable=False, default="")
    gender = sa.Column(sa.String(32), nullable=False)
    agama = sa.Column(sa.String(32), nullable=True)
    alamat = sa.Column(sa.String(256), nullable=True)
    telp = sa.Column(sa.String(16), nullable=True)
    user_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("auth_user.id", ondelete="CASCADE", onupdate="CASCADE"),
    )
    user = relationship(
        "UserModel", backref=backref("user_guru", cascade="all, delete-orphan")
    )

    def __init__(
        self,
        first_name=None,
        last_name=None,
        gender=None,
        alamat=None,
        agama=None,
        telp=None,
        user_id=None,
    ) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.alamat = alamat
        self.agama = agama
        self.telp = telp
        self.user_id = user_id

    def __str__(self) -> str:
        return f"{self.first_name.title()} {self.last_name.title()}"

    @classmethod
    def get_all(cls):
        data = cls.query.all()
        return data
    
    @classmethod
    def get_all_filter(cls, *filter):
        db.session.query(cls).filter(*filter).all()
