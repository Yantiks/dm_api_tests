from datetime import datetime

import requests
from hamcrest import assert_that, has_property, starts_with, all_of, instance_of, has_properties, equal_to
from contextlib import contextmanager
from requests.exceptions import HTTPError


@contextmanager
def check_status_code_http(expected_status_code: requests.codes = requests.codes.OK, expected_message: str = ''):
    try:
        yield
    except HTTPError as e:
        assert e.response.status_code == expected_status_code
        assert e.response.json()['title'] == expected_message


def test_get_v1_account(auth_account_helper):
    with check_status_code_http():
        response = auth_account_helper.get_client()
    assert_that(response,
                all_of(
                    has_property('resource', has_property('login', starts_with('yantik'))),
                    has_property('resource', has_property('online', instance_of(datetime))),
                    has_property(
                        'resource', has_properties(
                            {
                                'settings': has_properties(
                                    {
                                        'paging': has_properties(
                                            {
                                                'commentsPerPage': equal_to(10),
                                                'entitiesPerPage': equal_to(10),
                                                'messagesPerPage': equal_to(10),
                                                'postsPerPage': equal_to(10),
                                                'topicsPerPage': equal_to(10),
                                            }
                                        )
                                    }
                                )

                            }
                        )
                    )
                )
                )


def test_get_v1_account_no_auth(account_helper):
    with check_status_code_http(401, 'User must be authenticated'):
        account_helper.get_client()
