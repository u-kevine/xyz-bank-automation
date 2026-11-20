import allure
import pytest

from utils.data_loader import get

DEPOSIT = get("deposit")
MESSAGES = get("messages")
pytestmark = [pytest.mark.customer, pytest.mark.regression,
              allure.epic("XYZ Bank"), allure.feature("US2 - Customer"), allure.story("Deposit")]


@pytest.mark.smoke
@pytest.mark.parametrize("amount", DEPOSIT["valid_amounts"])
@allure.title("Deposit a valid amount and the balance updates")
@allure.severity(allure.severity_level.CRITICAL)
def test_deposit_valid_amount(account, amount):
    before = account.balance()

    account.deposit(amount)

    assert account.message() == MESSAGES["deposit_success"]
    assert account.balance() == before + amount


@pytest.mark.parametrize("amount", DEPOSIT["invalid_amounts"])
@allure.title("Zero or negative deposit is rejected")
@allure.severity(allure.severity_level.CRITICAL)
def test_deposit_invalid_amount(account, amount):
    before = account.balance()

    account.deposit(amount)

    assert account.message() != MESSAGES["deposit_success"], f"Deposit of {amount} reported success"
    assert account.balance() == before, f"Balance changed after depositing {amount}"
