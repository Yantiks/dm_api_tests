from datetime import datetime
from hamcrest import assert_that, has_property, starts_with, all_of, instance_of, has_properties, equal_to


def test_get_v1_account(auth_account_helper):
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
