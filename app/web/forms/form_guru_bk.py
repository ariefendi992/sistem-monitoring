from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, data_required
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms_sqlalchemy.orm import validators
from app.models.data_model import JenisPelanggaranModel2, TataTertibModel
from app.models.user_details_model import GuruModel


class FormTambahPelanggar(FlaskForm):
    kelas = SelectField(label="Nama Kelas ", choices=[("", "- Pilih -")])
    siswa = SelectField(
        label="Nama Siswa", choices=[("", "- Pilih -")], validate_choice=False
    )
    jenisPelanggaran = SelectField(
        label="Jenis Pelanggaran", choices=[("", "- Pilih -")]
    )
    pelapor = QuerySelectField(
        label="Pelapor",
        query_factory=lambda: GuruModel.query.all(),
        allow_blank=True,
        blank_text="- Pilih",
        validators=[validators.DataRequired("*Pelapor wajib dipilih.")],
    )
    catatan = TextAreaField(
        label="Catatan",
        validators=[data_required("*Catatan wajib diisi.")],
        render_kw=dict(required=False),
    )

    def validate_kelas(self, field):
        if field.data == "":
            raise ValidationError("*kelas wajib dipilih.")

    def validate_siswa(self, field):
        if field.data == "":
            raise ValidationError("*Nama Siswa wajib dipilih.")

    def validate_jenisPelanggaran(self, field):
        if field.data == "":
            raise ValidationError("*Jenis Pelanggaran wajib dipilih.")


class FormEditPelanggar(FlaskForm):
    siswa = StringField(label="Nama Siswa")
    jenisPelanggaran = SelectField(
        label="Pilih Jenis Pelanggaran", choices=[("", "- Pilih -")]
    )
    keterangan = TextAreaField(label="Keterangan")
    submit = SubmitField(label="Submit")


class FormJenisPelanggaran(FlaskForm):
    jenisPelanggaran = TextAreaField(label="Jenis Pelanggaran")
    status = SelectField(
        label="Status",
        choices=[("", "- Pilih -"), ("1", "Aktif"), ("0", "Tidak Aktif")],
    )
    submit = SubmitField(label="Submit")

    def validate_jenisPelanggaran(self, field):
        if field.data == "":
            raise ValidationError(f"*Jenis Pelanggaran wajib diisi.")

        data = JenisPelanggaranModel2.query.filter_by(
            jenis_pelanggaran=self.jenisPelanggaran.data
        ).first()

        if data:
            raise ValidationError(
                f"* {self.jenisPelanggaran.data.capitalize()} sudah ada!"
            )


class FormEditJenisPelanggaran(FlaskForm):
    jenisPelanggaran = TextAreaField(label="Jenis Pelanggaran")
    status = SelectField(
        label="Status",
        choices=[("", "- Pilih -"), ("1", "Aktif"), ("0", "Tidak Aktif")],
    )
    submit = SubmitField(label="Submit")

    # def validate_jenisPelanggaran(self, field):
    #     if field.data == "":
    #         raise ValidationError(
    #             f"*{self.jenisPelanggaran.label.text} tidak boleh kosong!"
    #         )

    #     elif len(field.data) < 10:
    #         raise ValidationError("*Silahkan input data dengan benar!")


class FormTambahTTertib(FlaskForm):
    tataTertib = TextAreaField(label="Tata tertib")
    submit = SubmitField(label="Submit")

    def validate_tataTertib(self, field: str) -> str:
        if field.data == "":
            raise ValidationError("*Form tata-tertib wajib  diisi!")

        data = TataTertibModel.query.filter_by(tata_tertib=field.data).first()
        
        if data:
            raise ValidationError('*Data tata tertib sudah ada.')

        

class FormEditTTertib(FlaskForm):
    pilihTTertib = SelectField(label="Pilih Tata Tertib", choices=[("", "- Pilih -")])
    tataTertib = TextAreaField(label="Tata tertib")
    submit = SubmitField(label="Submit")

    def validate_pilihTTertib(self, field: str) -> str:
        if field.data == "":
            raise ValidationError("*Pilih terlebih dahulu! form tidak boleh kosong!")

    def validate_tataTertib(self, field: str) -> str:
        if field.data == "":
            raise ValidationError("*Tata tertib tidak boleh kosong!")


