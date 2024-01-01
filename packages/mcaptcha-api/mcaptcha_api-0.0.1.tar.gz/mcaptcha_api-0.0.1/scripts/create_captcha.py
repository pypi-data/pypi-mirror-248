# SPDX-FileCopyrightText: 2023 Aravinth Manivannan <realaravinth@batsense.net>
#
# SPDX-License-Identifier: Apache-2.0
# SPDX-License-Identifier: MIT

import sys
from urllib.parse import urlparse, urlunparse, urlencode, parse_qsl
from requests import Session


def clean_url(url):
    parsed = urlparse(url)
    return urlunparse((parsed.scheme, parsed.netloc, "", "", "", ""))


def set_path(url: str, path: str) -> str:
    parsed = urlparse(url)
    return urlunparse((parsed.scheme, parsed.netloc, path, "", "", ""))


def help():
    print("Usage: create_captcha.py <option>")
    print("OPTIONS:\ncreate_captcha <mcaptcha_instance_url> <username> <password>")
    print("get_secret <mcaptcha_instance_url> <username> <password>")
    print("widget_url <mcaptcha_instance_url> <sitekey>")


c = Session()
if len(sys.argv) < 1:
    help()
    exit(1)

option = sys.argv[1]


def login():
    if len(sys.argv) < 4:
        help()
        exit(1)

    instance_url = clean_url(sys.argv[2])
    username = sys.argv[3]
    password = sys.argv[4]

    url = set_path(instance_url, "/api/v1/signin")
    payload = {"login": username, password: password}
    resp = c.post(url, json=payload)
    assert resp.status_code == 200


def create_captcha():
    instance_url = clean_url(sys.argv[2])
    username = sys.argv[3]
    password = sys.argv[4]

    levels = [
        {"difficulty_factor": 50, "visitor_threshold": 50},
        {"difficulty_factor": 500, "visitor_threshold": 500},
    ]
    payload = {
        "levels": levels,
        "duration": 30,
        "description": "create_captcha_test_script",
        "publish_benchmarks": False,
    }
    url = set_path(instance_url, "/api/v1/mcaptcha/create")

    resp = c.post(url, json=payload, cookies=c.cookies.get_dict())
    assert resp.status_code == 200
    return resp.json()["key"]


def get_secret():
    if len(sys.argv) < 3:
        help()
        exit(1)

    instance_url = clean_url(sys.argv[2])
    username = sys.argv[3]
    password = sys.argv[4]

    instance_url = clean_url(sys.argv[2])
    sitekey = sys.argv[3]

    url = set_path(instance_url, "/api/v1/account/secret/get")
    resp = c.get(url, cookies=c.cookies.get_dict())
    assert resp.status_code == 200
    return resp.json()["secret"]


def widget_url():
    if len(sys.argv) < 4:
        help()
        exit(1)

    instance_url = set_path(clean_url(sys.argv[2]), "/widget")
    sitekey = sys.argv[3]
    query = urlencode({"sitekey": sitekey})
    url = f"{instance_url}?{query}"

    return url


if __name__ == "__main__":
    if option == "create_captcha":
        login()
        print(create_captcha())
    elif option == "get_secret":
        login()
        print(get_secret())
    elif option == "widget_url":
        print(widget_url())
    else:
        help()
