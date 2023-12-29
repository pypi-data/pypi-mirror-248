.PHONY : build upload-test upload install-test install upgrade-test upgrade update-test update

build:
	python -m build

upload-test:
	twine upload --skip-existing --repository testpypi dist/*

upload:
	twine upload --skip-existing --repository pypi dist/*

install-test:
	pip install --index-url https://test.pypi.org/simple/ --no-deps secret-agent

install:
	pip install secret-agent

upgrade-test:
	pip install -U --index-url https://test.pypi.org/simple/ --no-deps secret-agent

upgrade:
	pip install -U secret-agent

update-test: build upload-test upgrade-test

update: build upload upgrade
