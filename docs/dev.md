## setup development environment

### linux

```shell
python3 -m venv env
env/bin/python -m pip install --upgrade pip
env/bin/python -m pip install -r requirements.txt
```

### windows

```shell
python -m venv env
env/Scripts/python -m pip install --upgrade pip
env/Scripts/python -m pip install -r requirements.txt
```

## deploy

```shell
# install requirements
env/bin/python -m pip install --upgrade twine

# build
env/bin/python -m build
# deploy to test.pypi.org
env/bin/python -m twine upload --repository testpypi dist/* --verbose
# deploy to pypi.org
env/bin/python -m twine upload dist/*
```

## install from test.pypi.org

```shell
env/bin/python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps py-skyrc-charger --upgrade
```