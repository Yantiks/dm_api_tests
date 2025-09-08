import requests
from contextlib import contextmanager
from requests.exceptions import HTTPError


@contextmanager
def check_status_code_http(expected_status_code: requests.codes = requests.codes.OK, expected_message: str = ''):
    try:
        yield
        if expected_status_code != requests.codes.ok:
            raise AssertionError(f"Expected status code {expected_status_code}")
        if expected_message:
            raise AssertionError(f"Expected message {expected_message}, but got OK")
    except HTTPError as e:
        assert e.response.status_code == expected_status_code
        assert e.response.json()['title'] == expected_message
