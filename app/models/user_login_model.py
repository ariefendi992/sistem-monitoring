import os
from flask_login import UserMixin
from ..site.lib.json import JsonFileObject

file = os.getcwd() + "/data.json"


class UserLogin(UserMixin):
    def __init__(self, id=None) -> None:
        filename = JsonFileObject(file)
        data = filename.get_json()
        self.id = id
        self.username = data.get("username")
        self.group = data.get("group")
        self.first_name = data.get("first_name")
        self.last_name = data.get("last_name")

    def __repr__(self) -> str:
        return f"group : {self.group}"
