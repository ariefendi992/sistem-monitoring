from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import ValidationError


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
