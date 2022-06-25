from port import Port
from device import Device
# from net import Net
from frame import Frame

class Switch(Device):
    def __init__(self, name, n_ports):
        super().__init__(name)
        self.n_ports = int(n_ports)

        # self.ports[f"{self.name}_{0}"] = Port(f"{self.name}_{0}")
        # self.s = self.ports[f"{self.name}_{0}"]
        self.macs_ports={}
        for i in range(1, int(n_ports)+1):
            temp_name = f"{self.name}_{str(i)}"
            self.ports[temp_name] = Port(temp_name)
            self.macs_ports={}#diccionario en que se indexa en una mac y devuelve el puerto por donde se alcanza
            #self.macs_for_ports[temp_name]=[]#creando un diccionario que tiene como key los nombres de los puertos y por cada uno una lista de las macs que se acceden desde ahi
            self.frame_in_for_port={}#diccionario en el que se indexa por puerto y se obtiene el frame que esta entrando por ese puerto
            self.frame_out_for_port={}#diccionario en el que se indexa por puerto y se obtiene el frame que esta saliendo por ese puerto  

    def read_bit(self, bit, port):
        self.ports[port].read_bit(bit)


#lo puse dentro de switch para no tocar frame por ahora, pero va dentro de frame
    #def append_bit_to_frame(frame:Frame,bit:int):#agrega el bit al lugar correspondiente en la trama, devuelve -1 si no se completa ninguna parte de la trama y devuelve el nombre de la parte de la trama que se complete
        

    def send_bit_to_all(self,bit:int,in_port:Port):#cuando aun no se conoce la mac de destino, se envian estos primeros bits a todo el mundo
        ports_to_send= []#[ p if not(p==in_port) else pass for p in self.ports]
        for p in self.ports.values():
            if not(p==in_port):
                ports_to_send.append(p)
        return ports_to_send
        


    def send_bit_to_mac(self,bit:int,mac:str,in_port:Port):#cuando ya se conoce la mac de destino y se sabe por que puerto se encuentra solo se envia por el puerto de la mac
        if self.macs_ports.__contains__(mac):
            port=self.macs_ports[mac]
            if(self.macs_ports[mac]==in_port):
                return []
            return port
        else:
            return self.send_bit_to_all(bit,in_port)

    def send_bit(self,in_port:Port,bit:int): #Cuando el bfs me envia un bit por un puerto
        # if self.frame_in_for_port.__contains__(in_port):
        #     frame:Frame=self.frame_in_for_port[in_port]
        # else:
        if not self.frame_in_for_port.__contains__(in_port):
            temp_frame:Frame = Frame()
            self.frame_in_for_port[in_port]=temp_frame
            # temp_frame.bits.append(bit)

        frame:Frame = self.frame_in_for_port[in_port]
        part_of_frame_completed_name,part_of_frame_completed_bits=frame.add_bit(bit)
        # if part_of_frame_completed_name == 'dest_mac':#si se acaba de completar la mac de destino
        #     pass
        if part_of_frame_completed_name == 'source_mac':#si se acaba de completar la mac de origen se agrega el puerto a la tabla de macs
            self.macs_ports[part_of_frame_completed_bits]=in_port

        if not (frame.actual_part=='dest_mac'):#si ya se descubrio la mac de destino envio a esta mac
            return self.send_bit_to_mac(bit,frame.get_dst_mac(),in_port)
            
        return self.send_bit_to_all(bit,in_port)
        
        # if self.macs_ports[frame.get_dst_mac()]:
        #     pass
        


        

        
        



