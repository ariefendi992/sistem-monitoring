from app.api.controller.auth_controller import auth
from app.api.controller.siswa_controller import siswa
from app.api.controller.guru_controller import guru
from app.api.controller.master_controller import master
from app.api.controller.data_controller import data
from app.api.controller.download_controller import download
from app.api.controller.jadwal_belajar_siswa import jadwal


def register_app(app):
    app.register_blueprint(auth)
    app.register_blueprint(siswa)
    app.register_blueprint(guru)
    app.register_blueprint(master)
    app.register_blueprint(data)
    app.register_blueprint(download)
    app.register_blueprint(jadwal)
