from Port import Port
from Device import Device

class Host(Device):
    def __init__(self, name):
        self.port = Port(f"{self.name}_1")
        
        
    # def show_port_name(self):
    #     print(f"{self.name}_{self.port.name}")