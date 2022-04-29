class User:

    def __init__(self, name, email, username, password):
        if type(name) is not str:
            raise ValueError

        if type(email) is not str:
            raise ValueError

        self.name = name
        self.email = email
        self.username = username
        self.password = password