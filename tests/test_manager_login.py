import allure
import pytest

pytestmark = [pytest.mark.manager, pytest.mark.regression,
              allure.epic("XYZ Bank"), allure.feature("US1 - Bank Manager"), allure.story("Login")]


@pytest.mark.smoke
@allure.title("Bank Manager can log in")
@allure.severity(allure.severity_level.BLOCKER)
def test_manager_login(home):
    manager = home.login_as_manager()
    assert manager.tabs_visible(), "Manager tabs are not all visible"


@allure.title("Home button returns to the start screen")
@allure.severity(allure.severity_level.MINOR)
def test_home_button_returns_to_start(home):
    home.login_as_manager()
    home.go_home()
    assert home.is_visible(home.MANAGER_LOGIN)
