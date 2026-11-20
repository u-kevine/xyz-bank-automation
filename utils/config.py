"""Central configuration. Every value can be overridden with an environment variable."""
import os

BASE_URL = os.getenv(
    "BASE_URL",
    "https://www.globalsqa.com/angularJs-protractor/BankingProject/#/login",
)
BROWSER = os.getenv("BROWSER", "chrome").lower()          
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
SELENIUM_REMOTE_URL = os.getenv("SELENIUM_REMOTE_URL")      
TIMEOUT = int(os.getenv("TIMEOUT", "10"))                    