import click
import os
from flask import Blueprint

db = Blueprint("db", __name__)


@db.cli.command("backup")
@click.argument("dbname")
def backup_db(dbname):
    target = os.getcwd() + "/database/"
    os.system(f"mysqldump -u root {dbname} >{target}{dbname}.sql")
