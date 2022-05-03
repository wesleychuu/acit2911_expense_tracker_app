from models.expense import Expense


class User:

    def __init__(self, userid, name, username, email, password, expenses=[]):
        if type(name) is not str:
            raise ValueError

        if type(email) is not str:
            raise ValueError

        self.id = userid
        self.name = name
        self.username = username
        self.email = email
        self.password = password
        self.expenses = expenses

    def add_expense(self, expense: Expense):
        """Add an expense to user's list

        Note: not quite right, need to fix
        """
        if type(expense) is not Expense:
            raise TypeError

        self.expenses.append(expense)

    def delete_expense(self, expense: Expense):
        """Remove an expense from user's list

        Note: probably not right, need to fix
        """
        index = None
        for i, e in enumerate(self.expenses):
            if e.get_expense_id() == expense.get_expense_id():
                index = i
                break

        del self.expenses[index]

    def to_dict(self):
        expenses = [e.to_dict() for e in self.expenses]

        user_dict = {
            "userid": self.id,
            "name": self.name,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "expenses": expenses
        }

        return user_dict
