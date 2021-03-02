#!make
# Makefile to simplify some common development tasks.
export SCHEMA_SRC_PATHS=./data/src-urls.json
export CODE_DIR_PATH=./vizzToolsCore


# Run 'make help' for a list of commands.
default: help
help:
	sh -c "$(MAKE) -p no_targets__ | awk -F':' '/^[a-zA-Z0-9][^\$$#\/\\t=]*:([^=]|$$)/ {split(\$$1,A,/ /);for(i in A)print A[i]}' | grep -v '__\$$' | sort"
build-docs:
	python3 ./docs/generate_schema_docs.py
	echo "Docs created!"
build-code:
	curl -O https://raw.githubusercontent.com/vizzTools/ci-scripts/master/json_schema_to_python.sh
	chmod +x ./json_schema_to_python.sh
	./json_schema_to_python.sh
	echo "Code built!"
	rm ./json_schema_to_python.sh
install:
	pip3 install -e .
#test:
#	py.test -v
clean:
	python3 setup.py clean
	find . -name '*.pyc' -delete
	find . -name '*~' -delete
#release:
#	@rm -rf dist/
#	python setup.py sdist upload -r pypi
#	python setup.py bdist_wheel upload -r pypi
#pypi:
#	python setup.py sdist bdist_wheel
#	python -m twine upload dist/*