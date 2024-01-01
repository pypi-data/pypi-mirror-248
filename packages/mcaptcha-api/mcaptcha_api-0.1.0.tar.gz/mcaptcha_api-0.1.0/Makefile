env:
	./scripts/download-cli.sh download
	. venv/bin/activate && pip install -r requirements.txt
	. venv/bin/activate && pip install build
	. venv/bin/activate && python -m build
	. venv/bin/activate && pip install -e .

test:
	$(eval SECRET = $(shell . ./venv/bin/activate && python ./scripts/create_captcha.py get_secret $(INSTANCE_URL) $(USERNAME) $(PASSWORD)))
	$(eval SITEKEY = $(shell . ./venv/bin/activate && python ./scripts/create_captcha.py create_captcha $(INSTANCE_URL) $(USERNAME) $(PASSWORD)))
	$(eval WIDGET_URL = $(shell . ./venv/bin/activate && python ./scripts/create_captcha.py widget_url $(INSTANCE_URL) $(SITEKEY)))
	$(eval TOKEN = $(shell ./scripts/download-cli.sh gen_pow $(WIDGET_URL)))
	. venv/bin/activate && \
		SITEKEY=$(SITEKEY) SECRET=$(SECRET) \
		INSTANCE_URL=$(INSTANCE_URL) \
		TOKEN=$(TOKEN) pytest

lint:
	black src/ scripts/
