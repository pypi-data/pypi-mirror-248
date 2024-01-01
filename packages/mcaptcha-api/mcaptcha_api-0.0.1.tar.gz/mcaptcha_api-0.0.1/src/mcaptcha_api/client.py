# SPDX-FileCopyrightText: 2023 Aravinth Manivannan <realaravinth@batsense.net>
#
# SPDX-License-Identifier: Apache-2.0
# SPDX-License-Identifier: MIT

from urllib.parse import urlparse, urlunparse
from requests import Session


class MCaptcha:
    def __init__(self, instance_url: str, sitekey: str, secret: str):
        self.client = Session()
        self.instance_url = self.__clean_url(instance_url)
        self.sitekey = sitekey
        self.secret = secret
        self.verify_url = self.__set_path(self.instance_url, "/api/v1/pow/siteverify")

    def __clean_url(self, url):
        parsed = urlparse(url)
        return urlunparse((parsed.scheme, parsed.netloc, "", "", "", ""))

    def __set_path(self, url: str, path: str) -> str:
        parsed = urlparse(url)
        return urlunparse((parsed.scheme, parsed.netloc, path, "", "", ""))

    def verify(self, token: str) -> bool:
        payload = {"token": token, "key": self.sitekey, "secret": self.secret}
        resp = self.client.post(self.verify_url, json=payload)
        assert resp.status_code == 200
        return resp.json()["valid"]
