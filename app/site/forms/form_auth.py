from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, StringField, SelectField, BooleanField
from wtforms.validators import ValidationError


class FormEditStatus(FlaskForm):
    state = SubmitField("Aktif")


class FormEditPassword(FlaskForm):
    kataSandi = PasswordField("Password")
    submit = SubmitField("Save Changes")

    def validate_kataSandi(self, field):
        if field.data == None:
            raise ValidationError("*Password tidak boleh kosong.")
        elif len(field.data) < 6:
            raise ValidationError("*Password minimal 6 karakter.")


class FormLogin(FlaskForm):
    username = StringField("Nama Pengguna")
    password = PasswordField("Kata Sandi")
    level = SelectField(
        "Level Pengguna",
        choices=[
            ("", "- Pilih -"),
            ("admin", "Admin"),
            ("guru", "Guru Mata Pelajaran"),
            ("bk", "Guru BK"),
        ],
    )
    remember = BooleanField("Remember Me")
    submit = SubmitField("Masuk")

    def validate_username(self, field):
        if field.data == "":
            raise ValidationError("*Username harap di isi!")

    def validate_password(self, field):
        if len(field.data) < 6 and len(field.data) > 0:
            raise ValidationError("*Jumlah karakter minimal 6 digit!")
        elif field.data == "":
            raise ValidationError("*Form Kata Sandi Tidak Boleh Kosong!")

    def validate_level(self, field):
        if field.data == "":
            raise ValidationError("*Pilih Level Pengguna Terlebih dahulu!")
