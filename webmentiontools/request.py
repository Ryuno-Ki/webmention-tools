import requests

import webmentiontools


user_agent = "Webmention Tools/{} requests/{}".format(
    webmentiontools.__version__,
    requests.__version__
)

def is_successful_response(response):
    """
    Checks status code of response for success.

    :param response: The response to check.
    :type response: requests.models.Response
    :return: Was response successful?
    :rtype: bool
    """
    accepted_status_code = str(response.status_code).startswith("2")
    accepted_content_type = response.headers.get("content-type").startswith("text/html")
    return accepted_status_code and accepted_content_type

def request_head_url(url):
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
        headers={"User-Agent": user_agent}
    )

def request_get_url(url):
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
        headers={"User-Agent": user_agent}
    )

def request_post_url(endpoint, source_url, target_url):
    """
    Makes a POST request against the endpoint.

    :param endpoint: The URL to send request to.
    :param source_url: URL of page containing a webmention.
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
        headers={"User-Agent": user_agent}
    )
