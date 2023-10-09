from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, StringField, SelectField, BooleanField
from wtforms.validators import ValidationError


class FormEditStatus(FlaskForm):
    state = SubmitField("Aktif")


class FormEditPassword(FlaskForm):
    kataSandi = PasswordField("Kata Sandi")
    submit = SubmitField("Perbaharui Data")

    def validate_kataSandi(self, field):
        if field.data == None:
            raise ValidationError("*Kata sandi tidak boleh kosong.")
        elif len(field.data) < 6:
            raise ValidationError("*Kata sandi minimal 6 karakter.")


class FormLogin(FlaskForm):
    username = StringField("Nama Pengguna")
    password = PasswordField("Kata Sandi")
    level = SelectField(
        "Nama Pengguna",
        choices=[
            ("", "- Pilih -"),
            ("admin", "Admin"),
            ("guru", "Guru Mata Pelajaran"),
            ("bk", "Guru BK"),
        ],
    )
    remember = BooleanField("Ingat Saya?")
    submit = SubmitField("Masuk")

    def validate_username(self, field):
        if field.data == "":
            raise ValidationError("*Nama pengguna harap di isi!")

    def validate_password(self, field):
        if len(field.data) < 6 and len(field.data) > 0:
            raise ValidationError("*Jumlah karakter minimal 6 digit!")
        elif field.data == "":
            raise ValidationError("*Kata Sandi Tidak Boleh Kosong!")

    def validate_level(self, field):
        if field.data == "":
            raise ValidationError("*Pilih Tipe Pengguna Terlebih dahulu!")
