

import unittest

import sys
import os

if True:  # pylint: disable=W0125
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/..")


from py_skyrc_charger.commands import (get_cmd_start, Action, get_cmd_poll_vals,
                                       get_cmd_stop, Config, get_cmd_get_version, parse_data, Status)


# compare messages captured by wireshark, with messages generated by this package

class TestCommands(unittest.TestCase):
    def test_get_cmd_start(self):
        test_cases = [
            # port, action, cells, cur_in, cur_out, stop, expected hex string
            (Config(1, Action.BALANCE, 2, 1.0, 0.5),
             '0f1605010002000a050ce41068000000000000000000007f'
             '00000000000000000000000000000000000000000000000000000000000000000000000000000000'),
            (Config(1, Action.BALANCE, 2, 1.0, 0.5),
             '0f1605010002000a050ce41068000000000000000000007f'
             '00000000000000000000000000000000000000000000000000000000000000000000000000000000'),
            (Config(1, Action.BALANCE, 6, 2.0, 0.5),
             '0f16050100060014050ce41068000000000000000000008d'
             '00000000000000000000000000000000000000000000000000000000000000000000000000000000'),
            (Config(1, Action.BALANCE, 6, 20.0, 0.5),
             '0f160501000600c8050ce410680000000000000000000041'
             '00000000000000000000000000000000000000000000000000000000000000000000000000000000'),
            (Config(1, Action.CHARGE, 6, 1.0, 0.5),
             '0f1605010006010a050ce410680000000000000000000084'
             '00000000000000000000000000000000000000000000000000000000000000000000000000000000'),
            (Config(1, Action.STORAGE, 6, 1.0, 0.5),
             '0f1605010006030a050f0a0f0a0000000000000000000050'
             '00000000000000000000000000000000000000000000000000000000000000000000000000000000'),
            (Config(2, Action.BALANCE, 6, 1.0, 0.5),
             '0f1605020106000a050ce410680000000000000000000085'
             '00000000000000000000000000000000000000000000000000000000000000000000000000000000'),
            (Config(1, Action.DISCHARGE, 6, 20.0, 0.5),
             '0f160501000602c8050ce410680000000000000000000043'
             '00000000000000000000000000000000000000000000000000000000000000000000000000000000'),
            (Config(1, Action.PARALLEL, 6, 20.0, 0.5),
             '0f160501000606c8050ce41068000000000000000000004700000000000000000000000000000000'
             '000000000000000000000000000000000000000000000000'),
            (Config(1, Action.PARALLEL, 6, 35.0, 0.5),
             '0f1605010006065e050ce4106800000000010000000000de00000000000000000000000000000000'
             '000000000000000000000000000000000000000000000000'),
            (Config(1, Action.IDLE, 6, 1.0, 0.5),
             '0f035a015b000000000000000000000000000000000000000000000000000000000000000000000000'
             '0000000000000000000000000000000000000000000000'),
            (Config(2, Action.IDLE, 6, 1.0, 0.5),
             '0f035a025c000000000000000000000000000000000000000000000000000000000000000000000000'
             '0000000000000000000000000000000000000000000000'),
            (Config(1, Action.IDLE_2, 6, 1.0, 0.5),
             '0f035f0160000000000000000000000000000000000000000000000000000000000000000000000000'
             '0000000000000000000000000000000000000000000000'),
            (Config(2, Action.IDLE_2, 6, 1.0, 0.5),
             '0f035f0261000000000000000000000000000000000000000000000000000000000000000000000000'
             '0000000000000000000000000000000000000000000000'),

        ]

        for config, expected_hex in test_cases:
            with self.subTest(config=config):
                expected = bytes.fromhex(expected_hex)
                result = get_cmd_start(config)
                self.assertEqual(result, expected, f"\nexpected:\n{expected.hex()}\nresult:\n{result.hex()}")

    def test_get_cmd_stop(self):
        test_cases = [
            # port, action, cells, cur_in, cur_out,  expected hex string
            (Config(1, Action.BALANCE, 6, 1.0, 0.5),
             '0f03fe01ff06000a050ce410680000000000000000000083'
             '00000000000000000000000000000000000000000000000000000000000000000000000000000000'),
            (Config(1, Action.BALANCE, 2, 1.0, 0.5),
             '0f03fe01ff02000a050ce41068000000000000000000007f'
             '00000000000000000000000000000000000000000000000000000000000000000000000000000000'),
        ]

        for config, expected_hex in test_cases:
            with self.subTest(config=config):
                expected = bytes.fromhex(expected_hex)
                result = get_cmd_stop(config)
                self.assertEqual(result, expected)

    def test_get_cmd_poll_vals(self):
        test_cases = [
            # port, action, cells, cur_in, cur_out,  expected hex string
            (Config(1, Action.BALANCE, 3, 1.0, 0.5),
             '0f0355015603000a050ce410680000000000000000000080'
             '00000000000000000000000000000000000000000000000000000000000000000000000000000000'),
        ]

        for config, expected_hex in test_cases:
            with self.subTest(config=config):
                expected = bytes.fromhex(expected_hex)
                result = get_cmd_poll_vals(config)
                self.assertEqual(result, expected)

    def test_parse_vals(self):
        test_data = [("cell_error", Status.ERROR,
                      "0f22550104000c000a050000017a100050320000000000000000000000000000000102850000b6"
                      "00000000000000000000000000000000000000000000000000"
                      ),
                     ("connection_error", Status.ERROR,
                      "0f22550104000b000a050000017a100050320000000000000000000000000000000102840000b6"
                      "00000000000000000000000000000000000000000000000000"
                      ),
                     ("timeout_error", Status.ERROR,
                      "0f225501040005000a050000017a1000503200000000000000000000000000000001027e000088"
                      "00000000000000000000000000000000000000000000000000"
                      ),
                     ("timeout_error_later", Status.ERROR,
                      "0f225501040005000a050000017a1000503200000000000000000000000000000001027e000088"
                      "00000000000000000000000000000000000000000000000000"
                      ),
                     ("pre_timeout_error", Status.ACTIVE,
                      "0f225501010001003b2c0b0066001d00000ea90eae0eb00064005f005b0000000001009d000088"
                      "00000000000000000000000000000000000000000000000000"
                      ), ("ok", Status.ACTIVE,
                          "0f22550101000000002bfe0000001b00000ea60eab0eac0064005f005b000000000100e1000000"
                          "00000000000000000000000000000000000000000000000000")]
        for data in test_data:
            # print(f"test: {data[0]}")
            vals = parse_data(bytes.fromhex(data[2]))
            self.assertEqual(vals.is_error, False)
            self.assertEqual(vals.data["status"], data[1])

    def test_get_cmd_get_version(self):
        test_cases = [
            '0f03570158'
            '00000000000000000000000000000000000000000000000000000000000000000000000000000000'
            '00000000000000000000000000000000000000',
        ]

        for expected_hex in test_cases:
            # with self.subTest(config=config):
            expected = bytes.fromhex(expected_hex)
            result = get_cmd_get_version()
            self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
