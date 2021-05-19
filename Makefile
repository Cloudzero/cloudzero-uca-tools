# Copyright (c) 2016-present, CloudZero, Inc. All rights reserved.
# Licensed under the BSD-style license. See LICENSE file in the project root for full license information.


NAME ?= myPythonLib

ERROR_COLOR = \033[1;31m
INFO_COLOR = \033[1;32m
WARN_COLOR = \033[1;33m
NO_COLOR = \033[0m

.PHONY: init build test
default: test

#################
#
# Helper Targets
#
#################
# Add an implicit guard for parameter input validation; use as target dependency guard-VARIABLE_NAME, e.g. guard-AWS_ACCESS_KEY_ID
guard-%:
	@if [ "${${*}}" = "" ]; then \
		printf \
			"$(ERROR_COLOR)ERROR:$(NO_COLOR) Variable [$(ERROR_COLOR)$*$(NO_COLOR)] not set.\n"; \
		exit 1; \
	fi


help:                                    ## Prints the names and descriptions of available targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


#################
#
# Docker Targets
#
#################
check-docker:                            ## Exits if docker is not installed and available
	@if which docker &>/dev/null ; then \
		printf "$(INFO_COLOR)OK:$(NO_COLOR) docker found on path!\n" ; \
	else \
		printf "$(ERROR_COLOR)ERROR:$(NO_COLOR) docker not found on path. Please install and configure docker!\n" ; \
		exit 1 ; \
	fi


#################
#
# Python Targets
#
#################
init:                                    ## ensures all dev dependencies into the current virtualenv
	@if [[ "$$VIRTUAL_ENV" = "" ]] ; then printf "$(WARN_COLOR)WARN:$(NO_COLOR) No virtualenv found, install dependencies globally." ; fi
	pip install -r requirements-dev.txt


test: check-docker                       ## runs the unit tests on all available python runtimes
	pytest


lint:                                    ## lints the code via adherence to PEP8 standards
	flake8


lint-fix:								                 ## fixes the code in place so that it will pass `make lint`
	autopep8 --ignore E265,E266,E402 --in-place --recursive --max-line-length=120 --exclude vendored .


clean-pyc:                               ## rms pyc, pyo, *~, and __pycache__
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +


build: test                              ## builds sdist
	./setup.py sdist


check-version:													 ## check that version is not in pypi
	@version=$$(awk '/version/{print $$NF}' pyfaaster/__version__.py |  tr -d "'") ; \
	 curl --http1.1 -IN "https://pypi.python.org/pypi?:action=display&name=pyfaaster&version=$${version}" | \
		grep "200 OK" \
		&& { printf "$(ERROR_COLOR)ERROR$(NO_COLOR): Version $(WARN_COLOR)$${version}$(NO_COLOR) already exists in pypi!\n" ; \
				 printf "You probably forgot to update $(WARN_COLOR)pyfaaster/__version__.py$(NO_COLOR). Go do that now.\n" ; exit 1 ; } \
		|| { printf "$(INFO_COLOR)OK$(NO_COLOR): Version $(INFO_COLOR)$${version}$(NO_COLOR) is available in pypi.\n" ; }


upload: build check-version              ## twine uploads dist/*
	twine upload dist/*
