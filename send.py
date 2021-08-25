import serial

baudrate = 19200

sers = []

SOM = 0x02
EOM = 0x03

COMMANDS = {
    'status': 0x30,
    'open': 0x31,
    'all_status': 0x32,
}

# NOTE: hardcoded addr - only single board available
# addr note: 0x00 - first board, 0x01 second and so on
def send_cmd(cmd, addr=0x00):
    input = [SOM, addr, COMMANDS[cmd], EOM]
    input.append(sum(input))

    t = serial.Serial("/dev/ttyS0", baudrate, timeout=1000, writeTimeout = 10)

    t.write(serial.to_bytes(input))

