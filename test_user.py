import pytest
from models.user import User
from models.expense import Expense, CATEGORIES


@pytest.fixture
def new_user():
    user1 = User(name="aleksandar zivkovic", email="azivkovic@my.bcit.ca",
                 username="alziv", password="password123")
    return user1


@pytest.fixture
def new_user2():
    user2 = User(name="Sean Walker",
                 username="swalker", email="swalker22@outlook.com", password="seaniscool32")
    return user2


@pytest.fixture
def new_expense():
    expense1 = Expense(name="McDonalds", date="2022-05-03",
                       category="Food", amount=5.23)
    return expense1


def test_name(new_user):
    assert new_user.name == "aleksandar zivkovic"


def test_name_invalid():
    """Name must be a string"""
    with pytest.raises(TypeError):
        User(name=12354, email="test@test.com",
             username="hello", password="password123")


def test_email(new_user):
    assert new_user.email == "azivkovic@my.bcit.ca"


def test_email_invalid():
    """Email must be a string"""
    with pytest.raises(TypeError):
        User(name="john smith", email=123123,
             username="hello", password="password453")


def test_email_no_at():
    """Email must contain the @ symbol"""
    with pytest.raises(ValueError):
        User(name="john hunter", email="johnhoutlook.com",
             username="johnhunt", password="password423")


def test_username(new_user):
    assert new_user.username == "alziv"


def test_username_invalid():
    """Username must be a string"""
    with pytest.raises(TypeError):
        User(name="bob wall", email="bob@gmail.com",
             username=54333, password="password321")


def test_username_too_short():
    """Username must be at least 5 characters long"""
    with pytest.raises(ValueError):
        User(name="henry gates", email="henry@gmail.com",
             username="henr", password="henryiscool33")


def test_password(new_user):
    assert new_user.password == "password123"


def test_password_invalid():
    """Password must be a string"""
    with pytest.raises(TypeError):
        User(name="carl johnson", email="carlj@outlook.com",
             username="carljohn", password=12312)


def test_password_too_short():
    """Password must be at least 8 characters long"""
    with pytest.raises(ValueError):
        User(name="john hunter", email="johnh@outlook.com",
             username="johnhunt", password="passwor")


def test_password_no_numbers():
    """Password must contain at least one number"""
    with pytest.raises(ValueError):
        User(name="john hunter", email="johnh@outlook.com",
             username="johnhunt", password="password")


def test_password_no_letters():
    """Password must contain at least one letter"""
    with pytest.raises(ValueError):
        User(name="hello world", email="hworld@gmail.com",
             username="hworld", password="12343252")


# def test_add_expense(new_user2, new_expense):
#     """THIS MAY NOT WORK PROPERLY"""
#     new_user2.add_expense(new_expense)
#     assert new_user2.expenses == [
#         {"amount": 5.23, "category": "Food", "date": "2022-05-03", "name": "McDonalds"}]


# def test_add_invalid_expenses(new_user2):
#     """Expense must be an instance of the expense class"""
#     with pytest.raises(TypeError):
#         new_user2.add_expense("food")


# def test_delete_expense(new_user2, new_expense):
#     """THIS MAY NOT WORK PROPERLY"""
#     new_user2.delete_expense(new_expense)
#     assert new_user2.expenses == []


# def test_delete_expense_invalid(new_user2):
#     with pytest.raises(TypeError):
#         new_user2.delete_expense("school")


# def test_to_dict(new_user2):
#     """Should return a dictionary of the user's attributes"""
#     assert new_user2.to_dict() == {"name": "Sean Walker", "username": "swalker",
#                                    "email": "swalker22@outlook.com", "password": "seaniscool32", "expenses": [{"amount": 5.23, "category": "Food", "date": "2022-05-03", "name": "McDonalds"}]}
