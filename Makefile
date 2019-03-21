.DEFAULT_GOAL := help
SHELL := /bin/bash

help:                ## Show available options with this Makefile
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

.PHONY: test
test:    ## Install sphinx dependencies
test:
	./upload_test_code.sh && \
	pytest

.PHONY: upload_code
upload_code:    ## Install sphinx dependencies
upload_code:
	~/arduino-1.8.8/arduino \
	--upload i2c_controller/i2c_slave_controller.ino \
	--port /dev/ttyUSB0 \
	--board arduino:avr:nano:cpu=atmega328old
