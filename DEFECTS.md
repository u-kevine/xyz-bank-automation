# Defect Log

| ID | Title | Severity | Status | Found by |
|---|---|---|---|---|
| DEF-01 | Customer name accepts digits and special characters | High | Open | `test_reject_non_alphabetic_names` |
| DEF-02 | Postcode accepts non-numeric characters | High | Open | `test_reject_non_numeric_post_code` |

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
- **Environment:** Chrome (headless), XYZ Bank demo site,