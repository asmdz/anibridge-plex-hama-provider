"""Utility module."""

import warnings
from logging import Logger
from urllib.parse import urlparse

import requests
from urllib3.exceptions import InsecureRequestWarning

__all__ = ["SelectiveVerifySession"]


class SelectiveVerifySession(requests.Session):
    """Session that selectively disables SSL verification for whitelisted domains."""

    def __init__(self, whitelist=None, *, logger: Logger) -> None:
        """Initialize the session with a whitelist of domains."""
        super().__init__()
        self.log = logger
        self.whitelist = set(whitelist or [])
        if self.whitelist:
            self.log.debug(
                "SSL verify disabled for domains: "
                + ", ".join([f"$$'{d}'$$" for d in sorted(self.whitelist)])
            )

    def request(self, method, url, *_, **kwargs):
        """Override the request method to selectively disable SSL verification."""
        domain = urlparse(url).hostname
        # Disable SSL verification for whitelisted domains
        if domain in self.whitelist:
            kwargs["verify"] = False
            # Suppress SSL warnings
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", InsecureRequestWarning)
                return super().request(method, url, **kwargs)
        return super().request(method, url, *_, **kwargs)
