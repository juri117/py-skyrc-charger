


## permissions

create a file `/lib/udev/rules.d/50-skyrc-t1000.rules` with the following content:
```
ACTION=="add", SUBSYSTEMS=="usb", ATTRS{idVendor}=="0000", ATTRS{idProduct}=="0001", MODE="660", GROUP="plugdev"
```

run:
```bash
sudo adduser $USER plugdev
```

## debug with wireshark

filter:
```
usb.dst == "1.6.1" || usb.dst == "1.6.2" || usb.src == "1.6.1" || usb.src == "1.6.2"
usb.dst == "1.6.2" || usb.src == "1.6.1"
```





