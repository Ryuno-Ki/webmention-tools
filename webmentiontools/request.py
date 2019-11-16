"""
Wrapper around requests
"""
from typing import Optional

import requests

import webmentiontools


USER_AGENT: str = "Webmention Tools/{} requests/{}".format(
    webmentiontools.__version__,
    requests.__version__
)


def is_successful_response(response: requests.models.Response) -> bool:
    """
    Checks status code of response for success.

    :param response: The response to check.
    :type response: requests.models.Response
    :return: Was response successful?
    :rtype: bool
    """
    accepted_status_code = str(response.status_code).startswith("2")
    content_type: Optional[str] = response.headers.get("content-type")

    accepted_content_type: bool = False
    if content_type is not None:
        accepted_content_type = content_type.startswith("text/html")
    return accepted_status_code and accepted_content_type


def request_head_url(url: str) -> requests.models.Response:
    """
    Makes a HEAD request against the url.

    :param url: The URL to send request to.
    :type url: str
    :return: Network response.
    :rtype: requests.models.Response
    """
    return requests.head(
        url,
        allow_redirects=True,
        headers={"User-Agent": USER_AGENT}
    )


def request_get_url(url: str) -> requests.models.Response:
    """
    Makes a GET request against the url.

    :param url: The URL to send request to.
    :type url: str
    :return: Network response.
    :rtype: requests.models.Response
    """
    return requests.get(
        url,
        allow_redirects=True,
        headers={"User-Agent": USER_AGENT}
    )


def request_post_url(
        endpoint: str,
        source_url: str,
        target_url: str) -> requests.models.Response:
    """
    Makes a POST request against the endpoint.

    :param endpoint: The URL to send request to.
    :param source_url: URL of page containing a Webmention.
    :param target_url: URL of reference in source_url
    :type endpoint: str
    :type source_url: str
    :type target_url: str
    :return: Network response.
    :rtype: requests.models.Response
    """
    payload = {"source": source_url, "target": target_url}
    return requests.post(
        endpoint,
        data=payload,
        allow_redirects=True,
        # type/* should be fine according to
        # https://tools.ietf.org/html/rfc7231#section-5.3.2
        # c.f. https://github.com/Ryuno-Ki/webmention-tools/issues/31
        headers={
            "Accept": "text/*, application/*",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": USER_AGENT
        }
    )
