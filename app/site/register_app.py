from app.site.controller.admin_controller import admin2
from app.site.controller.guru_controller import guru2
from app.site.controller.login_controller import auth2
from app.site.controller.wali_kelas_controller import wali_kelas
from app.site.controller.data_preprocessing_controller import data_pre
from app.site.controller.guru_bk_controller import guru_bk


def register_app_site(app):
    app.register_blueprint(guru2)
    app.register_blueprint(admin2)
    app.register_blueprint(auth2)
    app.register_blueprint(wali_kelas)
    app.register_blueprint(data_pre)
    app.register_blueprint(guru_bk)
