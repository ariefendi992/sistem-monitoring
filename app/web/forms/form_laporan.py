from flask_wtf import FlaskForm
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms_sqlalchemy.orm import validators
from app.models.master_model import KelasModel


class FormLaporanPelanggaran(FlaskForm):
    attr = {"hx-get": "/guru-bk/get-siswa", "hx-target": "#siswa"}
    kelas = QuerySelectField(
        "Kelas",
        query_factory=lambda: KelasModel.query.all(),
        allow_blank=True,
        blank_text="- Pilih -",
        get_label="kelas",
        validators=[validators.DataRequired("* Pilihan tidak boleh kosong!")],
        render_kw=attr,
    )

    siswa = QuerySelectField("Nama Siswa", allow_blank=True, blank_text="- Pilih -")
