import pytest

pytestmark = [pytest.mark.manager, pytest.mark.regression]


@pytest.mark.smoke
def test_manager_login(home):
    manager = home.login_as_manager()
    assert manager.tabs_visible(), "Manager tabs are not all visible"


def test_home_button_returns_to_start(home):
    home.login_as_manager()
    home.go_home()
    assert home.is_visible(home.MANAGER_LOGIN)