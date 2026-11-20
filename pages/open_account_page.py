import allure
from selenium.webdriver.common.by import By

from pages.manager_page import ManagerPage


class OpenAccountPage(ManagerPage):
    CUSTOMER_SELECT = (By.ID, "userSelect")
    CURRENCY_SELECT = (By.ID, "currency")
    PROCESS = (By.CSS_SELECTOR, "form button[type='submit']")

    def wait_loaded(self):
        self.find(self.CURRENCY_SELECT)
        return self

    def customer_options(self):
        return self.option_texts(self.CUSTOMER_SELECT)

    @allure.step("Open {currency} account for {customer_name}")
    def open_account(self, customer_name, currency):
        """Returns the alert text, e.g. 'Account created successfully with account Number :1016'."""
        self.select_by_text(self.CUSTOMER_SELECT, customer_name)
        self.select_by_text(self.CURRENCY_SELECT, currency)
        self.click(self.PROCESS)
        return self.accept_alert_if_present()