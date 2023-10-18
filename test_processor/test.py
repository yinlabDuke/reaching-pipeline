import serial
import struct
import time
import numpy as np

from dlclive import Processor

class test(Processor):
    def __init__(self, com, thres, baudrate=int(9600)):
        super().__init__()
        self.ser - serial.Serial(com, baudrate, timeout=0)
        self.thres = thres

    def switch_led(self):
        self.ser.reset_input_buffer()
        self.out_time.append(time.time())
        self.ser.write(b"I")

        while True:
            led_byte = self.ser.read()
            if len(led_byte) > 0:
                break

    def prcoess(self, pose, **kwargs):
        if kwargs["record"]:
            if pose[3,1] > self.thres:
                self.switch_led()
        return pose
    
    def save(self, filename):
        return 
