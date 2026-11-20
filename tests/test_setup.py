from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.config import BASE_URL
from utils.driver_factory import create_driver


def test_app_opens():
    driver = create_driver()
    try:
        driver.get(BASE_URL)
        page = BasePage(driver)
        manager_button = (By.XPATH, "//button[@ng-click='manager()']")
        assert page.is_visible(manager_button), "Bank Manager Login button not found"
    finally:
        driver.quit()