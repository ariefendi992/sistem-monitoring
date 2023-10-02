from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from app.extensions import db
from app.lib.date_time import utc_makassar


class NotifikasiSiswaModel(db.Model):
    __tablename__ = "data_notifikasi_siswa"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("detail_siswa.user_id"))
    msg = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=utc_makassar())

    def __init__(self, userID: int, msg: str) -> str:
        self.user_id = userID
        self.msg = msg
