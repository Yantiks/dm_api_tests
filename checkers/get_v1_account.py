from datetime import datetime
from hamcrest import assert_that, has_property, starts_with, all_of, instance_of, has_properties, equal_to


class GetV1Account():
    @classmethod
    def check_response_values(cls, response):
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