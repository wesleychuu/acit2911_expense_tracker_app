CATEGORIES = ["Food", "Apparel", "Entertainment",
              "Lifestyle", "Miscellaneious", "Groceries",
              "Services", "Technology", "School"]


class Expense:
    def __init__(self, name, date, category, amount):
        if type(name) is not str:
            raise TypeError

        # format: MM/DD/YYYY, done in HTML
        if type(date) is not str:
            raise TypeError

        if type(category) is not str:
            raise TypeError

        if category not in CATEGORIES:
            raise ValueError

        if type(amount) is not int or type(amount) is not float:
            raise TypeError

        if amount < 0:
            raise ValueError

        self.name = name
        self.date = date
        self.category = category
        self.amount = amount

    @property
    def name(self):
        """Get expense name"""
        return self.name

    @name.setter
    def name(self, name):
        """Set expense name"""
        if type(name) is not str:
            raise TypeError

        self.name = name

    @property
    def date(self):
        """Get expense name"""
        return self.date

    @date.setter
    def date(self, date):
        """Set expense name"""
        if type(date) is not str:
            raise TypeError

        self.date = date

    @property
    def category(self):
        """Get expense name"""
        return self.name

    @category.setter
    def category(self, category):
        """Set expense name"""
        if type(category) is not str:
            raise TypeError

        if category not in CATEGORIES:
            raise ValueError

        self.category = category

    @property
    def amount(self):
        """Get expense amount"""
        return self.amount

    @amount.setter
    def amount(self, amount):
        """Set expense amount"""
        if type(amount) is not int or type(amount) is not float:
            raise TypeError

        if amount < 0:
            raise ValueError

        self.amount = amount

    def to_dict(self):
        return {
            "name": self.name,
            "date": self.date,
            "category": self.category,
            "amount": self.amount
        }
