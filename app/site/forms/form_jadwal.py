from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SelectField, SubmitField
from wtforms.validators import ValidationError


class FormJadwalMengajar(FlaskForm):
    kode = StringField("Kode Mengajar")
    tahunAjaran = StringField("Tahun Ajaran")
    ta = HiddenField()
    semester = StringField("Semester")
    sms = HiddenField()
    namaGuru = SelectField("Guru Mata Pelajaran", choices=[("", "- Pilih -")])
    namaMapel = SelectField("Mata Pelajaran", choices=[("", "- Pilih -")])
    hari = SelectField("Hari", choices=[("", "- Pilih -")])
    kelas = SelectField("Kelas", choices=[("", "- Pilih -")])
    # waktuMulai = SelectField("Waktu Mulai", choices=[("", "- Pilih -")])
    # waktuSelesai = SelectField("Waktu Selesai", choices=[("", "- Pilih -")])
    waktuMulai2 = StringField("Waktu Mulai")
    waktuSelesai2 = StringField("Waktu Selesai")
    jamKe = StringField("Jam-Ke")
    submit = SubmitField("Submit Data")

    def validate_namaGuru(self, field):
        if field.data == "":
            raise ValidationError("** Harap pilih guru terlebih dahulu")

    def validate_namaMapel(self, field):
        if field.data == "":
            raise ValidationError("** Harap pilih mata pelajaran terlebih dahulu")

    def validate_hari(self, field):
        if field.data == "":
            raise ValidationError("** Harap pilih hari terlebih dahulu")

    def validate_kelas(self, field):
        if field.data == "":
            raise ValidationError("** Harap pilih kelas terlebih dahulu")

    # def validate_waktuMulai(self, field):
    #     if field.data == "":
    #         raise ValidationError("** Harap pilih waktu terlebih dahulu")

    # def validate_waktuSelesai(self, field):
    #     if field.data == "":
    #         raise ValidationError("** Harap pilih waktu terlebih dahulu")

    def validate_waktuMulai2(self, field):
        if field.data == "":
            raise ValidationError("** Harap di isi terlebih dahulu")

    def validate_waktuSelesai2(self, field):
        if field.data == "":
            raise ValidationError("** Harap di isi terlebih dahulu")

    def validate_jamKe(self, field):
        if field.data == "":
            raise ValidationError("** Harap di isi inputan jam-ke terlebih dahulu")
