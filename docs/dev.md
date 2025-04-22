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

```
env/bin/python -m build
env/bin/python -m pip install --upgrade twine
env/bin/python -m twine upload --repository testpypi dist/*
```
