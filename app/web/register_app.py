from app.web.controller.admin_controller import admin2
from app.web.controller.guru_controller import guru2
from app.web.controller.login_controller import auth2
from app.web.controller.wali_kelas_controller import wali_kelas
from app.web.controller.proses_controller import proses
from app.web.controller.guru_bk_controller import guru_bk


def register_app_web(app):
    app.register_blueprint(guru2)
    app.register_blueprint(admin2)
    app.register_blueprint(auth2)
    app.register_blueprint(wali_kelas)
    app.register_blueprint(proses)
    app.register_blueprint(guru_bk)
