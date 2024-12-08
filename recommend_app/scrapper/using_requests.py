"""
Use requests module to load the url and call scrapper to scrap the data.

Alternate is to use Selenium. We may use Selenium in the future but for now,
requests is sufficient.
"""

# Builtin imports
from typing import Optional

# Project specific imports
import requests

# Local imports
from ..exceptions import RecommendAppError
from .scrapper import Scrapper

# -----------------------------------------------------------------------------#
# Functions
# -----------------------------------------------------------------------------#


def get_request_header() -> dict[str, str]:
    """
    Return the request header
    """
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Referer": "https://www.google.com/",
        "Sec-Ch-Ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        "Sec-Fetch-Site": "cross-site",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    }

    return headers


def scrap(url: str) -> dict[str, Optional[str]]:
    """
    Use requests module to scrap the data
    """
    try:
        response = requests.get(url, headers=get_request_header())
    except requests.exceptions.MissingSchema as err:
        raise RecommendAppError(f"Invalid URL: {url}") from err

    if response.status_code != 200:
        raise RecommendAppError(
            f"{url} returned a response code - {response.status_code}"
        )

    scrapper = Scrapper(response.text)
    return scrapper.scrap()
