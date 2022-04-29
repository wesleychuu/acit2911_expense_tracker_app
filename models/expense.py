class Expense:
    def __init__(self, name, date, category, amount, notes=None):
        if type(name) is not str:
            raise TypeError

        # format: MM/DD/YYYY, done in HTML
        if type(date) is not str:
            raise TypeError

        if type(amount) is not int or type(amount) is not float:
            raise TypeError

        self.name = name
        self.date = date
        self.category = category
        self.amount = amount
        self.notes = notes
