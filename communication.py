import serial

class SerialModule:
    def __init__(self, port, baudrate=9600, parity='N', bytesize=8):
        self.port = port
        self.baudrate = baudrate
        self.parity = parity
        self.bytesize = bytesize
        self.serial = None
        self.listeners = {}

    def open(self):
        self.serial = serial.Serial(
            port=self.port,
            baudrate=self.baudrate,
            parity=self.parity,
            bytesize=self.bytesize
        )
        if self.serial.is_open:
            print(f"Seri port {self.port} basarili sekilde acildi.")
            print("-----------------------------------------")
        else:
            print(f"Seri port {self.port} acilirken hata olustu.")
            print("-----------------------------------------")

    def close(self):
        if self.serial and self.serial.is_open:
            self.serial.close()
            print(f"Seri port {self.port} kapandi.")
            print("-----------------------------------------")
        else:
            print(f"Seri port {self.port} acik degil.")
            print("-----------------------------------------")

    def write(self, data):
        if self.serial and self.serial.is_open:
            self.serial.write(data.encode())
        else:
            print(f"Seri port {self.port} acik degil.")
            print("-----------------------------------------")

    def read(self, size):
        if self.serial and self.serial.is_open:
            return self.serial.read(size).decode()
        else:
            print(f"Seri port {self.port} acik degil.")
            print("-----------------------------------------")

    def add_listener(self, character, callback):
        self.listeners[character] = callback

    def remove_listener(self, character):
        if character in self.listeners:
            del self.listeners[character]

    def listen(self):
        if self.serial and self.serial.is_open:
            while True:
                data = self.read(1)
                if data:
                    for character, callback in self.listeners.items():
                        if data == character:
                            callback()
        else:
            raise ValueError(f"Seri port {self.port} acik degil.")
        print("-----------------------------------------")
