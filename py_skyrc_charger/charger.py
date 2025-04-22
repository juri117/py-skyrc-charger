import sys
import time
import threading
from typing import Callable, Optional, Dict

import usb.core
import usb.util
import usb.backend.libusb1


from .commands import Config, Action, get_cmd_start, get_cmd_stop, get_cmd_poll_vals, parse_data


VENDOR_ID = 0x0000
PRODUCT_ID = 0x0001

ENDPOINT_WRITE = 0x02
ENDPOINT_READ = 0x81


class Charger:
    def __init__(self, rec_data_callback: Optional[Callable[[Dict], None]] = None):
        self.dev = None
        self._rec_data_callback = rec_data_callback
        self.read_thread = None
        self.stop_requested = False
        # init with a basic config otherwise data polling is not working
        self.port_configs = {1: Config(1, Action.BALANCE, 6, 1.0, 0.5),
                             2: Config(2, Action.BALANCE, 6, 1.0, 0.5)}

    def connect_device(self):
        dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
        if dev is None:
            raise ValueError('Device not found')
        print(dev[0].interfaces())
        i = dev[0].interfaces()[0].bInterfaceNumber
        if dev.is_kernel_driver_active(i):
            try:
                dev.detach_kernel_driver(i)
            except usb.core.USBError as e:
                sys.exit(
                    f"Could not detach kernel driver from interface({i}): {e}")
        self.dev = dev
        self.start_read_thread()

    def start_read_thread(self):
        if self.read_thread is None:
            self.stop_requested = False
            self.read_thread = threading.Thread(target=self._read_data_thread, daemon=True)
            self.read_thread.start()

    def stop_read_thread(self):
        self.stop_requested = True
        self.read_thread = None

    def start_program(self, config: Config):
        self.port_configs[config.port] = config
        cmd = get_cmd_start(config)
        self._write_data(cmd)

    def stop_program(self, config: Config):
        cmd = get_cmd_stop(config)
        self._write_data(cmd)
        # self.port_configs[config.port] = None

    def poll_all_vals(self):
        for config in self.port_configs.values():
            if config is not None:
                self.poll_vals(config)

    def poll_vals(self, config: Config):
        cmd = get_cmd_poll_vals(config)
        self._write_data(cmd)

    def _write_data(self, data):
        try:
            # print(f"write: {data.hex()}")
            res = self.dev.write(ENDPOINT_WRITE, data)
            return res
        except usb.core.USBError as e:
            print(f"Error: {e}")
            return None

    def _read_data(self, length):
        try:
            return self.dev.read(ENDPOINT_READ, length, timeout=1000)
        except usb.core.USBError as e:
            print(f"Error: {e}")
        return None

    def _read_data_thread(self):
        while not self.stop_requested:
            data = self._read_data(64)
            if data is not None and self._rec_data_callback is not None:
                vals = parse_data(data)
                self._rec_data_callback(vals)
            else:
                print("No data")
            time.sleep(0.1)


def rec_data_callback_sample(data):
    print(f"Received data: {data}")


if __name__ == "__main__":
    charger = Charger(rec_data_callback_sample)
    charger.connect_device()

    conf = Config(1, Action.BALANCE, 6, 1.0, 0.5)
    charger.start_program(conf)

    start_time = time.time()
    while time.time() - start_time < 60:
        # charger.poll_vals(conf)
        charger.poll_all_vals()
        time.sleep(1.0)

    print("START")
    charger.start_program(conf)

    start_time = time.time()
    while time.time() - start_time < 600:
        charger.poll_vals(conf)
        time.sleep(1.0)

    print("STOP")
    charger.stop_program(conf)
