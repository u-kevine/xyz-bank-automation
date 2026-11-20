import allure
from selenium.webdriver.common.by import By

from pages.manager_page import ManagerPage


class CustomersPage(ManagerPage):
    SEARCH = (By.XPATH, "//input[@ng-model='searchCustomer']")
    ROWS = (By.CSS_SELECTOR, "table tbody tr")
    DELETE_BUTTON = (By.CSS_SELECTOR, "button[ng-click='deleteCust(cust)']")
    CELLS = (By.TAG_NAME, "td")

    def wait_loaded(self):
        self.find(self.SEARCH)
        return self

    @allure.step("Search customers for '{text}'")
    def search(self, text):
        self.type(self.SEARCH, text)
        return self

    def rows(self):
        """Each row as a dict: first_name, last_name, post_code, accounts."""
        result = []
        for row in self.find_all(self.ROWS):
            cells = [c.text.strip() for c in row.find_elements(*self.CELLS)]
            if len(cells) >= 4:
                result.append({"first_name": cells[0], "last_name": cells[1],
                               "post_code": cells[2], "accounts": cells[3].split()})
        return result

    def find_customer(self, first_name, last_name):
        self.search(first_name)
        for row in self.rows():
            if row["first_name"] == first_name and row["last_name"] == last_name:
                return row
        return None

    @allure.step("Delete customer {first_name} {last_name}")
    def delete_customer(self, first_name, last_name):
        self.search(first_name)
        for row in self.find_all(self.ROWS):
            cells = [c.text.strip() for c in row.find_elements(*self.CELLS)]
            if cells[:2] == [first_name, last_name]:
                row.find_element(*self.DELETE_BUTTON).click()
                return True
        return False