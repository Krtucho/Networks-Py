from Port import Port
from Device import Device

class Hub(Device):
    def __init__(self, name, n_ports):
        self.n_ports = n_ports
        self.ports: dict = {}

        self.ports[f"{self.name}_{0}"] = Port(f"{self.name}_{0}")
        self.s = self.ports[f"{self.name}_{0}"]
        
        for i in [1, n_ports+1]:
            temp_name = f"{self.name}_i"
            self.ports[temp_name] = Port(temp_name)
            
    def read_bit(self, bit, port):
        self.ports[port].read_bit(bit)