# Defect Log

| ID | Title | Severity | Status | Found by |
|---|---|---|---|---|
| DEF-01 | Customer name accepts digits and special characters | High | Open | `test_reject_non_alphabetic_names` |
| DEF-02 | Postcode accepts non-numeric characters | High | Open | `test_reject_non_numeric_post_code` |
| DEF-03 | Customer can reset (erase) their transaction history | Critical | Open | `test_history_cannot_be_reset` |
| DEF-04 | Transaction history shows nothing when opened within the same second as a transaction | Medium | Open | Diagnostic runs (timing-dependent, no automated test) |

---

## DEF-01: Customer name accepts digits and special characters

- **Requirement:** US1, Adding Customers: names should only contain alphabetic characters.
- **Severity:** High (invalid data is stored in the system).
- **Steps to reproduce:**
  1. Open the app and click **Bank Manager Login**.
  2. Click **Add Customer**.
  3. Enter First Name `Ada123`, Last Name `Love@ce!`, Post Code `10001`.
  4. Click **Add Customer**.
- **Expected:** The customer is rejected with a validation message.
- **Actual:** Alert "Customer added successfully with customer id :6". The customer appears in the Customers list.
- **Test data that reproduces it:** `Ada123`, `Love@ce!`, `J0hn#` / `D0e$`.
- **Environment:** Chrome (headless), XYZ Bank demo site.

## DEF-02: Postcode accepts non-numeric characters

- **Requirement:** US1, Adding Customers: postal codes should only contain numeric characters.
- **Severity:** High (invalid data is stored in the system).
- **Steps to reproduce:**
  1. Open the app and click **Bank Manager Login**.
  2. Click **Add Customer**.
  3. Enter First Name `Ada`, Last Name `Lovelace`, Post Code `ABCDE`.
  4. Click **Add Customer**.
- **Expected:** The customer is rejected with a validation message.
- **Actual:** Alert "Customer added successfully with customer id :6".
- **Test data that reproduces it:** `E1A2B`, `ABCDE`, `12-34`.
- **Environment:** Chrome (headless), XYZ Bank demo site.

## DEF-03: Customer can reset (erase) their transaction history

- **Requirement:** US2, Transaction Security: customers should not be able to reset or alter their transaction history.
- **Severity:** Critical (financial records can be erased by the account holder).
- **Steps to reproduce:**
  1. Log in as a customer with an account.
  2. Click **Deposit**, enter `250`, click **Deposit**.
  3. Click **Transactions**. One Credit row of 250 is listed.
  4. Click **Reset**.
- **Expected:** No Reset option, or the history is unchanged.
- **Actual:** All transactions disappear from the list. Balance after Reset: <fill in from your manual check>.
- **Environment:** Chrome (headless), XYZ Bank demo site.

## DEF-04: Transaction history shows nothing when opened within the same second as a transaction

- **Requirement:** US2, Viewing Transactions: customers should be able to view a list of their recent transactions.
- **Severity:** Medium (the customer sees an empty history; the data itself is not lost).
- **Steps to reproduce:**
  1. Log in as a customer with an account.
  2. Deposit `250`.
  3. Click **Transactions** within the same clock second as the deposit (achievable by automation or a fast user).
- **Expected:** The deposit is listed.
- **Actual:** The table is empty. Also seen when the first and last transactions fall in the same second.
- **Evidence (8 instrumented runs, page data read from the AngularJS scope):**
  - In every run the page held both transactions (`transactions` = 2), including when the table was empty,
    so the data exists but is hidden.
  - When the table was empty, the End date filter (`end`) had no valid value; when it showed rows, `end` was set.
  - Opening Transactions immediately: 4/4 empty. Opening 3 s later: 4/4 listed.
  - Example failing run: last transaction `17:28:31.218`, End filter limit `maxEDate` `17:28:31.658` (same second).
- **Likely cause (inferred, not confirmed in source):** the date-filter validation compares limits to the second,
  so a value later in the same second is treated as out of range and discarded, which empties the list.
- **Reproducibility:** Timing-dependent, so there is no reliable automated regression test.
  Tests that open the history keep each step in a new second (`wait_for_new_second()`).
- **Screenshot:** `docs/evidence/DEF-04_empty_history.png`.
- **Environment:** Chrome (headless), XYZ Bank demo site.
