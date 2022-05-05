from port import Port
from device import Device

class Switch(Device):
    def __init__(self, name, n_ports):
        super().__init__(name)
        self.n_ports = int(n_ports)

        self.ports[f"{self.name}_{0}"] = Port(f"{self.name}_{0}")
        self.s = self.ports[f"{self.name}_{0}"]
        
        for i in range(1, int(n_ports)+1):
            temp_name = f"{self.name}_{str(i)}"
            self.ports[temp_name] = Port(temp_name)
            
    def read_bit(self, bit, port):
        self.ports[port].read_bit(bit)

    