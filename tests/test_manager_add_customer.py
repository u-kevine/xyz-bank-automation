import pytest

from utils.data_generator import unique_customer
from utils.data_loader import get

pytestmark = [pytest.mark.manager, pytest.mark.regression]

MESSAGES = get("messages")
INVALID_NAMES = get("invalid_names")
INVALID_POST_CODES = get("invalid_post_codes")


@pytest.mark.smoke
def test_add_customer_valid(home):
    base = get("valid_customer")
    customer = unique_customer(base["first_name"], base["last_name"], base["post_code"])
    add_page = home.login_as_manager().open_add_customer()

    alert = add_page.add_customer(customer["first_name"], customer["last_name"], customer["post_code"])

    assert alert and MESSAGES["customer_added"] in alert, f"Unexpected alert: {alert}"
    row = add_page.open_customers().find_customer(customer["first_name"], customer["last_name"])
    assert row is not None, "New customer is missing from the Customers list"
    assert row["post_code"] == customer["post_code"]


@pytest.mark.xfail(reason="DEF-01: customer name accepts digits and special characters",
                   raises=AssertionError)
@pytest.mark.parametrize("data", INVALID_NAMES, ids=[d["id"] for d in INVALID_NAMES])
def test_reject_non_alphabetic_names(home, data):
    add_page = home.login_as_manager().open_add_customer()

    alert = add_page.add_customer(data["first_name"], data["last_name"], "10001")

    assert not (alert and MESSAGES["customer_added"] in alert), \
        f"Name with invalid characters was accepted: {alert}"


@pytest.mark.xfail(reason="DEF-02: postcode accepts non-numeric characters",
                   raises=AssertionError)
@pytest.mark.parametrize("post_code", INVALID_POST_CODES)
def test_reject_non_numeric_post_code(home, post_code):
    customer = unique_customer(post_code=post_code)
    add_page = home.login_as_manager().open_add_customer()

    alert = add_page.add_customer(customer["first_name"], customer["last_name"], post_code)

    assert not (alert and MESSAGES["customer_added"] in alert), \
        f"Postcode '{post_code}' was accepted: {alert}"


def test_required_first_name(home):
    add_page = home.login_as_manager().open_add_customer()

    alert = add_page.add_customer("", "Lovelace", "10001")

    assert alert is None, f"Form submitted with an empty first name: {alert}"
    assert add_page.validation_message("first_name"), "No validation message on empty first name"


def test_duplicate_customer_rejected(home):
    customer = unique_customer()
    add_page = home.login_as_manager().open_add_customer()
    add_page.add_customer(customer["first_name"], customer["last_name"], customer["post_code"])

    second_alert = add_page.add_customer(customer["first_name"], customer["last_name"], customer["post_code"])

    assert second_alert and MESSAGES["duplicate_customer"] in second_alert, \
        f"Duplicate customer was not rejected: {second_alert}"
