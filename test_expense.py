import pytest
from models.expense import Expense


def test_expense():
    expense1 = Expense("KFC", "01/01/2001", "Food", 10.56)

    assert expense1.name == "KFC"
    assert expense1.date == "01/01/2001"
    assert expense1.category == "Food"
    assert expense1.amount == 10.56


def test_invalid_expense():
    with pytest.raises(TypeError):
        Expense(100, "01/01/2001", "Food", 10.56)
    with pytest.raises(TypeError):
        Expense("KFC", 1 / 1 / 2001, "Food", 10.56)
    with pytest.raises(TypeError):
        Expense("KFC", "01/01/2001", 123, 10.56)
    with pytest.raises(TypeError):
        Expense("KFC", "01/01/2001", "Food", "0.56")

    with pytest.raises(ValueError):
        Expense("KFC", "01/01/01", "Food", 10.56)
    with pytest.raises(ValueError):
        Expense("KFC", "01/01/xxxx", "Food", 10.56)
    with pytest.raises(ValueError):
        Expense("KFC", "01/01/2001", "Some Category", 10.56)
    with pytest.raises(ValueError):
        Expense("KFC", "01-01-2001", "Food", 10.56)
    with pytest.raises(ValueError):
        Expense("KFC", "01/01/2001", "Food", -10.56)


def test_to_dict():
    expense1 = Expense("KFC", "01/01/2001", "Food", 10.56)
    expense1_dict = {
        "name": "KFC",
        "date": "01/01/2001",
        "category": "Food",
        "amount": 10.56,
    }

    assert expense1.to_dict() == expense1_dict
