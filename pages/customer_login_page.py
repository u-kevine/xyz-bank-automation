import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage

PLACEHOLDER = "---Your Name---"


class CustomerLoginPage(BasePage):
    USER_SELECT = (By.ID, "userSelect")
    LOGIN = (By.CSS_SELECTOR, "form button[type='submit']")

    def wait_loaded(self):
        self.find(self.USER_SELECT)
        return self

    def customer_names(self):
        return [n for n in self.option_texts(self.USER_SELECT) if n and n != PLACEHOLDER]

    @allure.step("Log in as customer {full_name}")
    def login(self, full_name):
        from pages.account_page import AccountPage
        self.select_by_text(self.USER_SELECT, full_name)
        self.click(self.LOGIN)          # button only appears after a name is selected
        return AccountPage(self.driver).wait_loaded()   