import json
# import itertools

from models.user import User


class UserManager:

    # id_iter = itertools.count(start=0, step=1)

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

    def __len__(self):
        return len(self.users)

    def save(self):
        """Save all user info to users.json file; serialize using User.to_dict()"""
        with open("data/users.json", "w") as fp:
            json.dump([user.to_dict() for user in self.users], fp)

    def get_latest_userid(self) -> int:
        """Get the user ID of the latest user and add one"""
        return self.users[-1]["userid"] + 1

    def add_new_user(self, name, username, email, password):
        """Create a new user and add them"""
        id = self.get_latest_userid()
        user = User(id, name, username, email, password)
        self.users.append(user)

    def get_uesr_by_id(self, userid: int) -> User:
        """Find a user by ID and return the instance"""
        for user in self.users:
            if user.id == userid:
                return user

    def delete_user(self, userid) -> bool:
        """Find a user by ID and remove them if they exist"""
        user = self.get_uesr_by_id(userid)
        if user:
            self.users.remove(user)
            return True

        return False
