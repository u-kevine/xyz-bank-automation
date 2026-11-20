import platform
import shutil
from pathlib import Path

import allure
import pytest

from pages.home_page import HomePage
from utils import config
from utils.data_generator import full_name, unique_customer
from utils.driver_factory import create_driver

ROOT = Path(__file__).resolve().parent


# ---------------- browser ----------------
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


# ---------------- business-flow fixtures ----------------
@pytest.fixture
def new_customer(home):
    """Creates a unique customer (no account yet) and returns its data."""
    customer = unique_customer()
    with allure.step(f"Precondition: create customer {full_name(customer)}"):
        home.login_as_manager().open_add_customer().add_customer(
            customer["first_name"], customer["last_name"], customer["post_code"])
        home.go_home()
    return customer


@pytest.fixture
def customer_with_account(home, new_customer):
    """A unique customer with one Dollar account (balance 0)."""
    with allure.step("Precondition: open a Dollar account"):
        home.login_as_manager().open_open_account().open_account(full_name(new_customer), "Dollar")
        home.go_home()
    return new_customer


@pytest.fixture
def account(home, customer_with_account):
    """Logged in as a fresh customer with balance 0, ready to transact."""
    with allure.step("Precondition: log in as the new customer"):
        return home.go_to_customer_login().login(full_name(customer_with_account))


# ---------------- Allure integration ----------------
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach a screenshot and the URL when a test fails or hits a known defect (xfail)."""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and (report.failed or hasattr(report, "wasxfail")):
        drv = item.funcargs.get("driver")
        if drv is not None:
            try:
                allure.attach(drv.get_screenshot_as_png(), name="screenshot",
                              attachment_type=allure.attachment_type.PNG)
                allure.attach(drv.current_url, name="url",
                              attachment_type=allure.attachment_type.URI_LIST)
            except Exception:  # browser may already be gone
                pass


def pytest_sessionstart(session):
    """Write run environment info and defect categories into the Allure results folder."""
    results_dir = session.config.getoption("allure_report_dir", default=None)
    if not results_dir:
        return
    results = Path(results_dir)
    results.mkdir(parents=True, exist_ok=True)
    env = {
        "Base.URL": config.BASE_URL,
        "Browser": config.BROWSER,
        "Headless": config.HEADLESS,
        "Remote.Grid": config.SELENIUM_REMOTE_URL or "local",
        "Python": platform.python_version(),
    }
    (results / "environment.properties").write_text(
        "\n".join(f"{k}={v}" for k, v in env.items()), encoding="utf-8")
    shutil.copy(ROOT / "allure_config" / "categories.json", results / "categories.json")
