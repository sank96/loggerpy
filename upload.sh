#!/usr/bin/env bash
python3 setup.py sdist bdist_wheel

python3 -m twine upload dist/*

sleep 3

pip install --upgrade loggerpy
