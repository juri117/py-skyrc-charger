

## install

```shell
python -m venv env
env/Scripts/python -m pip install --upgrade pip
env/Scripts/python -m pip install -r requirements.txt
```

linux
```shell
python3 -m venv env
env/bin/python -m pip install pyusb
env/bin/python -m pip install -r requirements.txt
env/bin/python -m pip install --upgrade pip
```



## usb permissions

create a file `/lib/udev/rules.d/50-skyrc-t1000.rules` with the following content:
```bash
ACTION=="add", SUBSYSTEMS=="usb", ATTRS{idVendor}=="0000", ATTRS{idProduct}=="0001", MODE="660", GROUP="plugdev"
```

run:
```bash
sudo adduser $USER plugdev
```