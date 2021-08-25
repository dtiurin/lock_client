import serial
from conf import l

sers = []

COMMANDS = {
    'status': 0x30,
    'open': 0x31,
    'all_status': 0x32,
}

# NOTE: hardcoded addr - only single board available
# addr note: 0x00 - first board, 0x01 second and so on
def send_cmd(cmd, addr=0x01):
    input = [0x02, addr, COMMANDS[cmd], 0x03]
    input.append(sum(input))

    t = serial.Serial("/dev/ttyS0", l, timeout=1000, writeTimeout = 10)

    t.write(serial.to_bytes(input))

