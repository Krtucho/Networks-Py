from port import Port
from device import Device

class Hub(Device):
    def __init__(self, name, n_ports):
        super().__init__(name)
        self.n_ports = int(n_ports)
        self.states_ports={}

        #self.ports[f"{self.name}_{0}"] = Port(f"{self.name}_{0}")
        #self.s = self.ports[f"{self.name}_{0}"]
        
        for i in range(1, int(n_ports)+1):
            temp_name = f"{self.name}_{str(i)}"
            self.ports[temp_name] = Port(temp_name)
            
    def read_bit(self, bit, port):
        self.ports[port].read_bit(bit)

    def send_port(self,in_port:Port):
        ports_to_send:list=[]
        self.states_ports[in_port]="receive"
        for port in self.ports:
            if not(port.name == in_port.name):
                ports_to_send.append(port)
                self.states_ports[in_port]="send"
        return ports_to_send

    