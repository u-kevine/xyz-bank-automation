from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class ManagerPage(BasePage):
    ADD_CUSTOMER_TAB = (By.XPATH, "//button[@ng-click='addCust()']")
    OPEN_ACCOUNT_TAB = (By.XPATH, "//button[@ng-click='openAccount()']")
    CUSTOMERS_TAB = (By.XPATH, "//button[@ng-click='showCust()']")

    def wait_loaded(self):
        self.find(self.ADD_CUSTOMER_TAB)
        return self

    def tabs_visible(self):
        return all(self.is_visible(tab) for tab in
                   (self.ADD_CUSTOMER_TAB, self.OPEN_ACCOUNT_TAB, self.CUSTOMERS_TAB))