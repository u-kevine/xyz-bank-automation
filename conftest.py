from utils.data_generator import unique_customer
import pytest

from pages.home_page import HomePage
from utils.driver_factory import create_driver


@pytest.fixture
def driver():
    """A fresh browser per test. The app keeps data in memory, so every test starts clean."""
    drv = create_driver()
    yield drv
    drv.quit()


@pytest.fixture
def home(driver):
    """The bank app's home page, already open."""
    return HomePage(driver).open()


@pytest.fixture
def new_customer(home):
    """Creates a unique customer (no account yet) and returns its data."""
    customer = unique_customer()
    home.login_as_manager().open_add_customer().add_customer(
        customer["first_name"], customer["last_name"], customer["post_code"])
    home.go_home()
    return customer