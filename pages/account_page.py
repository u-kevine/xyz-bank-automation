import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class AccountPage(BasePage):
    WELCOME_NAME = (By.CSS_SELECTOR, "span.fontBig")
    NO_ACCOUNT_MSG = (By.XPATH, "//span[@ng-show='noAccount']")
    ACCOUNT_SELECT = (By.ID, "accountSelect")
    ACCOUNT_INFO = (By.XPATH, "//div[@ng-hide='noAccount']//strong")   # [number, balance, currency]
    TRANSACTIONS_TAB = (By.XPATH, "//button[@ng-click='transactions()']")
    DEPOSIT_TAB = (By.XPATH, "//button[@ng-click='deposit()']")
    WITHDRAW_TAB = (By.XPATH, "//button[@ng-click='withdrawl()']")
    FORM_LABEL = (By.CSS_SELECTOR, "form label")
    AMOUNT = (By.XPATH, "//input[@ng-model='amount']")
    SUBMIT = (By.CSS_SELECTOR, "form button[type='submit']")
    MESSAGE = (By.CSS_SELECTOR, "span.error")
    LOGOUT = (By.CSS_SELECTOR, "button.logout")

    def wait_loaded(self):
        self.find(self.WELCOME_NAME)
        return self

    # ---- account info ----------------------------------------------------
    def welcome_name(self):
        return self.text_of(self.WELCOME_NAME)

    def has_no_account_message(self):
        return self.is_visible(self.NO_ACCOUNT_MSG)

    def no_account_message(self):
        return self.text_of(self.NO_ACCOUNT_MSG)

    def can_transact(self):
        return self.is_visible(self.DEPOSIT_TAB, timeout=2)

    def _info(self):
        return [e.text.strip() for e in self.find_all(self.ACCOUNT_INFO)]

    def account_number(self):
        return self._info()[0]

    def balance(self):
        self.find(self.ACCOUNT_INFO)
        return int(float(self._info()[1]))

    def currency(self):
        return self._info()[2]

    @allure.step("Select account {account_number}")
    def select_account(self, account_number):
        self.select_by_text(self.ACCOUNT_SELECT, str(account_number))
        return self

    # ---- money movement --------------------------------------------------
    def _submit_amount(self, amount):
        self.type(self.AMOUNT, amount)
        self.click(self.SUBMIT)

    @allure.step("Deposit {amount}")
    def deposit(self, amount):
        self.click(self.DEPOSIT_TAB)
        self.wait_for_text(self.FORM_LABEL, "Deposited")
        self._submit_amount(amount)
        return self

    @allure.step("Withdraw {amount}")
    def withdraw(self, amount):
        self.click(self.WITHDRAW_TAB)
        self.wait_for_text(self.FORM_LABEL, "Withdrawn")
        self._submit_amount(amount)
        return self

    def message(self, timeout=3):
        """Text of the status message, or '' if none is shown."""
        if self.is_visible(self.MESSAGE, timeout=timeout):
            return self.text_of(self.MESSAGE)
        return ""

    def amount_validation_message(self):
        return self.find(self.AMOUNT).get_attribute("validationMessage")

    # ---- navigation ------------------------------------------------------
    @allure.step("Log out")
    def logout(self):
        from pages.customer_login_page import CustomerLoginPage
        self.click(self.LOGOUT)
        return CustomerLoginPage(self.driver).wait_loaded()