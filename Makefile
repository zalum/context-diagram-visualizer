.PHONY: build
test:
		pytest
install-requirements:
		pip install -r requirements.txt
		pip install https://github.com/zalum/system-model-schema/releases/download/0.0.1/system_model_schema-0.0.1.dev1_20190830-py3-none-any.whl
build: install-requirements
		python3 setup.py bdist_wheel egg_info -d