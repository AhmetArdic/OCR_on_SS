class DualWriter:
    def __init__(self, serial_module, stdout):
        self.serial_module = serial_module
        self.stdout = stdout

    def write(self, text):
        self.serial_module.write(text)
        self.stdout.write(text)