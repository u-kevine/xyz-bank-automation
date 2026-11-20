import pytest

from utils.data_loader import get

W = get("withdraw")
MESSAGES = get("messages")
pytestmark = [pytest.mark.customer, pytest.mark.regression]


@pytest.mark.smoke
def test_withdraw_within_balance(account):
    account.deposit(W["opening_deposit"])

    account.withdraw(W["valid_amount"])

    assert account.message() == MESSAGES["withdraw_success"]
    assert account.balance() == W["opening_deposit"] - W["valid_amount"]


def test_withdraw_exact_balance(account):
    account.deposit(300)

    account.withdraw(300)

    assert account.message() == MESSAGES["withdraw_success"]
    assert account.balance() == 0


def test_withdraw_more_than_balance(account):
    account.deposit(100)

    account.withdraw(101)

    assert account.message() == MESSAGES["withdraw_insufficient"]
    assert account.balance() == 100, "Balance changed after a rejected withdrawal"


@pytest.mark.parametrize("amount", W["invalid_amounts"])
def test_withdraw_invalid_amount(account, amount):
    account.deposit(100)

    account.withdraw(amount)

    assert account.message() != MESSAGES["withdraw_success"], f"Withdrawal of {amount} reported success"
    assert account.balance() == 100, f"Balance changed after withdrawing {amount}"