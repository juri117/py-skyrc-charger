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


commands = [
    "0f2255010100010004596903de001900000ee30ee80ee60ee90ee70ee8000000000100d6",
    "0f2255010100010004597103de001900000ee50eea0ee70eea0ee80ee8000000000100e5",
    "0f2255010100010005597403de001900000ee50eea0ee80eea0ee90eea000000000100ed",
    "0f2255010100010006597f03d8001900000ee80eec0ee90eeb0eea0eea000000000100fb"
]

for cmd in commands:
    raw_data = bytes.fromhex(cmd)
    data = parse_data(raw_data)
    print(data)
