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