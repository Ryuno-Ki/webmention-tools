#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sending a Webmention.
"""
import logging
from typing import Optional
import warnings

import requests

from webmentiontools.discover import WebmentionDiscover
from webmentiontools.request import request_post_url

LOGGER = logging.getLogger(__name__)
VALID_STATUS_CODES = (201, 202)
ACCEPTED_STATUS_CODES = (200, )
STATUS_CODES = VALID_STATUS_CODES + ACCEPTED_STATUS_CODES


class WebmentionSend:
    """
    Sends or updates a Webmention.
    """
    def __init__(self,  # pylint: disable=too-many-arguments
                 from_url: str,
                 to_url: str,
                 source=None,
                 target=None,
                 endpoint=None) -> None:
        if source is not None:
            warnings.warn(
                "'source' argument is deprecated. Use 'from_url' instead.",
                PendingDeprecationWarning
            )

        if target is not None:
            warnings.warn(
                "'target' argument is deprecated. Use 'to_url' instead.",
                PendingDeprecationWarning
            )

        if endpoint is not None:
            warnings.warn(
                "'endpoint' argument is obsolete and thus ignored.",
                DeprecationWarning
            )

        self.from_url: str = from_url
        self.to_url: str = to_url
        self.discover: WebmentionDiscover = WebmentionDiscover(to_url)

    def send_notification(self) -> bool:
        """
        Sends a notification to the target server to trigger a Webmention
        comment.

        :returns: Was notification successful?
        :rtype: bool
        """
        endpoint: Optional[str] = self.discover.discover()

        if endpoint is None:
            logging.error("No Webmention endpoint found")
            return False

        response: requests.models.Response = request_post_url(
            endpoint,
            self.from_url,
            self.to_url)

        if int(response.status_code) in STATUS_CODES:
            return True

        LOGGER.error("Received status code %s", str(response.status_code))
        LOGGER.debug(response.text)
        return False

    def delete_webmention(self) -> bool:
        """
        Sends a notification to the target server to trigger removal of a
        Webmention comment.

        :returns: Was Webmention comment successfully removed?
        :rtype: bool
        """
        return self.send_notification()

    # c.f. http://pylint-messages.wikidot.com/all-messages
    # unused-argument = W0613
    # no-self-use = R0201
    def send(self, **kwargs) -> None:  # pylint: disable=W0613, R0201
        """
        Method is obsolete.
        """
        warnings.warn(
            "'WebmentionSend.send()' is obsolete. "
            "Did you meant to use WebmentionSend.send_notification()?",
            DeprecationWarning
        )
