from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField
from wtforms.validators import ValidationError


class FormAddGuru(FlaskForm):
    username = StringField(label="NIP")
    password = PasswordField(label="Password")
    tipe = StringField(label="Group")
    fullname = StringField(label="Nama Lengkap")
    jenisKelamin = SelectField(
        label="Jenis Kelamin",
        choices=[
            ("", "- Pilih -"),
            ("laki-laki", "Laki-laki"),
            ("perempuan", "Perempuan"),
        ],
    )
    agama = SelectField(
        label="Agama",
        choices=[
            ("", "- Pilih -"),
            ("islam", "Islam"),
            ("kristen", "Kristen"),
            ("katolik", "Katolik"),
            ("hindu", "Hindu"),
            ("budha", "Budha"),
        ],
    )
    alamat = StringField(label="Alamat")
    telp = StringField(label="No. Telp")
    submit = SubmitField(label="Submit Data")

    def validate_username(self, field):
        if field.data == "":
            raise ValidationError("*Input NIP tidak boleh kosong.")

    def validate_password(self, field):
        if field.data == "":
            raise ValidationError("*Input Password tidak boleh kosong.")

    def validate_fullname(self, field):
        if field.data == "":
            raise ValidationError("*Input Nama tidak boleh kosong.")

    def validate_jenisKelamin(self, field):
        if field.data == "":
            raise ValidationError("*Pilihan Jenis Kelamin tidak boleh kosong.")

    def validate_agama(self, field):
        if field.data == "":
            raise ValidationError("*Pilihan Agama tidak boleh kosong.")


class FormEditGuru(FlaskForm):
    nip = StringField("NIP")
    fullname = StringField("Nama Lengkap")
    jenisKelamin = SelectField(
        "Jenis Kelamin",
        choices=[
            ("_", "- Pilih -"),
            ("laki-laki", "Laki-Laki"),
            ("perempuan", "Perempuan"),
        ],
    )
    agama = SelectField(
        label="Agama",
        choices=[
            ("", "- Pilih -"),
            ("islam", "Islam"),
            ("kristen", "Kristen"),
            ("katolik", "Katolik"),
            ("hindu", "Hindu"),
            ("budha", "Budha"),
        ],
    )
    alamat = StringField("Alamat")
    telp = StringField("Telp")
    submit = SubmitField("Save Changes")


class FormGetProfileGuru(FlaskForm):
    nip = StringField("NIP")
    fullname = StringField("Nama Lengkap")
    gender = SelectField(
        "Jenis Kelamin",
        choices=[
            ("_", "- Pilih -"),
            ("laki-laki", "Laki-Laki"),
            ("perempuan", "Perempuan"),
        ],
    )
    agama = SelectField(
        label="Agama",
        choices=[
            ("", "- Pilih -"),
            ("islam", "Islam"),
            ("kristen", "Kristen"),
            ("katolik", "Katolik"),
            ("hindu", "Hindu"),
            ("budha", "Budha"),
        ],
    )
    alamat = StringField("Alamat")
    telp = StringField("Telp")
    submit = SubmitField("Submit Data")
    submit2 = SubmitField("Ubah Data")
    cancel = SubmitField("Cancel")


class FormUpdatePassword(FlaskForm):
    password = PasswordField("Password Baru")
    submit = SubmitField("Ganti Password")

    def validate_password(self, field):
        if field.data == "":
            raise ValidationError("** Password tidak boleh kosong.!")
        if len(field.data) <= 6:
            raise ValidationError(
                "** Panjang karakter password minimal 6 digit atau karakter.!"
            )
