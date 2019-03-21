.DEFAULT_GOAL := help
SHELL := /bin/bash

help:                ## Show available options with this Makefile
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

.PHONY: test
test:    ## Install sphinx dependencies
test:
	./upload_test_code.sh && \
	pytest