import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.manager_page import ManagerPage
from utils.config import BASE_URL

from pages.customer_login_page import CustomerLoginPage


class HomePage(BasePage):
    CUSTOMER_LOGIN = (By.XPATH, "//button[@ng-click='customer()']")
    MANAGER_LOGIN = (By.XPATH, "//button[@ng-click='manager()']")
    HOME_BUTTON = (By.CSS_SELECTOR, "button.home")

    @allure.step("Open XYZ Bank home page")
    def open(self):
        self.driver.get(BASE_URL)
        self.find(self.MANAGER_LOGIN)
        return self

    @allure.step("Go to home page")
    def go_home(self):
        self.click(self.HOME_BUTTON)
        self.find(self.MANAGER_LOGIN)
        return self

    @allure.step("Log in as Bank Manager")
    def login_as_manager(self):
        self.click(self.MANAGER_LOGIN)
        return ManagerPage(self.driver).wait_loaded()

    @allure.step("Go to Customer Login")
    def go_to_customer_login(self):
        self.click(self.CUSTOMER_LOGIN)
        return CustomerLoginPage(self.driver).wait_loaded()