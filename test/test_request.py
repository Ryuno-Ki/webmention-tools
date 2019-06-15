import unittest

import pytest
import requests

import webmentiontools
from webmentiontools.request import (
    is_successful_response,
    request_get_url,
    request_head_url,
    request_post_url,
    user_agent
)

from .endpoints import WEBMENTION_ROCKS_TESTS


class RequestTestCase(unittest.TestCase):
    def test_user_agent(self):
        assert "Webmention Tools" in user_agent
        assert webmentiontools.__version__ in user_agent
        assert "requests" in user_agent
        assert requests.__version__ in user_agent

    @pytest.mark.integration
    def test_is_successful_response(self):
        for test in WEBMENTION_ROCKS_TESTS:
            response = request_head_url(test["url"])
            is_successful = is_successful_response(response)
            assert is_successful is True

    @pytest.mark.integration
    def test_request_head_url(self):
        for test in WEBMENTION_ROCKS_TESTS:
            if test["source"] == "header":
                response = request_head_url(test["url"])
                assert isinstance(response, requests.models.Response)

    @pytest.mark.integration
    def test_request_get_url(self):
        for test in WEBMENTION_ROCKS_TESTS:
            if test["source"] == "html":
                response = request_get_url(test["url"])
                assert isinstance(response, requests.models.Response)

    @pytest.mark.integration
    def test_request_post_url(self):
        source_url = "http://example.com"
        endpoint = WEBMENTION_ROCKS_TESTS[0]["url"]
        TARGETS = [
            "https://webmention.rocks/update/1",
            "https://webmention.rocks/update/1/part/2"
        ]

        for target_url in TARGETS:
            response = request_post_url(endpoint, source_url, target_url)
            assert isinstance(response, requests.models.Response)
