

from dataclasses import dataclass
from checksum import calc_checksum

# bytes
SYNC = 0x0f
CMD_START = [0x16, 0x05]
CMD_STOP = [0x03, 0xfe]
CMD_POLL_VALS = [0x03, 0x55]


class Action:
    BALANCE = 0
    CHARGE = 1
    STORAGE = 3


@dataclass
class Config:
    port: int
    action: Action
    cells: int
    cur_in: float
    cur_out: float

    @property
    def min_volt(self):
        if self.action == Action.STORAGE:
            return 3.85
        else:
            return 3.3

    @property
    def max_volt(self):
        if self.action == Action.STORAGE:
            return 3.85
        else:
            return 4.2


####################################
# get cmd
####################################
def get_cmd_start(config: Config):
    return _get_cmd(config, CMD_START, 0x00, 0)


def get_cmd_stop(config: Config):
    return _get_cmd(config, CMD_STOP, 0xff, 8)


def get_cmd_poll_vals(config: Config):
    return _get_cmd(config, CMD_POLL_VALS, 0x56, 90)


def _get_cmd(config: Config, cmd: list[int], byte4: int, checksum_add: int):
    cur_in = int(config.cur_in * 10)
    cur_out = int(config.cur_out * 10)

    min_volt_bytes = u16_to_bytes(int(config.min_volt * 1000))
    max_volt_bytes = u16_to_bytes(int(config.max_volt * 1000))

    cmd = [SYNC] + cmd + [
        config.port, byte4, config.cells, config.action, cur_in, cur_out
    ] + min_volt_bytes + max_volt_bytes + [
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00
    ]
    return finalize_cmd(cmd, checksum_add=checksum_add)


def finalize_cmd(cmd: list[int], checksum_add: int = 0) -> bytes:
    cmd.append((calc_checksum(cmd) + checksum_add) % 256)
    while len(cmd) < 64:
        cmd.append(0x00)
    return bytes(cmd)


####################################
# parse commands
####################################

def parse_data(data):
    if len(data) <= 0:
        return None
    if data[0] == 0x0f:
        if data[1] == 0x22 and data[2] == 0x55:
            # print("got vals")
            values = {
                # 'test8': data[0],
                # 'test7': bytes_to_u16(data[1], data[2]) / 1000,
                # 'test6': bytes_to_u16(data[3], data[4]) / 1000,
                # 'test5': bytes_to_u16(data[5], data[6]) / 1000,
                # 'test4': bytes_to_u16(data[7], data[8]) / 1000,
                'volt_total': bytes_to_u16(data[9], data[10]) / 1000,
                'current': bytes_to_u16(data[11], data[12]) / 1000,
                # 'test2': bytes_to_u16(data[13], data[14]) / 1000,
                # 'test1': bytes_to_u16(data[15], data[16]) / 1000,
                'volt0': bytes_to_u16(data[17], data[18]) / 1000,
                'volt1': bytes_to_u16(data[19], data[20]) / 1000,
                'volt2': bytes_to_u16(data[21], data[22]) / 1000,
                'volt3': bytes_to_u16(data[23], data[24]) / 1000,
                'volt4': bytes_to_u16(data[25], data[26]) / 1000,
                'volt5': bytes_to_u16(data[27], data[28]) / 1000,
                # 'testa': bytes_to_u16(data[29], data[30]) / 1000,
                # 'testb': bytes_to_u16(data[31], data[32]) / 1000,
                # 'testc': bytes_to_u16(data[33], data[34]) / 1000,
                # 'testd': data[35],
                # 'volt_total': bytes_to_u16(data[35], data[36]) / 100,
            }
            # print(values)
            return values
    return None


####################################
# utils
####################################

def bytes_to_u16(b1, b2):
    return (b1 << 8) | b2


def u16_to_bytes(val):
    return [(val >> 8) & 0xFF, val & 0xFF]


if __name__ == "__main__":
    print(get_cmd_start(Config(1, Action.BALANCE, 6, 1.0, 0.5)).hex())
    print(get_cmd_stop(Config(1, Action.BALANCE, 6, 1.0, 0.5)).hex())
    print(get_cmd_poll_vals(Config(1, Action.BALANCE, 6, 1.0, 0.5)).hex())
