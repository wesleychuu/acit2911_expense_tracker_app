import json

from models.user import User


class UserManager:
    def __init__(self):
        self.users = []
        with open("data/users.json") as fp:
            data = json.load(fp)
            for user in data:
                self.users.append(User(**user))
