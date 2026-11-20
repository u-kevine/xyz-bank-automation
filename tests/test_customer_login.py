import pytest

from utils.data_loader import get

pytestmark = [pytest.mark.customer, pytest.mark.regression]


@pytest.mark.smoke
def test_customer_login(home):
    c = get("existing_customers")[0]
    name = f"{c['first_name']} {c['last_name']}"

    account = home.go_to_customer_login().login(name)

    assert account.welcome_name() == name
    assert account.account_number().isdigit(), "Account number is not shown"
    assert account.currency() in get("currencies")


def test_logout(account):
    login_page = account.logout()

    assert login_page.customer_names(), "Customer selection is not shown after logout"