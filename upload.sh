#!/usr/bin/env bash
python3 setup.py sdist bdist_wheel

python3 -m twine upload dist/*

echo -n "Waiting..."
for _ in {1..10}
do
  echo -n "."
  sleep 0.5
done
echo


pip install --upgrade loggerpy
