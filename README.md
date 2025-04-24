
# py skyrc charger

this package allows to interface with skyrc chargers using the usb-connection as a more flexible replacement for the *Charge Master* software.

## supported devices

this code was developed and tested using the T1000: https://www.skyrc.com/t1000
however chargers working with the original Charge Master software are likely to work as well. A list of supported devices is on the download page of Charge Master: https://www.skyrc.com/downloads

**tested on linux only**, windows should also work, but it is more difficult to setup the usb driver

# setup (linux)

## fix usb permissions

this might be necessary to run the code without sudo.

create a file `/lib/udev/rules.d/50-skyrc-t1000.rules` with the following content:
```bash
ACTION=="add", SUBSYSTEMS=="usb", ATTRS{idVendor}=="0000", ATTRS{idProduct}=="0001", MODE="660", GROUP="plugdev"
```

run:
```bash
sudo adduser $USER plugdev
```
