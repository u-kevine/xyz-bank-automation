import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage


class TransactionsPage(BasePage):
    ROWS = (By.CSS_SELECTOR, "table tbody tr")
    BACK = (By.XPATH, "//button[@ng-click='back()']")
    RESET = (By.XPATH, "//button[@ng-click='reset()']")

    def wait_loaded(self):
        self.find(self.BACK)
        return self

    def transactions(self):
        """Rows as dicts: date_time, amount (int), type ('Credit' / 'Debit')."""
        result = []
        for row in self.find_all(self.ROWS):
            cells = [c.text.strip() for c in row.find_elements(By.TAG_NAME, "td")]
            if len(cells) >= 3:
                result.append({"date_time": cells[0], "amount": int(float(cells[1])),
                               "type": cells[2]})
        return result

    @allure.step("Wait for at least {count} transaction(s)")
    def wait_for_transactions(self, count, attempts=3):
        """A transaction made a moment ago can be missing from the list the first time it
        opens. Re-open the view (Back -> Transactions) until it shows up."""
        from pages.account_page import AccountPage
        for _ in range(attempts):
            try:
                WebDriverWait(self.driver, 3).until(lambda d: len(self.transactions()) >= count)
                return self.transactions()
            except TimeoutException:
                self.click(self.BACK)
                AccountPage(self.driver).wait_loaded().click(AccountPage.TRANSACTIONS_TAB)
                self.wait_loaded()
        return self.transactions()

    def reset_visible(self):
        return self.is_visible(self.RESET, timeout=2)

    @allure.step("Click Reset")
    def reset(self):
        self.click(self.RESET)
        return self

    @allure.step("Go back to account")
    def back(self):
        from pages.account_page import AccountPage
        self.click(self.BACK)
        return AccountPage(self.driver).wait_loaded()