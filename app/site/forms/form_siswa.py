from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, DateField
from wtforms.validators import ValidationError
# from wtforms.fields import DateField

class FormAddSiswa(FlaskForm):
    username = StringField(label="NISN")
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
    tempatLahir = StringField(label='Tempat Lahir')
    tanggalLahir = DateField(label='Tanggal Lahir')
    namaOrtu = StringField(label='Nama Orang Tua')
    telp = StringField(label='No. Telp')    
    alamat = StringField(label='Alamat')
    kelas = SelectField(label="Kelas")
    submit = SubmitField(label="Submit Data")

    def validate_username(self, field):
        if len(field.data) == 0:
            raise ValidationError("*Username tidak boleh kosong..!")

    def validate_password(self, field):
        if len(field.data) == 0:
            raise ValidationError("*Password tidak boleh kosong..!")
        elif len(field.data) < 6:
            raise ValidationError("*Jumlah karakter minimal 6")

    def validate_fullname(self, field):
        if len(field.data) == 0:
            raise ValidationError("*Nama tidak boleh kosong..!")

    def validate_jenisKelamin(self, field):
        if field.data == "":
            raise ValidationError("*Pilih jenis kelamin..!")

    def validate_agama(self, field):
        if field.data == "":
            raise ValidationError("*Pilih agama..!")

    def validate_kelas(self, field):
        if field.data == "":
            raise ValidationError("*Pilih kelas..!")


class FormEditSiswa(FlaskForm):
    nisn = StringField("NISN")
    fullname = StringField("Nama Lengkap")
    kelas = SelectField("Kelas")
    # kelas = SelectField("Kelas", choices=[("", "- Pilih -")])
    jenisKelamin = SelectField(
        "Jenis Kelamin",
        choices=[
            ("","- Pilih -"),
            ("laki-laki", "Laki-Laki"),
            ("perempuan", "Perempuan"),
        ],
    )
    tempatLahir = StringField('Tempat Lahir')
    tanggalLahir= DateField('Tanggal Lahir')
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
    alamat = StringField('Alamat')
    namaOrtu = StringField('Nama Orang Tua/Wali')
    telp = StringField('No. Telp')
    submit = SubmitField('Save Changes')

