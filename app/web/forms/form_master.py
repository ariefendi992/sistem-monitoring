from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import ValidationError

from app.models.master_model import KelasModel


class FormMapel(FlaskForm):
    mapel = StringField(label="Nama Mata Pelajaran")
    submit = SubmitField(label="Tambah Data")

    def validate_mapel(self, field):
        if len(field.data) == 0:
            raise ValidationError("*Inputan Mapel tidak boleh kosong.")


class FormEditMapel(FlaskForm):
    mapel = StringField(label="Nama Mata Pelajaran")
    submit = SubmitField(label="Perbaharui Data")

    # def validate_mapel(self, field):
    #     if len(field.data) == 0:
    #         raise ValidationError("*Inputan Mapel tidak boleh kosong.")


class FormSemester(FlaskForm):
    semester = SelectField(
        label="Semester",
        choices=[("", "- Pilih -"), ("ganjil", "Ganjil"), ("genap", "Genap")],
    )
    status = SelectField(
        label="Status",
        choices=[("", "- Pilih -"), ("1", "Aktif"), ("0", "Tidak Aktif")],
    )
    submit = SubmitField("Tambah Data")

    def validate_semester(self, field):
        if field.data == "":
            raise ValidationError("*Pilihan tidak boleh kosong.")

    def validate_status(self, field):
        if field.data == "":
            raise ValidationError("*Pilihan tidak boleh kosong.")


class FormEditSemester(FlaskForm):
    status = SelectField(
        label="Status",
        choices=[("", "- Pilih -"), ("1", "Aktif"), ("0", "Tidak Aktif")],
    )
    submit = SubmitField("Perbaharui Data")

    def validate_status(self, field):
        if field.data == "":
            raise ValidationError("*Pilihan tidak boleh kosong.")


class FormTahunAJaran(FlaskForm):
    tahunAjaran = StringField(label="Tahun Ajaran")
    status = SelectField(
        label="Status",
        choices=[("", "- Pilih -"), ("1", "Aktif"), ("0", "Tidak Aktif")],
    )
    submit = SubmitField("Tambah Data")

    def validate_tahunAjaran(self, field):
        if field.data == "":
            raise ValidationError("*Inputan tidak boleh kosong.")

    def validate_status(self, field):
        if field.data == "":
            raise ValidationError("*Pilihan tidak boleh kosong.")


class FormKelas(FlaskForm):
    kelas = StringField(label="Nama Kelas")
    submit = SubmitField(label="Tambah Data Data")

    def validate_kelas(self, field):
        if field.data == "":
            raise ValidationError("*Inputan tidak boleh kosong.")

        # if KelasModel.get_filter_by(kelas=field.data):
        #     raise ValidationError("Data kelas sudah ada.")


class FormEditKelas(FlaskForm):
    kelas = StringField(label="Kelas")
    jumlahLaki = StringField(label="Laki-Laki")
    jumlahPerempuan = StringField(label="Perempuan")
    jumlahSiswa = StringField(label="Jumlah Siswa")
    submit = SubmitField(label="Perbaharui Data")

    # def validate_kelas(self, field):
    #     if field.data == '':
    #         raise ValidationError('*Inputan tidak boleh kosong.')


class FormHari(FlaskForm):
    hari = SelectField(
        label="Hari",
        choices=[
            ("", "- Pilih -"),
            ("senin", " Senin"),
            ("selasa", "Selasa"),
            ("rabu", "Rabu"),
            ("kamis", "Kamis"),
            ("jumat", "Jumat"),
            ("sabtu", "Sabtu"),
            ("minggu", "Minggu"),
        ],
    )
    submit = SubmitField(label="Tambah Data")

    def validate_hari(self, field):
        if field.data == "":
            raise ValidationError("*Pilih Hari terlebih dahulu.")


class FormJam(FlaskForm):
    jam = StringField("Jam")
    submit = SubmitField("Tambah Data")

    # def validate_jam(self, field):
    #     if field.data == '':
    #         raise ValidationError('*Inputan Jam tidak boleh kosong.')


class FormWaliKelas(FlaskForm):
    namaGuru = SelectField("Nama Guru", choices=[("", "- Pilih -")])
    kelas = SelectField("Nama Kelas", choices=[("", "- Pilih -")])
    submit = SubmitField("Tambah Data")

    def validate_namaGuru(self, field):
        if field.data == "":
            raise ValidationError("*Pilih nama guru terlebih dahulu.")

    def validate_kelas(self, field):
        if field.data == "":
            raise ValidationError("*Pilih nama kelas terlebih dahulu.")


class FormEditWaliKelas(FlaskForm):
    namaGuru = SelectField("Nama Guru", choices=[("", "- Pilih -")])
    kelas = SelectField("Nama Kelas", choices=[("", "- Pilih -")])
    submit = SubmitField("Tambah Data")


class FormEditGuruBK(FlaskForm):
    namaGuru = SelectField("Nama Guru", choices=[("", "- Pilih -")])
    submit = SubmitField("Perbaharui Data")


class FormGuruBK(FlaskForm):
    namaGuru = SelectField("Nama Guru", choices=[("", "- Pilih -")])
    submit = SubmitField("Tambah Data")

    def validate_namaGuru(self, field):
        if field.data == "":
            raise ValidationError("*Pilih nama guru terlebih dahulu.")


class FormKepsek(FlaskForm):
    namaGuru = SelectField("Nama Guru", choices=[("", "- Pilih -")])
    # status = SelectField(
    #     label="Status",
    #     choices=[("", "- Pilih -"), ("1", "Aktif"), ("0", "Tidak Aktif")],
    # )
    submit = SubmitField("Tambah Data")

    def validate_namaGuru(self, field):
        if field.data == "":
            raise ValidationError("*Pilih nama guru terlebih dahulu.")


class FormKepsek(FlaskForm):
    namaGuru = SelectField("Nama Guru", choices=[("", "- Pilih -")])
    submit = SubmitField("Tambah Data")

    def vaildate_namaGuru(self, field):
        if field.data == "":
            raise ValidationError("* Harap Pilih Nama Guru.")


class FormEditKepsek(FlaskForm):
    namaGuru = SelectField("Nama Guru", choices=[("", "- Pilih -")])
    status = SelectField(
        label="Status",
        choices=[("", "- Pilih -"), ("1", "Aktif"), ("0", "Tidak Aktif")],
    )
    submit = SubmitField("Perbaharui Data")


class FormKategoriPelanggaran(FlaskForm):
    kategori = StringField(label="Nama Kategori")
    submit = SubmitField(label="Tambah Data")

    def validate_kategori(self, field):
        if field.data == "":
            raise ValidationError("*Inputan tidak boleh kosong!")


class FormJenisPelanggaran(FlaskForm):
    kategori = SelectField(label="Pilih Kategori", choices=[("", "- Pilih -")])
    jenis = StringField(label="Jenis Pelanggaran")
    poin = IntegerField(label="Jumlah Poin")
    submit = SubmitField(label="Tambah Data")

    def validate_kategori(self, field):
        if field.data == "":
            raise ValidationError("*Harap pilih kategori!")

    def validate_jenis(self, field):
        if field.data == "":
            raise ValidationError("*Inputan tidak boleh kosong!")

    def validate_poin(self, field):
        if field.data == "":
            raise ValidationError("*Inputan tidak boleh kosong!")
