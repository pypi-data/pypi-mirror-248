import logging
import os
import subprocess

from vicky.clients import VickyAPIClient
from vicky.exceptions import ImproperlyConfigured
from vicky.utils import encode_file, encode_templates_to_dict

logger = logging.getLogger(__name__)


class Deployment:
    def __init__(
        self,
        theme: str,
        directory: str,
        custom_css=None,
        custom_js=None,
        api_key=None,
        version=None,
        *args,
        **kwargs
    ):
        self.theme = theme
        self.directory = directory
        self.custom_css = custom_css
        self.custom_js = custom_js
        self.api_key = api_key if api_key else self.get_api_key()
        self.version = version if version else self.get_version()
        self.client = self.get_client()

    def run(self):
        encoded_templates = encode_templates_to_dict(self.directory)
        res = self.client.update_themes(self.theme, encoded_templates)
        logger.info("Successfully updated themes")

        if self.custom_css or self.custom_js:
            settings = {}
            if self.custom_css:
                settings["custom_css"] = encode_file(self.custom_css)
            if self.custom_js:
                settings["custom_js"] = encode_file(self.custom_js)
            res = self.client.update_settings(self.theme, settings)
            logger.info("Successfully updated settings")

    def get_client(self):
        client = VickyAPIClient(self.api_key)
        return client

    def get_api_key(self):
        api_key = os.getenv("VICKY_API_KEY")
        if not api_key:
            raise ImproperlyConfigured(
                "The VICKY_API_KEY environment variable must be set."
            )
        return api_key

    def get_version(self):
        process = subprocess.Popen(
            ["git", "rev-parse", "--short", "HEAD"],
            shell=False,
            stdout=subprocess.PIPE,
        )
        git_short_hash = process.communicate()[0].strip()
        version = git_short_hash.decode()
        return version
