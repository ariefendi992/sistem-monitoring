from flask import Blueprint, make_response, request, jsonify
from app.lib.status_code import *
from app.extensions import db
from app.models.master_model import MengajarModel

jadwal = Blueprint("jadwal", __name__, url_prefix="/api/v2/jadwal-belajar/")


@jadwal.get("by-kelas/<int:kelasId>")
def jadwal_belajar(kelasId):
    sql_jadwal = (
        db.session.query(MengajarModel)
        .filter_by(kelas_id=kelasId)
        .order_by(MengajarModel.hari_id)
        .all()
    )

    data = []
    for i in sql_jadwal:
        data.append(
            {
                "id": i.id,
                "kelas_id": i.kelas_id,
                "mapel": i.mapel.mapel,
                "hari": i.hari.hari,
            }
        )
    response = make_response(jsonify(data))

    return response, HTTP_200_OK
