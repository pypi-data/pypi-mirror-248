pip install setuptools
python setup.py sdist bdist_wheel
pip install twine
python3 -m build
python3 -m twine upload --repository-url https://upload.pypi.org/legacy/  dist/*
