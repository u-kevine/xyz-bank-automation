import allure
from selenium.webdriver.common.by import By

from pages.manager_page import ManagerPage


class AddCustomerPage(ManagerPage):
    FIRST_NAME = (By.XPATH, "//input[@ng-model='fName']")
    LAST_NAME = (By.XPATH, "//input[@ng-model='lName']")
    POST_CODE = (By.XPATH, "//input[@ng-model='postCd']")
    SUBMIT = (By.CSS_SELECTOR, "form button[type='submit']")

    def wait_loaded(self):
        self.find(self.FIRST_NAME)
        return self

    @allure.step("Add customer {first_name} {last_name} ({post_code})")
    def add_customer(self, first_name, last_name, post_code):
        """Fills and submits the form. Returns the alert text, or None if no alert appeared."""
        self.type(self.FIRST_NAME, first_name)
        self.type(self.LAST_NAME, last_name)
        self.type(self.POST_CODE, post_code)
        self.click(self.SUBMIT)
        return self.accept_alert_if_present()

    def validation_message(self, field="first_name"):
        """Browser (HTML5) validation message of a field, e.g. 'Please fill out this field.'"""
        locator = {"first_name": self.FIRST_NAME, "last_name": self.LAST_NAME,
                   "post_code": self.POST_CODE}[field]
        return self.find(locator).get_attribute("validationMessage")