from utils.config import BASE_URL
from utils.driver_factory import create_driver


def test_app_opens():
    driver = create_driver()
    try:
        driver.get(BASE_URL)
        assert "XYZ Bank" in driver.page_source
    finally:
        driver.quit()