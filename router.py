from port import Port
from device import Device
# from net import Net
from port_data import PortData
from route import Route
from frame import Frame

class Router(Device):
    def __init__(self, name, n_ports) -> None:
        super().__init__(name)
        self.n_ports = int(n_ports)
        
        # self.macs_ports = {}
        # self.ip_ports = {}
        
        # Routes
        self.routes_table = {}
        
        self.ports_data = {}
        
        for i in range(1, int(n_ports)+1):
            temp_name = f"{self.name}_{str(i)}"
            self.ports[temp_name] = Port(temp_name)
            
            self.ports_data[temp_name] = PortData()
       
    def set_ip(self, interface, ip):
        self.ports_data[interface].set_ip(ip)
    
    def set_mac(self, interface, mac):
        self.ports_data[interface].set_mac(mac)
      
    def add_route(self, route: Route):
        self.routes_table[route.mask] = route # Las mascaras tienen prioridad, asi que indexamos por las mascaras
      
    # Busca dado un puerto de entrada y un paquete ip retorna el puerto del router por donde debe de seguir
    def forward_packet(self, in_port, ip_packet):
        pass
            
    def read_bit(self, bit, port):
        self.ports[port].read_bit(bit)
        
    def send_bit(self,in_port:Port,bit:int): #Cuando el bfs me envia un bit por un puerto
        # if self.frame_in_for_port.__contains__(in_port):
        #     frame:Frame=self.frame_in_for_port[in_port]
        # else:
        if not self.frame_in_for_port.__contains__(in_port):
            temp_frame:Frame = Frame(state="receiving")
            self.frame_in_for_port[in_port]=temp_frame
            # temp_frame.bits.append(bit)

        frame:Frame = self.frame_in_for_port[in_port]
        part_of_frame_completed_name,part_of_frame_completed_bits=frame.add_bit(bit)
        # if part_of_frame_completed_name == 'dest_mac':#si se acaba de completar la mac de destino
        #     pass
                
        if part_of_frame_completed_name == 'source_mac':#si se acaba de completar la mac de origen se agrega el puerto a la tabla de macs
            self.macs_ports[part_of_frame_completed_bits]=in_port

        if frame.index >= 15:
            if part_of_frame_completed_name == 'overflow':
                temp_frame:Frame = Frame(state="receiving")
                self.frame_in_for_port[in_port]=temp_frame

            # if part_of_frame_completed_name=='check_bits':#si es el ultimo bit del frame que se esta recibiendo vacio envio a la mac y ademas vacio el frame de entrada de este puerto
                # self.send_bit_to_mac(bit,frame.get_dst_mac(),in_port)
                # self.frame_in_for_port[in_port]=Frame()
                # return

            if self.macs_ports.__contains__(frame.get_dst_mac()): #frame.actual_part=='dest_mac'):#si ya se descubrio la mac de destino envio a esta mac
                self.send_bit_to_mac(bit,frame.get_dst_mac(),in_port)
        
        
        return self.send_bit_to_all(bit,in_port)
        
        # if self.macs_ports[frame.get_dst_mac()]:
        #     pass
        