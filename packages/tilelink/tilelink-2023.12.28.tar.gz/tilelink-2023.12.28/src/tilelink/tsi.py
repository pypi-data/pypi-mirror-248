import struct

import serial


class UARTTSI:
    CMD_READ = 0x00
    CMD_WRITE = 0x01
    def __init__(self, port, baudrate=115200):
        self.ser = serial.Serial(port=port, baudrate=baudrate)
    
    def readWord(self, address):
        command = UARTTSI.CMD_READ
        header = struct.pack("<LQQ", command, address, 0)
        self.ser.write(header)

        received = self.ser.read(4)
        rx_data, = struct.unpack("<L", received)
        return rx_data
    
    def writeWord(self, address, data):
        command = UARTTSI.CMD_WRITE
        header = struct.pack("<LQQ", command, address, 0)
        payload = struct.pack("<L", data)
        buffer = header + payload

        self.ser.write(buffer)


if __name__ == "__main__":
    port = "/dev/ttyUSB3"
    baudrate = 115200

    tsi = UARTTSI(port=port, baudrate=baudrate)
    
    tsi.writeWord(0x08000000, 0xdeadbeef)
    
    print(hex(tsi.readWord(0x08000000)))

