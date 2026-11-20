import allure
import pytest

pytestmark = [pytest.mark.customer, pytest.mark.regression,
              allure.epic("XYZ Bank"), allure.feature("US2 - Customer"), allure.story("Transactions")]

# DEF-04: the history hides every row if the page opens in the same second as the last transaction,
# or if the first and last transactions share a second. These tests check other behaviour, so each step
# is kept in a new second with wait_for_new_second().


@allure.title("A deposit appears in the transaction history")
@allure.severity(allure.severity_level.CRITICAL)
def test_deposit_listed(account):
    account.deposit(250)
    account.wait_for_new_second()

    rows = account.open_transactions().wait_for_transactions(1)

    assert (250, "Credit") in [(r["amount"], r["type"]) for r in rows], \
        f"Deposit not listed in transactions: {rows}"


@allure.title("A withdrawal appears in the transaction history")
@allure.severity(allure.severity_level.CRITICAL)
def test_withdrawal_listed(account):
    account.deposit(250)
    account.wait_for_new_second()
    account.withdraw(50)
    account.wait_for_new_second()

    rows = account.open_transactions().wait_for_transactions(2)

    summary = [(r["amount"], r["type"]) for r in rows]
    assert (250, "Credit") in summary, f"Deposit missing: {summary}"
    assert (50, "Debit") in summary, f"Withdrawal missing: {summary}"


@allure.issue("DEF-03")
@pytest.mark.xfail(reason="DEF-03: customer can reset (erase) transaction history",
                   raises=AssertionError)
@allure.title("Customer cannot reset or alter transaction history")
@allure.severity(allure.severity_level.BLOCKER)
def test_history_cannot_be_reset(account):
    account.deposit(250)
    account.wait_for_new_second()
    page = account.open_transactions()
    before = page.wait_for_transactions(1)
    assert before, "Precondition failed: deposit not listed before Reset"

    if page.reset_visible():
        page.reset()

    assert page.transactions() == before, "Transaction history changed after Reset"
    assert page.back().balance() == 250, "Balance changed after Reset"


@allure.title("Back returns to the account page")
@allure.severity(allure.severity_level.MINOR)
def test_back_to_account(account):
    page = account.open_transactions()

    assert page.back().welcome_name(), "Back did not return to the account page"
