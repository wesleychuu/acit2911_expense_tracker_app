import json
import itertools

from models.user import User


class UserManager:

    id_iter = itertools.count(start=0, step=1)

    def __init__(self):
        with open("data/users.json") as fp:
            self.users = [
                User(
                    elem["userid"],
                    elem["name"],
                    elem["username"],
                    elem["email"],
                    elem["password"],
                    elem["expenses"]
                ) for elem in json.load(fp)
            ]
