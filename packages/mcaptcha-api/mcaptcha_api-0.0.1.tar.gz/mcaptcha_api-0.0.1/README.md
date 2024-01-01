[![status-badge](https://ci.batsense.net/api/badges/106/status.svg)](https://ci.batsense.net/repos/106)

---

# mcaptcha_api: Python library to interact with mCaptcha server

### Example

```python
mcaptcha = MCaptcha(instance_url=INSTANCE_URL, sitekey=SITEKEY, secret=SECRET)
assert mcaptcha.verify(token=TOKEN) is True
```
