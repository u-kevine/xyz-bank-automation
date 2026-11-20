import pytest

from pages.customer_login_page import CustomerLoginPage

from utils.data_generator import full_name
from utils.data_loader import get

pytestmark = [pytest.mark.manager, pytest.mark.regression]

MESSAGES = get("messages")


@pytest.mark.smoke
@pytest.mark.parametrize("currency", get("currencies"))
def test_open_account_for_new_customer(home, new_customer, currency):
    manager = home.login_as_manager()

    alert = manager.open_open_account().open_account(full_name(new_customer), currency)

    assert alert and MESSAGES["account_created"] in alert, f"Unexpected alert: {alert}"
    account_no = alert.split(":")[-1].strip()
    row = manager.open_customers().find_customer(new_customer["first_name"], new_customer["last_name"])
    assert account_no in row["accounts"], f"Account {account_no} not listed for the customer"
    account = home.go_home().go_to_customer_login().login(full_name(new_customer))
    assert account.account_number() == account_no
    assert account.balance() == 0
    assert account.currency() == currency


def test_new_customer_available_for_account(home, new_customer):
    options = home.login_as_manager().open_open_account().customer_options()

    assert full_name(new_customer) in options, "New customer is not in the Open Account list"


def test_search_customer(home):
    target = get("existing_customers")[1]
    customers = home.login_as_manager().open_customers().search(target["first_name"])

    rows = customers.rows()

    assert rows, "Search returned no rows"
    assert any(r["first_name"] == target["first_name"] and r["last_name"] == target["last_name"]
               for r in rows), "Searched customer not in results"
    for r in rows:
        values = " ".join([r["first_name"], r["last_name"], r["post_code"]] + r["accounts"]).lower()
        assert target["first_name"].lower() in values, f"Row does not match search: {r}"


def test_delete_existing_customer(home):
    target = get("existing_customers")[1]
    customers = home.login_as_manager().open_customers()

    deleted = customers.delete_customer(target["first_name"], target["last_name"])

    assert deleted, "Customer row not found"
    assert customers.find_customer(target["first_name"], target["last_name"]) is None, \
        "Customer is still listed after deletion"


def test_delete_new_customer_with_account(home, new_customer):
    manager = home.login_as_manager()
    manager.open_open_account().open_account(full_name(new_customer), "Dollar")
    customers = manager.open_customers()

    customers.delete_customer(new_customer["first_name"], new_customer["last_name"])

    assert customers.find_customer(new_customer["first_name"], new_customer["last_name"]) is None

def test_no_access_without_account(home, new_customer):
    account = home.go_to_customer_login().login(full_name(new_customer))

    assert account.has_no_account_message(), "'No account' message is not shown"
    assert account.no_account_message() == MESSAGES["no_account"]
    assert not account.can_transact(), "Deposit/Withdraw available without an account"


def test_deleted_customer_cannot_log_in(home, customer_with_account):
    c = customer_with_account
    home.login_as_manager().open_customers().delete_customer(c["first_name"], c["last_name"])

    login_names = home.go_home().go_to_customer_login().customer_names()

    assert full_name(c) not in login_names, f"Deleted customer {full_name(c)} can still log in"