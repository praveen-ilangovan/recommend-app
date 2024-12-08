"""
Scraps the information from a webpage using beautifulsoup
"""

# Builtin imports
import json
from typing import Optional

# Project specific imports
from bs4 import BeautifulSoup

# -----------------------------------------------------------------------------#
# Class
# -----------------------------------------------------------------------------#


class Scrapper:
    """
    Takes in the html content and scraps the information

    Args:
        content (str): Content of a webpage
    """

    def __init__(self, content: str):
        self.__soup = BeautifulSoup(content, "lxml")

        # Keys we need to extract from the webpage
        self.__keys = ["url", "title", "description", "thumbnail"]

        # Dictionary to keep track of extracted information until we return it
        # as a NewCard
        self.__extracted: dict[str, Optional[str]] = {}

    # -------------------------------------------------------------------------#
    # Methods
    # -------------------------------------------------------------------------#
    def scrap(self) -> dict[str, Optional[str]]:
        """
        Scrap and returns the information as a data model.

        Tries extracting this information from different tags. Starts of with
        the ld+json tag. If that tag isn't available or only a set of keys were
        available, the code fallsback to og meta tags. It then fallsback to meta
        tags and finally opts to extract the webpage title at the least.

        Returns:
            Dict
        """
        for method in (
            self.__from_ldjson,
            self.__from_og,
            self.__from_meta,
            self.__get_title,
        ):
            method()
            if not self.__keys:
                break

        return self.__extracted

    # -------------------------------------------------------------------------#
    # Methods: Privates
    # -------------------------------------------------------------------------#
    def __from_ldjson(self) -> None:
        """
        Extract the data from the ld+json tag
        """
        schema = self.__soup.find("script", type="application/ld+json")
        if not schema:
            return

        mapper = {
            "url": "url",
            "title": "name",
            "description": "description",
            "thumbnail": "image",
        }
        schema_dict = json.loads(schema.text)
        for key, schema_key in mapper.items():
            if schema_key in schema_dict:
                self.__extracted[key] = schema_dict[schema_key]
                self.__keys.remove(key)

    def __from_og(self) -> None:
        """
        Extract the data from the og tag
        """
        mapper = {
            "url": "og:url",
            "title": "og:title",
            "description": "og:description",
            "thumbnail": "og:image",
        }

        for key, og_key in mapper.items():
            if key not in self.__keys:
                continue

            prop = self.__soup.find("meta", property=og_key, content=True)
            if not prop:
                continue

            self.__extracted[key] = prop["content"]  # type: ignore
            self.__keys.remove(key)

    def __from_meta(self) -> None:
        """
        Use meta tag to extract the data
        """
        mapper = {"title": "title", "description": "description"}
        for key, meta_key in mapper.items():
            if key not in self.__keys:
                continue

            meta = self.__soup.find("meta", attrs={"name": meta_key}, content=True)
            if not meta:
                continue

            self.__extracted[key] = meta["content"]  # type: ignore
            self.__keys.remove(key)

    def __get_title(self) -> None:
        """
        If nothing works, atleast try to retrieve the title of the page
        """
        if "title" not in self.__keys or not self.__soup.title:
            return

        self.__extracted["title"] = self.__soup.title.text
        self.__keys.remove("title")
