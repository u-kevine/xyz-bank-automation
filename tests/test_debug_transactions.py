import time

import pytest
from selenium.webdriver.common.by import By

DATE_INPUTS = (By.XPATH, "//input[@type='datetime-local']")


@pytest.mark.parametrize("run", range(1, 6))
def test_debug_withdrawal_listed(account, run):
    driver = account.driver
    account.deposit(250)
    account.withdraw(50)

    page = account.open_transactions()
    time.sleep(2)                                   # let the table render; diagnostic only
    rows = page.transactions()

    filters = [i.get_attribute("value") for i in driver.find_elements(*DATE_INPUTS)]
    browser_now = driver.execute_script("return new Date().toString()")
    print(f"\n--- run {run} ---")
    print(f"rows on open : {rows}")
    print(f"start / end  : {filters}")
    print(f"browser now  : {browser_now}")

    if not rows:
        driver.save_screenshot(f"debug_empty_run{run}.png")
        driver.refresh()
        time.sleep(3)
        print(f"after refresh: {page.transactions()}")
