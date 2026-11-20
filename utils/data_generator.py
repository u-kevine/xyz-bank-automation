"""Generates unique, valid customer data so tests never collide."""
import random
import string


def _letters(n=6):
    return "".join(random.choices(string.ascii_lowercase, k=n))


def unique_customer(first_name="Test", last_name="Customer", post_code="10001"):
    """Names stay alphabetic-only, as the acceptance criteria require."""
    return {
        "first_name": f"{first_name}{_letters()}",
        "last_name": f"{last_name}{_letters(4)}",
        "post_code": post_code,
    }


def full_name(customer):
    return f"{customer['first_name']} {customer['last_name']}"