import pytest

from utils.data_loader import get

DEPOSIT = get("deposit")
MESSAGES = get("messages")
pytestmark = [pytest.mark.customer, pytest.mark.regression]


@pytest.mark.smoke
@pytest.mark.parametrize("amount", DEPOSIT["valid_amounts"])
def test_deposit_valid_amount(account, amount):
    before = account.balance()

    account.deposit(amount)

    assert account.message() == MESSAGES["deposit_success"]
    assert account.balance() == before + amount


@pytest.mark.parametrize("amount", DEPOSIT["invalid_amounts"])
def test_deposit_invalid_amount(account, amount):
    before = account.balance()

    account.deposit(amount)

    assert account.message() != MESSAGES["deposit_success"], f"Deposit of {amount} reported success"
    assert account.balance() == before, f"Balance changed after depositing {amount}"