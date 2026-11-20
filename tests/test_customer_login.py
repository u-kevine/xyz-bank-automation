import allure
import pytest

from utils.data_loader import get

pytestmark = [pytest.mark.customer, pytest.mark.regression,
              allure.epic("XYZ Bank"), allure.feature("US2 - Customer"), allure.story("Login")]


@pytest.mark.smoke
@allure.title("Existing customer can log in and see account details")
@allure.severity(allure.severity_level.BLOCKER)
def test_customer_login(home):
    c = get("existing_customers")[0]
    name = f"{c['first_name']} {c['last_name']}"

    account = home.go_to_customer_login().login(name)

    assert account.welcome_name() == name
    assert account.account_number().isdigit(), "Account number is not shown"
    assert account.currency() in get("currencies")


@allure.title("Logout returns to customer selection")
@allure.severity(allure.severity_level.NORMAL)
def test_logout(account):
    login_page = account.logout()

    assert login_page.customer_names(), "Customer selection is not shown after logout"
