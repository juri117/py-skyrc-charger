

import unittest

import sys
import os

if True:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/../../")


from py_charger.src.commands import get_cmd_start, Action, get_cmd_poll_vals, get_cmd_stop, Config


# I compare messages, captured by wireshark, with my generated messages

class TestCommands(unittest.TestCase):
    def test_get_cmd_start(self):
        test_cases = [
            # port, action, cells, cur_in, cur_out, stop, expected hex string
            (Config(1, Action.BALANCE, 2, 1.0, 0.5),
             '0f1605010002000a050ce41068000000000000000000007f00000000000000000000000000000000000000000000000000000000000000000000000000000000'),
            (Config(1, Action.BALANCE, 2, 1.0, 0.5),
             '0f1605010002000a050ce41068000000000000000000007f00000000000000000000000000000000000000000000000000000000000000000000000000000000'),
            (Config(1, Action.BALANCE, 6, 2.0, 0.5),
             '0f16050100060014050ce41068000000000000000000008d00000000000000000000000000000000000000000000000000000000000000000000000000000000'),
            (Config(1, Action.BALANCE, 6, 20.0, 0.5),
             '0f160501000600c8050ce41068000000000000000000004100000000000000000000000000000000000000000000000000000000000000000000000000000000'),
            (Config(1, Action.CHARGE, 6, 1.0, 0.5),
             '0f1605010006010a050ce41068000000000000000000008400000000000000000000000000000000000000000000000000000000000000000000000000000000'),
            (Config(1, Action.STORAGE, 6, 1.0, 0.5),
             '0f1605010006030a050f0a0f0a000000000000000000005000000000000000000000000000000000000000000000000000000000000000000000000000000000'),
            (Config(2, Action.BALANCE, 6, 1.0, 0.5),
             '0f1605020006000a050ce41068000000000000000000008400000000000000000000000000000000000000000000000000000000000000000000000000000000'),
        ]

        for config,  expected_hex in test_cases:
            with self.subTest(config=config):
                expected = bytes.fromhex(expected_hex)
                result = get_cmd_start(config)
                self.assertEqual(result, expected)

    def test_get_cmd_stop(self):
        test_cases = [
            # port, action, cells, cur_in, cur_out,  expected hex string
            (Config(1, Action.BALANCE, 6, 1.0, 0.5),
             '0f03fe01ff06000a050ce41068000000000000000000008300000000000000000000000000000000000000000000000000000000000000000000000000000000'),
            (Config(1, Action.BALANCE, 2, 1.0, 0.5),
             '0f03fe01ff02000a050ce41068000000000000000000007f00000000000000000000000000000000000000000000000000000000000000000000000000000000'),
        ]

        for config,  expected_hex in test_cases:
            with self.subTest(config=config):
                expected = bytes.fromhex(expected_hex)
                result = get_cmd_stop(config)
                self.assertEqual(result, expected)

    def test_get_cmd_poll_vals(self):
        test_cases = [
            # port, action, cells, cur_in, cur_out,  expected hex string
            (Config(1, Action.BALANCE, 3, 1.0, 0.5),
             '0f0355015603000a050ce41068000000000000000000008000000000000000000000000000000000000000000000000000000000000000000000000000000000'),
        ]

        for config,  expected_hex in test_cases:
            with self.subTest(config=config):
                expected = bytes.fromhex(expected_hex)
                result = get_cmd_poll_vals(config)
                self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
