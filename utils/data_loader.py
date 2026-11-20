"""Loads static test data from test_data/test_data.json."""
import json
from functools import lru_cache
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "test_data" / "test_data.json"


@lru_cache(maxsize=1)
def load_test_data():
    with open(DATA_FILE, encoding="utf-8") as f:
        return json.load(f)


def get(section):
    return load_test_data()[section]