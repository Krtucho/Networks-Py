from ip_packet import IP_Packet
from port import Port
from device import Device
# from net import Net
from port_data import PortData
from route import Route
from frame import Frame
from utils import ip_str_to_ip_bit

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
       
    def set_ip(self, interface, ip, mask):
        self.ports_data[interface].set_ip(ip, mask)
    
    def set_mac(self, interface, mac):
        self.ports_data[interface].set_mac(mac)
      
    def add_route(self, route: Route):
        self.routes_table[route.mask] = route # Las mascaras tienen prioridad, asi que indexamos por las mascaras
    
    def modify_and_send_frame(self, frame:Frame, ip_packet: IP_Packet, new_dst_ip):
        new_dst_ip_tr, _ = ip_str_to_ip_bit(new_dst_ip)
        
        ip_packet.edit_dst_ip(new_dst_ip)
        frame.edit_data_bits(ip_packet.bits)
        return frame    
     
    def ip_and_mask(self, ip, mask, destination):
        _, mask_tr = ip_str_to_ip_bit(mask)
        _, dest_tr = ip_str_to_ip_bit(destination)
        
        and_lst = [0,0,0,0]
        
        for i in range(0, 4):
            and_lst[i] = ip[i] & mask_tr[i]
        
        return mask_tr[0] == dest_tr
     
    # Busca dado un puerto de entrada y un paquete ip retorna el puerto del router por donde debe de seguir
    def forward_packet(self, in_port, ip_packet: IP_Packet, frame:Frame):
        dst_ip = ip_packet.get_dst_ip()
        if dst_ip == None:
            return None
        dst_ip = ip_packet.convert_from_bits_to_ip(dst_ip)
        
        # Ordeno mi tabla de rutas y me quedo con la lista resultante
        items = list(self.routes_table.keys)
        items.sort()
        items.reverse()
        for item in items:
        # Aplico AND entre ip del destino en ip_packet y cada mascara ordenadamente
            for temp_route in item:
                if self.ip_and_mask(dst_ip, temp_route.mask, temp_route.destination):
                    port_name = f"{self.name}_{str(temp_route.interface)}"
                    if temp_route.gateway == "0.0.0.0":
                        self.ports_data[port_name].add_frame_out(frame_to_send)
                        return self.ports[port_name]
                    else:
                        frame_to_send = self.modify_and_send_frame(frame, ip_packet, temp_route.gateway)
                        self.ports_data[port_name].add_frame_out(frame_to_send)
                        return self.ports[port_name]
                        
        
        
            
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
        