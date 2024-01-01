[![status-badge](https://ci.batsense.net/api/badges/106/status.svg)](https://ci.batsense.net/repos/106)

---

# mcaptcha_api: Python library to interact with mCaptcha server

## Installation

```bash
pip install mcaptcha_api
```

## Usage

| Parameter      | Info                                                                                                                  |
| -------------- | --------------------------------------------------------------------------------------------------------------------- |
| `instance_url` | the URL of the mCaptcha instance you are using                                                                        |
| `sitekey`      | The captcha identifier; can be obtained from dashboard or from widget URL (`http://hostname/widget?sitekey=<sitekey>` |
| `secret`       | Account secret; can be obtained from mCaptcha dashboard account settings page                                         |

```python
mcaptcha = MCaptcha(instance_url=INSTANCE_URL, sitekey=SITEKEY, secret=SECRET)
assert mcaptcha.verify(token=TOKEN) is True
```
