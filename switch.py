from port import Port
from device import Device
from net import Net

class Switch(Device):
    def __init__(self, name, n_ports):
        super().__init__(name)
        self.n_ports = int(n_ports)

        self.ports[f"{self.name}_{0}"] = Port(f"{self.name}_{0}")
        self.s = self.ports[f"{self.name}_{0}"]
        self.macs_for_ports={}
        for i in range(1, int(n_ports)+1):
            temp_name = f"{self.name}_{str(i)}"
            self.ports[temp_name] = Port(temp_name)
            self.macs_for_ports[temp_name]=[]#creando un diccionario que tiene como key los nombres de los puertos y por cada uno una lista de las macs que se acceden desde ahi
               
    def read_bit(self, bit, port):
        self.ports[port].read_bit(bit)

    # def update_macs(net:Net,port_0:Port):#hace un bfs para buscar todos los host a los que se llega desde cada puerto y guardarlo en la lista de macs pr puerto
    #     for port in self.ports:
    #         if not(port.name == port_0.name) and not(port.name[len(port.name-1)]=='0')and not(port.name[len(port.name-1)]=='_'):
    #             hosts=net.BFS(port,0,0,True)
    #             for host in hosts[0]:
    #                 self.macs_for_ports[port.name].append(host.mac)
                    



    # def send_port(net:Net,port_0:Port,mac:int):
    #     self.update_macs(net,port_0)
    #     ports_to_send=[]
        
    #     return 0

        
    