from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from app.lib.db_statement import DBStatement
from app.models.user_model import UserModel

dbs = DBStatement()


class FormTambahAdmin(FlaskForm):
    """AI is creating summary for FormTambahAdmin

    Args:
        FlaskForm ([type]): [description]

    Raises:
        ValidationError: [description]
        ValidationError: [description]
        ValidationError: [description]
    """

    username = StringField(
        "Username",
        validators=[DataRequired("* Username harus diisi.")],
        render_kw={"required": False},
        description="Username Admin",
    )
    password = PasswordField("Password")
    group = StringField("Group", default="admin", render_kw=dict(disabled=True))
    fullname = StringField(
        "Nama Lengkap",
        validators=[DataRequired("* Nama harus diisi.")],
        render_kw=dict(required=False),
    )
    gender = SelectField(
        "Jenis Kelamin",
        choices=[
            ("", "- Pilih -"),
            ("laki-laki", "Laki-Laki"),
            ("perempuan", "Perempuan"),
        ],
        validators=[DataRequired("* Pilihan tidak bleh kosong!")],
        render_kw={"required": False},
    )

    alamat = StringField("Alamat", render_kw={"class": "form-control form-control-sm"})
    telp = StringField("Telp/Hp", render_kw={"class": "form-control form-control-sm"})

    def validate_username(self, field):
        checkUsername = dbs.get_one(UserModel, username=field.data)
        if checkUsername:
            raise ValidationError("* Username sudah ada!")

    def validate_password(self, field):
        if field.data == "":
            raise ValidationError("* Password harus diisi.")
        elif len(field.data) <= 6:
            raise ValidationError("* Jumlah karakter mininal 6")


class FormEditAdmin(FlaskForm):
    """AI is creating summary for FormEditAdmin

    Args:
        FlaskForm ([type]): [description]

    Raises:
        ValidationError: [description]
        ValidationError: [description]
        ValidationError: [description]
    """

    username = StringField(
        "Username",
        validators=[DataRequired("* Username harus diisi.")],
        render_kw={"required": False, "disabled": True},
        description="Username Admin",
    )
    # password = PasswordField("Password")
    # group = StringField("Group", default="admin", render_kw=dict(disabled=True))
    fullname = StringField(
        "Nama Lengkap",
        validators=[DataRequired("* Nama harus diisi.")],
        render_kw=dict(required=False),
    )
    gender = SelectField(
        "Jenis Kelamin",
        choices=[
            ("", "- Pilih -"),
            ("laki-laki", "Laki-Laki"),
            ("perempuan", "Perempuan"),
        ],
        validators=[DataRequired("* Pilihan tidak bleh kosong!")],
        render_kw={"required": False},
    )
    alamat = StringField(
        "Alamat",
        validators=[DataRequired("* Alamat harus diisi.")],
        render_kw={"class": "form-control form-control-sm", "required": False},
    )
    telp = StringField(
        "Telp/Hp",
        validators=[DataRequired("* Telp/HP harus diisi.")],
        render_kw={"class": "form-control form-control-sm", "required": False},
    )
    submit = SubmitField("Tambah Data")
    submit2 = SubmitField("Perbaharui Data")
    cancel = SubmitField("Batal")

    # def validate_username(self, field):
    #     checkUsername = dbs.get_one(UserModel, username=field.data)
    #     if checkUsername:
    #         raise ValidationError("* Username sudah ada!")

    # def validate_password(self, field):
    #     if field.data == "":
    #         raise ValidationError("* Password harus diisi.")
    #     elif len(field.data) <= 6:
    #         raise ValidationError("* Jumlah karakter mininal 6")


class FormUpdatePasswordAmdin(FlaskForm):
    password = PasswordField("Password")
    submit = SubmitField("Update Pasword")

    def validate_password(self, field):
        if field.data == "":
            raise ValidationError("*Password tidak boleh kosong!")
        elif len(field.data) < 6:
            raise ValidationError("*Panjang mininal 6 karakter")
