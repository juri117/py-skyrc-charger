import usb.core
import usb.util

# Find all connected USB devices
devices = usb.core.find(find_all=True)

# Print information about each device
for device in devices:
    print(f"Device: {device.idVendor}:{device.idProduct}")
