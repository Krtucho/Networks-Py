from Port import Port
from Device import Device

class Host(Device):
    def __init__(self, name):
        super().__init__(name)
        self.port = Port(f"{self.name}_1")
        self.transmitting = False
    def read_bit(self, bit, port=1):
        self.port.read_bit(bit)
        pass
    
    def send_many_bits(bits:list):
        self.send
    def send_bit(self):
        pass
    
    def check_transmision(self)
        if self.transmitting:
            if ! collision:
                write_in_file_logs()
            else:
                if self.port.disconnected:
                    try_again()
                elif collision:
                    wait()
    
    def check_read(self):
        """Escribe el bit que recibio en el archivo de logs"""
        pass
    # def show_port_name(self):
    #     print(f"{self.name}_{self.port.name}")