"""Shared Selenium helpers. Page objects inherit from BasePage; tests never touch locators."""
import allure
from selenium.common.exceptions import NoAlertPresentException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from utils.config import TIMEOUT


class BasePage:
    def __init__(self, driver, timeout=TIMEOUT):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)

    # ---- element helpers -------------------------------------------------
    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator):
        return self.driver.find_elements(*locator)

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator, text):
        element = self.find(locator)
        element.clear()
        element.send_keys(str(text))

    def text_of(self, locator):
        return self.find(locator).text.strip()

    def select_by_text(self, locator, text):
        Select(self.find(locator)).select_by_visible_text(text)

    def option_texts(self, locator):
        return [o.text.strip() for o in Select(self.find(locator)).options]

    def is_visible(self, locator, timeout=3):
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def wait_for_text(self, locator, text):
        self.wait.until(EC.text_to_be_present_in_element(locator, text))

    # ---- alert helpers ---------------------------------------------------
    def accept_alert_if_present(self, timeout=3):
        """Returns the alert text and accepts it, or None when no alert appears."""
        try:
            alert = WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
        except TimeoutException:
            return None
        try:
            text = alert.text
            alert.accept()
        except NoAlertPresentException:
            return None
        allure.attach(text, name="alert_text", attachment_type=allure.attachment_type.TEXT)
        return text