#!/usr/bin/env bash

python3 ./setup.py upload

python3 -m pip install --upgrade build
python3 -m build

python3 -m pip install --upgrade twine
python3 -m twine upload --repository pypi dist/*