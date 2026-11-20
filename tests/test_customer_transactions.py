import pytest

pytestmark = [pytest.mark.customer, pytest.mark.regression]


def test_deposit_listed(account):
    account.deposit(250)

    rows = account.open_transactions().wait_for_transactions(1)

    assert (250, "Credit") in [(r["amount"], r["type"]) for r in rows], \
        f"Deposit not listed in transactions: {rows}"


def test_withdrawal_listed(account):
    account.deposit(250)
    account.withdraw(50)

    rows = account.open_transactions().wait_for_transactions(2)

    summary = [(r["amount"], r["type"]) for r in rows]
    assert (250, "Credit") in summary, f"Deposit missing: {summary}"
    assert (50, "Debit") in summary, f"Withdrawal missing: {summary}"


@pytest.mark.xfail(reason="DEF-03: customer can reset (erase) transaction history")
def test_history_cannot_be_reset(account):
    account.deposit(250)
    page = account.open_transactions()
    before = page.wait_for_transactions(1)

    if page.reset_visible():
        page.reset()

    assert page.transactions() == before, "Transaction history changed after Reset"
    assert page.back().balance() == 250, "Balance changed after Reset"


def test_back_to_account(account):
    page = account.open_transactions()

    assert page.back().welcome_name(), "Back did not return to the account page"