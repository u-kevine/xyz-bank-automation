# XYZ Bank – Selenium WebDriver Test Automation

Automated UI tests for the [XYZ Bank app](https://www.globalsqa.com/angularJs-protractor/BankingProject/),
covering User Story 1 (Bank Manager) and User Story 2 (Customer).

**Stack:** Python · pytest · Selenium 4 · Page Object Model · Allure · Docker · GitHub Actions

## Project structure

```
xyz-bank-automation/
├── .github/workflows/ci.yml     # CI: build, run in Docker, Allure report, GitHub Pages
├── allure_config/
│   └── categories.json          # groups results: known defects, new failures, broken tests
├── docs/evidence/               # screenshots supporting defect reports
├── pages/                       # Page Object Model: all locators and page actions
│   ├── base_page.py             # shared waits, clicks, typing, dropdowns, alerts
│   ├── home_page.py
│   ├── manager_page.py          # manager tabs
│   ├── add_customer_page.py
│   ├── open_account_page.py
│   ├── customers_page.py        # search and delete
│   ├── customer_login_page.py
│   ├── account_page.py          # balance, deposit, withdraw, logout
│   └── transactions_page.py
├── test_data/test_data.json     # inputs and expected messages
├── tests/                       # tests grouped by user story and feature
├── utils/
│   ├── config.py                # settings from environment variables
│   ├── driver_factory.py        # local or remote (Docker) browser
│   ├── data_loader.py           # reads test_data.json
│   └── data_generator.py        # unique, letters-only customer names
├── conftest.py                  # fixtures, screenshots, Allure environment
├── DEFECTS.md                   # defect log with reproduction steps and evidence
├── Dockerfile                   # test-runner image
├── docker-compose.yml           # test runner + Selenium standalone Chrome
├── pytest.ini
└── requirements.txt
```

## Coverage

| User story | Area | Tests |
|---|---|---|
| US1 Bank Manager | Login, add customer (valid, invalid names, invalid postcodes, required fields, duplicates) | `test_manager_login.py`, `test_manager_add_customer.py` |
| US1 Bank Manager | Open account (each currency), no access without account, search, delete, no access after delete | `test_manager_accounts.py` |
| US2 Customer | Login, logout | `test_customer_login.py` |
| US2 Customer | Deposit (valid, zero, negative) | `test_customer_deposit.py` |
| US2 Customer | Withdraw (within, exact, above balance, zero, negative) | `test_customer_withdraw.py` |
| US2 Customer | Transactions listed, history cannot be reset | `test_customer_transactions.py` |

## Run locally

Requires Python 3.12+ and Google Chrome.

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

pytest                              # full suite (headless by default)
pytest -m smoke                     # smoke tests only
HEADLESS=false pytest               # watch the browser (needs a screen)
BROWSER=firefox pytest              # run in Firefox
```

Selenium Manager downloads the matching browser driver automatically.

## Run in Docker

```bash
mkdir -p allure-results
docker compose up --build --abort-on-container-exit --exit-code-from tests
docker compose down
```

Run a subset: `docker compose run --rm tests pytest -p no:cacheprovider -m smoke`.
Watch the browser live at port 7900 (noVNC, password `secret`).

## Allure report

Requires Java 11+ and the Allure CLI (`npm install -g allure-commandline`).

```bash
allure generate allure-results --clean -o allure-report
allure open allure-report
```

The report includes results by user story and severity, step-by-step logs, a screenshot and URL
for every failure and known defect, the run environment, defect categories and links to `DEFECTS.md`.

## CI/CD

On every push and pull request to `main`, GitHub Actions builds the images, runs the suite in Docker,
generates the Allure report with trend history, posts a results summary on the run, and (for `main`)
publishes the report to GitHub Pages. It can also be run manually from the **Actions** tab.

## Known defects

Tests for acceptance criteria the app does not meet are marked `xfail` with the defect ID.
`xfail_strict` and `raises=AssertionError` make sure that an xfail only counts when the assertion fails
(the defect), and that a fixed defect fails the build so its marker gets removed.

| Defect | Severity | Summary | Test |
|---|---|---|---|
| DEF-01 | High | Customer names accept digits and special characters | `test_reject_non_alphabetic_names` |
| DEF-02 | High | Postcodes accept non-numeric characters | `test_reject_non_numeric_post_code` |
| DEF-03 | Critical | Customer can reset (erase) transaction history | `test_history_cannot_be_reset` |
| DEF-04 | Medium | History shows nothing when opened within the same second as a transaction | none (timing-dependent; see `DEFECTS.md`) |

Full reproduction steps and evidence are in [DEFECTS.md](DEFECTS.md).

## Design decisions

- **Fresh browser per test.** The app keeps data in memory, so every test starts from the same state and no test depends on another.
- **Explicit waits only.** `BasePage` waits for elements and conditions; the one timed wait, `wait_for_new_second()`, works around DEF-04 and is called explicitly where needed.
- **Unique generated data.** New customers get random letters-only names, so tests never collide and never break the name rule they test.
- **Page objects act, tests judge.** Page methods return results (alert text, balances, rows); only tests make assertions.