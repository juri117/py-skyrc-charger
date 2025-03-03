

from dataclasses import dataclass
from checksum import calc_checksum, check_checksum

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
            data = data[0:36]
            res = check_checksum(data)
            if not res:
                print("checksum failed")
                return None
            # print("got vals")
            values = {
                'unknown_3': data[3],  # ? const 1
                'unknown_4': data[4],  # ? const 1
                'charge_total': bytes_to_u16(data[5], data[6]) / 1000,  # Ah
                'time': bytes_to_u16(data[7], data[8]),  # s
                'volt_total': bytes_to_u16(data[9], data[10]) / 1000,  # V
                'current': bytes_to_u16(data[11], data[12]) / 1000,  # A
                'unknown_13': data[13],  # ? const 0
                'system_temp': data[14],  # ? system temperatur C ?
                'unknown_15': data[15],  # ? const 0
                'unknown_16': data[16],  # ? const 0
                'volt0': bytes_to_u16(data[17], data[18]) / 1000,  # V
                'volt1': bytes_to_u16(data[19], data[20]) / 1000,  # V
                'volt2': bytes_to_u16(data[21], data[22]) / 1000,  # V
                'volt3': bytes_to_u16(data[23], data[24]) / 1000,  # V
                'volt4': bytes_to_u16(data[25], data[26]) / 1000,  # V
                'volt5': bytes_to_u16(data[27], data[28]) / 1000,  # V
                'unknown_29': data[29],  # ? const 0
                'unknown_30': data[30],  # ? const 0
                'unknown_31': data[31],  # ? const 0
                'unknown_32': data[32],  # ? const 0
                'unknown_33': data[33],  # ? const 1
                'unknown_34': data[34],  # ? const 0
                # 'checksum': data[35],
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
