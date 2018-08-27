__author__ = 'sherrychen'

import serial

from time import sleep

class RCControl(object):

    def __init__(self, serial_port):
        self.serial_port = serial.Serial(serial_port, 115200, timeout=1)

    def steer(self, prediction):
        if prediction == 2:
            self.serial_port.write(chr(1).encode())
            print("Forward")
        elif prediction == 0:
            self.serial_port.write(chr(7).encode())
            print("Left")
        elif prediction == 1:
            self.serial_port.write(chr(6).encode())
            print("Right")
        else:
            self.stop()

    def stop(self):
        self.serial_port.write(chr(0).encode())

    def forward(self):
        self.serial_port.write(chr(0).encode())
        self.serial_port.write(chr(1).encode())
        print("Forward")

    def reverse(self):
        self.serial_port.write(chr(0).encode())
        self.serial_port.write(chr(2).encode())
        print("Reverse")

    def forward_left(self):
        self.serial_port.write(chr(0).encode())
        self.serial_port.write(chr(7).encode())
        print("Forward Left")

    def forward_right(self):
        self.serial_port.write(chr(0).encode())
        self.serial_port.write(chr(6).encode())
        print("Forward Right")

    def reverse_left(self):
        self.serial_port.write(chr(0).encode())
        self.serial_port.write(chr(9).encode())
        print("Reverse Left")

    def reverse_right(self):
        self.serial_port.write(chr(0).encode())
        self.serial_port.write(chr(8).encode())
        print("Reverse Right")

if __name__ == '__main__':
    rc_car = RCControl("/dev/cu.usbmodem1411")
    while True:
        rc_car.forward_left()
        sleep(1)
        rc_car.forward_right()
        sleep(1)
        rc_car.reverse_left()
        sleep(1)
        rc_car.reverse_right()
        sleep(1)


