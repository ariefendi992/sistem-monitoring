from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    StringField,
    HiddenField,
    DateField,
    SubmitField,
    SelectField,
)
from wtforms.validators import ValidationError


class AbsensiForm(FlaskForm):
    name = StringField("Nama")
    id = HiddenField("User ID")
    pertemuan = HiddenField("Pertemuan")
    today = DateField("Tanggal")
    ket = BooleanField("")
    submit = SubmitField("Selesai")


class FormSelectAbsensi(FlaskForm):
    kelas = SelectField(label="Pilih Kelas", choices=[("", "- Pilih -")])
    bulan = SelectField(label="Pilih Bulan", choices=[("", "- Pilih -")])
    tahun = SelectField(label="Pilih Tahun", choices=[("", "- Pilih -")])

    def validate_kelas(self, field):
        if field.data == "":
            raise ValidationError("*Harap pilih kelas")

    def validate_bulan(self, field):
        if field.data == "":
            raise ValidationError("*Harap pilih bulan")

    def validate_tahun(self, field):
        if field.data == "":
            raise ValidationError("*Harap pilih tahun")


class FormSelectKehadiranSemester(FlaskForm):
    kelas = SelectField(label="Pilih Kelas", choices=[("", "- Pilih -")])
    semester = SelectField(label="Pilih Semester", choices=[("", "- Pilih -")])
    submit = SubmitField(label="Lihat Data")

    def validate_kelas(self, field):
        if field.data == "":
            raise ValidationError("*Harap pilih kelas")

    def validate_semester(self, field):
        if field.data == "":
            raise ValidationError("*Harap pilih semester")
