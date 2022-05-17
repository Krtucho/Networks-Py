from port import Port
from device import Device
from net import Net
from frame import Frame

class Switch(Device):
    def __init__(self, name, n_ports):
        super().__init__(name)
        self.n_ports = int(n_ports)

        # self.ports[f"{self.name}_{0}"] = Port(f"{self.name}_{0}")
        # self.s = self.ports[f"{self.name}_{0}"]
        self.macs_for_ports={}
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
    def append_bit_to_frame(frame:Frame,bit:int):#agrega el bit al lugar correspondiente en la trama, devuelve -1 si no se completa ninguna parte de la trama y devuelve el nombre de la parte de la trama que se complete
        pass

    def send_bit_to_mac():#cuando ya se conoce la mac de destino y se sabe por que puerto se encuentra solo se envia por el puerto de la mac
        pass

    def send_bit_to_all():#cuando aun no se conoce la mac de destino, se envian estos primeros bits a todo el mundo
        pass



    def send_bit(self,port_0:Port,bit:int): #Cuando el bfs me envia un bit por un puerto
        frame=self.frame_in_for_port[port_0]
        end_frame=self.append_bit_to_frame(frame,bit)
        
        



