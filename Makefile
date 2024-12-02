.PHONY: test build clean publish docker-test

test:
	python -m unittest discover tests

build:
	python -m build

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/

# Publish the package to PyPI
publish: build
	twine upload dist/*

docker-test:
	docker build -t ctx-test -f Dockerfile.test .
	docker run --rm ctx-test