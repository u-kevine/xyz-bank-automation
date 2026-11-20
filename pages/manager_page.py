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

    def open_add_customer(self):
        from pages.add_customer_page import AddCustomerPage
        self.click(self.ADD_CUSTOMER_TAB)
        return AddCustomerPage(self.driver).wait_loaded()

    def open_open_account(self):
        from pages.open_account_page import OpenAccountPage
        self.click(self.OPEN_ACCOUNT_TAB)
        return OpenAccountPage(self.driver).wait_loaded()

    def open_customers(self):
        from pages.customers_page import CustomersPage
        self.click(self.CUSTOMERS_TAB)
        return CustomersPage(self.driver).wait_loaded()