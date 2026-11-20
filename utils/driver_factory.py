"""Creates a local or remote WebDriver based on utils.config."""
from selenium import webdriver

from utils import config


def _chrome_options():
    options = webdriver.ChromeOptions()
    if config.HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return options


def _firefox_options():
    options = webdriver.FirefoxOptions()
    if config.HEADLESS:
        options.add_argument("-headless")
    options.add_argument("--width=1920")
    options.add_argument("--height=1080")
    return options


def create_driver():
    if config.BROWSER == "firefox":
        options = _firefox_options()
        local = webdriver.Firefox
    else:
        options = _chrome_options()
        local = webdriver.Chrome

    if config.SELENIUM_REMOTE_URL:
        driver = webdriver.Remote(command_executor=config.SELENIUM_REMOTE_URL, options=options)
    else:
        driver = local(options=options)  
    driver.set_page_load_timeout(60)
    return driver