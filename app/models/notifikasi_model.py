from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from app.extensions import db
from app.lib.date_time import utc_makassar


class NotifikasiSiswaModel(db.Model):
    __tablename__ = "data_notifikasi_siswa"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("detail_siswa.user_id"))
    msg = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=utc_makassar())

    def __init__(self, userID: int, msg: str | None) -> str:
        self.user_id = userID
        self.msg = msg

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_all_filter_by(cls, user_id: int):
        return db.session.query(cls).filter_by(user_id=user_id).all()

    @classmethod
    def get_one_filter_by(cls, user_id):
        return db.session.query(cls).filter_by(user_id=user_id).first()
