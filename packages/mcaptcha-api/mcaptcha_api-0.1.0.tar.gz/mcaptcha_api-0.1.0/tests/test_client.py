# SPDX-FileCopyrightText: 2023 Aravinth Manivannan <realaravinth@batsense.net>
#
# SPDX-License-Identifier: Apache-2.0
# SPDX-License-Identifier: MIT

import os
from mcaptcha_api import MCaptcha 

INSTANCE_URL = os.environ["INSTANCE_URL"]
SITEKEY = os.environ["SITEKEY"]
SECRET = os.environ["SECRET"]
TOKEN = os.environ["TOKEN"]

def test_client():
    mcaptcha = MCaptcha(instance_url=INSTANCE_URL, sitekey=SITEKEY, secret=SECRET)
    assert mcaptcha.verify(token=TOKEN) is True
    assert mcaptcha.verify(token="foo") is False
