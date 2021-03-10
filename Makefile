.PHONY: build

test:
		pytest

install-requirements:
		pip install -r requirements.txt  --index-url https://pypi.org/simple

build: install-requirements
		python3 setup.py bdist_wheel egg_info -d

get-artifact-name:
	@ls dist/*.whl