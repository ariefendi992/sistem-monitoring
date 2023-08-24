from flask_wtf import FlaskForm
from sqlalchemy import func
from wtforms import SelectField
from wtforms.validators import ValidationError, DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField
from app.lib.date_time import nama_bulan
from app.models.data_model import AbsensiModel


from app.models.master_model import KelasModel, NamaBulanModel


class FormSelectKelas(FlaskForm):
    kelas = SelectField(label="Pilih Kelas", choices=[("", "- Pilih -")])

    def validate_kelas(self, field):
        if field.data == "":
            raise ValidationError("*Harap pilih kelas")


class FormSelectKehadiranSiswa(FlaskForm):
    kelas = SelectField("Pilih Kelas", choices=[("", "- Pilih -")])
    bulan = SelectField("Pilih Bulan", choices=[("", "- Pilih -")])
    tahun = SelectField("Pilih Tahun", choices=[("", "- Pilih -")])

    def validate_kelas(self, field):
        if field.data == "":
            raise ValidationError("*Harap pilih kelas")

    def validate_bulan(self, field):
        if field.data == "":
            raise ValidationError("*Harap Pilih Bulan")

    def validate_tahun(self, field):
        if field.data == "":
            raise ValidationError("*Harap Pilih Tahun")


class FormRekapAbsenWali(FlaskForm):
    bulan = SelectField(label="*Pilih Bulan", choices=[("", "- Pilih -")])
    tahun = SelectField(label="*Pilih Tahun", choices=[("", "- Pilih -")])

    def validate_bulan(self, field):
        if field.data == "":
            raise ValidationError("* Harap Pilih Bulan!")

    def validate_tahun(self, field):
        if field.data == "":
            raise ValidationError("* Harap Pilih Tahun!")


class FormSelectMapel(FlaskForm):
    mapel = SelectField(label="Pilih Mata Pelajaran", choices=[("", "- Pilih -")])
    bulan = SelectField(label="Pilih Bulan", choices=[("", "- Pilih -")])
    tahun = SelectField(label="Pilih Tahun", choices=[("", "- Pilih -")])

    def validate_mapel(self, field):
        if field.data == "" or field.data == None:
            raise ValidationError(f"* Harap {field.label.text}!")

    def validate_bulan(self, field):
        if field.data == "" or field.data == None:
            raise ValidationError(f"* Harap {field.label.text}!")

    def validate_tahun(self, field):
        if field.data == "" or field.data == None:
            raise ValidationError(f"* Harap {field.label.text}!")


class FormRekapAbsen(FlaskForm):
    kelas = QuerySelectField(
        "Kelas",
        query_factory=lambda: KelasModel.query.all(),
        allow_blank=True,
        blank_text="- Pilih -",
        validators=[DataRequired(message="Pilihan tidak boleh kosong.")],
    )

    bulan = QuerySelectField(
        "Nama Bulan",
        query_factory=lambda: NamaBulanModel.query.all(),
        allow_blank=True,
        blank_text="- Pilih -",
        validators=[DataRequired(message="Pilihan tidak boleh kosong.")],
    )

    tahun = QuerySelectField(
        "Tahun",
        query_factory=lambda: AbsensiModel.query.group_by(
            func.year(AbsensiModel.tgl_absen)
        ).all(),
        allow_blank=True,
        blank_text="- Pilih -",
        get_label="tgl_absen.year",
        validators=[DataRequired(message="Pilihan tidak boleh kosong.")],
    )
