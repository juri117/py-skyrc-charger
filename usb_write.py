import usb.core
import usb.util
import usb.backend.libusb1
import sys
import time


VENDOR_ID = 0x0000
PRODUCT_ID = 0x0001

ENDPOINT_WRITE = 0x02
ENDPOINT_READ = 0x81


def connect_device():
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
                "Could not detatch kernel driver from interface({0}): {1}".format(i, str(e)))
    return dev


def write_data(dev, data):
    res = dev.write(ENDPOINT_WRITE, data)
    return res


def read_data(dev, length):
    try:
        return dev.read(ENDPOINT_READ, length)
    except usb.core.USBError as e:
        print(f"Error: {e}")
        return None


def bytes_to_number(b1, b2):
    return (b1 << 8) | b2


def parse_data(data):
    if len(data) <= 0:
        return None
    if data[0] == 0x0f:
        if data[1] == 0x22 and data[2] == 0x55:
            # print("got vals")
            values = {
                # 'test8': data[0],
                # 'test7': bytes_to_number(data[1], data[2]) / 1000,
                # 'test6': bytes_to_number(data[3], data[4]) / 1000,
                # 'test5': bytes_to_number(data[5], data[6]) / 1000,
                # 'test4': bytes_to_number(data[7], data[8]) / 1000,
                'volt_total': bytes_to_number(data[9], data[10]) / 1000,
                'current': bytes_to_number(data[11], data[12]) / 1000,
                # 'test2': bytes_to_number(data[13], data[14]) / 1000,
                # 'test1': bytes_to_number(data[15], data[16]) / 1000,
                'volt0': bytes_to_number(data[17], data[18]) / 1000,
                'volt1': bytes_to_number(data[19], data[20]) / 1000,
                'volt2': bytes_to_number(data[21], data[22]) / 1000,
                'volt3': bytes_to_number(data[23], data[24]) / 1000,
                'volt4': bytes_to_number(data[25], data[26]) / 1000,
                'volt5': bytes_to_number(data[27], data[28]) / 1000,
                # 'testa': bytes_to_number(data[29], data[30]) / 1000,
                # 'testb': bytes_to_number(data[31], data[32]) / 1000,
                # 'testc': bytes_to_number(data[33], data[34]) / 1000,
                # 'testd': data[35],
                # 'volt_total': bytes_to_number(data[35], data[36]) / 100,
            }
            # print(values)
            return values
    return None


if __name__ == "__main__":

    data_req_vals = bytes.fromhex(
        '0f0355015603000a050ce41068000000000000000000008000000000000000000000000000000000000000000000000000000000000000000000000000000000')

    data_start = bytes.fromhex(
        # '0f1605010003000a050ce41068000000000000000000008000000000000000000000000000000000000000000000000000000000000000000000000000000000')
        '0f1605010006000a050ce41068000000000000000000008300000000000000000000000000000000000000000000000000000000000000000000000000000000')

    data_stop = bytes.fromhex(
        '0f03fe01ff06000a050ce41068000000000000000000008300000000000000000000000000000000000000000000000000000000000000000000000000000000')

    dev = connect_device()

    # res = write_data(dev, data_req_vals)
    # print(f"Wrote data: {res}")
    # time.sleep(1.0)

    # data = read_data(dev, 64)
    # data = dev.read(0x81, 100)
    # print(f"Received data 0x81: {data}")

    # parse_data(data)

    # start
    print("START")
    res = write_data(dev, data_start)
    print(f"Wrote data: {res}")
    time.sleep(1)

    with open(f'usb_data_{time.strftime("%Y-%m-%d_%H-%M-%S")}.txt', 'a') as f:

        start_time = time.time()
        while time.time() - start_time < 3600:  # Run for 1 hour (3600 seconds)
            res = write_data(dev, data_req_vals)
            # print(f"Wrote data: {res}")
            time.sleep(.1)
            for j in range(5):
                data = read_data(dev, 64)
                if data is not None:
                    hex_string = ''.join(f'{x:02x}' for x in data)
                    # print(f"{hex_string}")

                    f.write(
                        f"{time.strftime('%Y-%m-%d_%H-%M-%S')}: {hex_string}\n")
                    data_dict = parse_data(data)
                    print(data_dict)
                    break
                else:
                    time.sleep(0.1)
            time.sleep(0.5)

    time.sleep(1)
    print("STOP")
    res = write_data(dev, data_stop)
    print(f"Wrote data: {res}")

    # stop

    # start
    # dev.write(e, bytes.fromhex(
    #    '0F04FE0001FF00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'))

    # data = dev.read(e, 40)
    # print(f"Received data: {data}")
    #    except Exception as e:
    #        print(f"Error: {e}")
