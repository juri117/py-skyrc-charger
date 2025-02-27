import usb.core
import usb.util
import usb.backend.libusb1
import sys
import os


os.environ['LIBUSB_DEBUG'] = '4'

if False:

    # Try multiple backend paths where libusb DLL might be
    possible_paths = [
        # Default path
        None,
        # Common Windows installation paths
        r'C:\Windows\System32\libusb0.dll',
        r'C:\Windows\System32\libusb-1.0.dll',

        # Current directory
        os.path.join(os.path.dirname(__file__), 'libusb-1.0.dll'),
    ]

    backend = None
    for path in possible_paths:
        try:
            backend = usb.backend.libusb1.get_backend(
                find_library=lambda x: path)
            if backend is not None:
                print(f"Successfully loaded USB backend from: {path}")
                break
        except Exception as e:
            print(f"Failed to load backend from {path}: {str(e)}")

    if backend is None:
        print("Error: Could not find libusb backend. Please ensure libusb is installed.")
        print("Try installing libusb using Zadig (https://zadig.akeo.ie/)")
        sys.exit(1)


# USB device identifiers
VENDOR_ID = 0x0000
PRODUCT_ID = 0x0001

print("Core:", usb.core.find(find_all=True))

devs = usb.core.find(find_all=True)
for dev in devs:
    print(
        f"Vendor ID: 0x{dev.idVendor:04x}, Product ID: 0x{dev.idProduct:04x}")

# Find the USB device
device = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)

# Add debug information
if device is None:
    # List all available USB devices
    print("Available USB devices:")
    for dev in usb.core.find(find_all=True):
        print(
            f"Vendor ID: 0x{dev.idVendor:04x}, Product ID: 0x{dev.idProduct:04x}")
    raise ValueError(
        'Device not found. Please check the Vendor ID and Product ID.')

try:
    # Get current configuration
    cfg = device.get_active_configuration()
    print(f"Active configuration: {cfg}")
except usb.core.USBError:
    # If there's no active configuration or we can't read it
    print("No active configuration found. Attempting to set configuration...")

# usb.util.claim_interface(device, 0)

# Reset the device
device.reset()

# Set the active configuration
# device.set_configuration()

# Optionally, claim the interface (usually interface 0)
# If you get permission errors, you might need to detach the kernel driver

'''
try:
    if device.is_kernel_driver_active(0):
        device.detach_kernel_driver(0)
    device.set_interface_altsetting(0, 0)
except (usb.core.USBError, NotImplementedError) as e:
    print(f"Note: Could not set interface: {str(e)}")
'''

# Data captured from Wireshark
data = bytes([
    0x1b, 0x00, 0xc0, 0x68, 0xd0, 0xfb, 0x0d, 0x82, 0xff, 0xff,
    0x00, 0x00, 0x00, 0x00, 0x09, 0x00, 0x00, 0x01, 0x00, 0x06,
    0x00, 0x02, 0x01, 0x40, 0x00, 0x00, 0x00, 0x0f, 0x03, 0x5f,
    0x02, 0x61, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00
])

# Send the data to endpoint 0x02
# try:
bytes_written = device.write(0x02, data)
print(f"Wrote {bytes_written} bytes to device")
# except usb.core.USBError as e:
#    print(f"Failed to write to device: {str(e)}")
