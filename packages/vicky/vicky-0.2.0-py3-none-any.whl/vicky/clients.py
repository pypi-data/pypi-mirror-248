import json
import os

import requests

from vicky.exceptions import ClientError, ImproperlyConfigured


class VickyAPIClient:
    def __init__(self, api_key: str, base_url: str = "http"):
        self.api_key = api_key
        self.base_url = self.get_base_url()

    def update_themes(self, theme: str, templates: dict) -> dict:
        url = f"{self.base_url}/theme-builder/themes/{theme}/"
        headers = self.get_headers()
        data = json.dumps(
            {
                "templates": templates,
            }
        )
        res = requests.post(url, headers=headers, data=data)
        return res.json()

    def update_settings(self, theme: str, settings: dict) -> dict:
        url = f"{self.base_url}/theme-builder/themes/{theme}/settings/"
        headers = self.get_headers()
        data = json.dumps(settings)
        res = requests.post(url, headers=headers, data=data)
        return res.json()

    def get_headers(self):
        return {
            "x-theme-builder-api-key": self.api_key,
            "Content-Type": "application/json",
        }

    def get_base_url(self):
        base_url = os.getenv("VICKY_BASE_URL")
        if not base_url:
            raise ImproperlyConfigured(
                "The VICKY_BASE_URL environment variable must be set."
            )
        return base_url
