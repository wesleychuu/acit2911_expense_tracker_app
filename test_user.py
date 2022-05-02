import pytest
from models.user import User


@pytest.fixture
def new_user():
    user1 = User(name="aleksandar zivkovic", email="azivkovic@my.bcit.ca",
                 username="alziv", password="password123")
    return user1


def test_name():
    assert new_user.name == "aleksandar zivkovic"


def test_name_invalid():
    """Name must be a string"""
    with pytest.raises(ValueError):
        User(name=12354, email="test@test.com",
             username="hello", password="password123")


def test_email():
    assert new_user.email == "azivkovic@my.bcit.ca"


def test_email_invalid():
    """Email must be a string"""
    with pytest.raises(ValueError):
        User(name="john smith", email=123123,
             username="hello", password="password453")


def test_email_no_at():
    """Email must contain the @ symbol"""
    with pytest.raises(ValueError):
        User(name="john hunter", email="johnhoutlook.com",
             username="johnhunt", password="password423")


def test_username():
    assert new_user.username == "alziv"


def test_username_invalid():
    """Username must be a string"""
    with pytest.raises(ValueError):
        User(name="bob wall", email="bob@gmail.com",
             username=54333, password="password321")


def test_username_too_short():
    """Username must be at least 5 characters long"""
    with pytest.raises(ValueError):
        User(name="henry gates", email="henry@gmail.com",
             username="henr", password="henryiscool33")


def test_password():
    assert new_user.password == "password123"


def test_password_invalid():
    with pytest.raises(ValueError):
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
