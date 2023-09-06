from app.backup_db_cli import db


def register_cli(app):
    app.register_blueprint(db)
