def test_checksum_algorithms(commands):
    def sum_modulo256(data):
        return sum(data) % 256

    def twos_complement_sum(data):
        total = sum(data)
        return (256 - (total % 256)) % 256

    def crc8(data):
        crc = 0
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 0x80:
                    crc = (crc << 1) ^ 0x07
                else:
                    crc <<= 1
                crc &= 0xFF
        return crc

    for cmd in commands:
        # Convert hex string to bytes (excluding last byte)
        data = bytes.fromhex(cmd[:-2])
        actual = int(cmd[-2:], 16)

        sum_check = sum_modulo256(data)
        twos_check = twos_complement_sum(data)
        crc_check = crc8(data)

        print(f"\nCommand: {cmd}")
        print(f"Actual checksum: {actual:02x}")
        print(f"Sum mod 256: {sum_check:02x}")
        print(f"Two's complement: {twos_check:02x}")
        print(f"CRC8: {crc_check:02x}")


# Test commands
commands = [
    "0f1605010002000a050ce41068000000000000000000007f",
    "0f1605010006000a050ce410680000000000000000000083",
    "0f160501000600c8050ce410680000000000000000000041",
    "0f03fe01ff06030a050f0a0f0a0000000000000000000050",
    "0f03fe01ff06000a050ce410680000000000000000000083",
    "0f2255010100010004596903de001900000ee30ee80ee60ee90ee70ee8000000000100d6",
    "0f2255010100010004597103de001900000ee50eea0ee70eea0ee80ee8000000000100e5",
    "0f2255010100010005597403de001900000ee50eea0ee80eea0ee90eea000000000100ed",
    "0f2255010100010006597f03d8001900000ee80eec0ee90eeb0eea0eea000000000100fb",
    "0f225501010000000158f10833001800000eb00eb30eaf0eb70eb10eb200000000010075",
    "0f225501010000000258f10068001800000ea90ea90ea40eaf0ea70ea80000000001006b",
    "0f2255010100000002592301e2001800000ed30ed70ed30ed90ed60ed700000000010028",
    "0f2255010100010003595603e1001800000ee00ee50ee30ee40ee40ee3000000000100ae",
    "0f2255010100010004596003d8001800000ee20ee70ee30ee50ee60ee5000000000100b9",
    "0f2255010100010004596603d9001800000ee30ee70ee50ee70ee60ee5000000000100c5",
    "0f2255010100010005596903d8001800000ee30ee90ee60ee70ee70ee8000000000100cf",
    "0f2255010100010005597103d2001900000ee40eea0ee60ee90ee90ee9000000000100d9",
    "0f2255010100020006597403da001900000ee50eea0ee80ee90ee90ee9000000000100e9"
]

for cmd in commands:
    raw_data = bytes.fromhex(cmd)
    data = raw_data[:-1]
    # data = data[1:]
    checksum = 0
    for byte in data:
        checksum += byte
        checksum = checksum % 256
    print(
        f"Checksum: {raw_data[-1]:02x} =? {checksum:02x}, diff: {raw_data[-1] - checksum}")


# test_checksum_algorithms(commands)
