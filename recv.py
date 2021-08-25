import RPi.GPIO as GPIO
import serial
import threading

EN_485 =  4
baudrate = 19200

GPIO.setmode(GPIO.BCM)
GPIO.setup(EN_485, GPIO.OUT)
GPIO.output(EN_485, GPIO.LOW)

sers = []
sers.append(serial.Serial("/dev/ttyS0", 
                          baudrate, 
                          writeTimeout = 1,
                          bytesize=8,
                          parity='N',
                          stopbits=1,
                          timeout=None,
                          xonxoff=0,
                          rtscts=0))


print('STARTING LISTENING:')

def interpret_msg(msg):
    
    def get_bitmap(size, mask=0xff):
        if size == 1:
            return 0xff
        else:
            mask = mask << 8
            return mask | get_bitmap(size-1, mask)
    
    get_field_val = lambda o, s: (msg >> o * 8) & get_bitmap(s)

    init_o = 8
    init_s = 1
    data_o = 2
    data_s = 6
    chcksum_o = 0
    chcksum_s = 1
    eom_o = 1
    eom_s = 1

    status_s = 4
    status_o = 2

    status = get_field_val(status_o, status_s)
    print(f'STATUS: {"closed" if status else "opened"}')

    print('------------------------------')


def read_from_port(ser):
    ser.reset_input_buffer()
    ser.reset_output_buffer()
    while True:
        message = ser.read(9).hex()
        message = int(message, 16)
        print(hex(message))
        interpret_msg(message)

for ser in sers:
    thread = threading.Thread(target=read_from_port, args=(ser,))
    thread.start()
