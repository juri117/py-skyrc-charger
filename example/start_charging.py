import sys
import os
import time


if True:  # pylint: disable=W0125
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/..")

# from src.charger import Charger, Config, Action

from py_skyrc_charger import Charger, Config, Action


def rec_data_callback_sample(data):
    print(f"Received data: {data}")


if __name__ == "__main__":
    charger = Charger(rec_data_callback_sample)
    charger.connect()

    conf = Config(2, Action.BALANCE, 6, 1.0, 0.5)

    start_time = time.time()
    while time.time() - start_time < 5:
        charger.poll_all_vals()
        time.sleep(1.0)

    print("START")
    charger.start_program(conf)

    start_time = time.time()
    while time.time() - start_time < 5:
        charger.poll_all_vals()
        time.sleep(1.0)

    print("STOP")
    charger.stop_program(conf.port)

    start_time = time.time()
    while time.time() - start_time < 5:
        charger.poll_all_vals()
        time.sleep(1.0)
