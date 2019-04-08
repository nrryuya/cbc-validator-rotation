#!/bin/sh

flake8

pip install -r requirements.txt -r requirements-test.txt

pytest
