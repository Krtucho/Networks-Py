from port import Port
from device import Device
from frame import *
# from check import Check
# from frame import Frame

class Host(Device):
    def __init__(self, name, signal_time=10):
        super().__init__(name)
        self.port = Port(f"{self.name}_1")
        self.ports[0] = self.port
        self.transmitting = False # Si se encuentra transmitiendo en este instante
        self.writing = False    # Esta escribiendo en este instante
        
        self.time_to_retry = 0  # Tiempo necesario para reintentar enviar
        self.pending = False    # Si el host esta intentando reenviar alguna informacion que no puedo enviarla debido a una colision o un a desconexion
        self.bits_to_send = []  # Bits a enviar
        self.actual_bit = -1     # Bit que se esta enviando actualmente

        self.signal_time = signal_time
        
        self.time_to_send_next_bit = signal_time # Tiempo restante para enviar el siguiente bit de la lista bits_to_send
        
        self.mac_address = "" # Direccion mac de esta pc, por el momento se tendra que asignar manualmente
        self.ip_adress=[]
        # Frames
        self.frames_list:list = [] # Lista con los frames a enviar
        self.actual_frame = -1 # Indice del frame actual de la lista de frames_list
        # Frames times
        self.last_updated_frame_time = 0 # Tiempo transcurrido desde que se envio el ultimo bit
        self.receiving_frame = None#=Frame()#ver despues por que no se construyo la trama vacia
        # Files
        self.data_name = f'output/{name}_data.txt'
        self._data = open(self.data_name, 'w') # Archivo de salida en la que se guardaran los logs

        #IP Packets
        self.ip_packets_list:list = [] # Lista con los ip_packets a enviar
        


    def add_frame(self, frame:Frame):
        if len(self.frames_list) == 0:
            self.actual_frame = 0
        self.frames_list.append(frame)

    def create_frame(self, bit):
        self.frames_list.append(Frame())

    def change_detected(self, bit_to_cmp: int):
        change:bool = False
        if bit_to_cmp == -1: # S
            change = False
        else:
            change = not (self.port.bits_received_in_ms == bit_to_cmp)
            
        self.port.bits_received_in_ms = bit_to_cmp
        return change

    def update_bit_time(self, ms: int, collision: bool):
        if self.time_to_send_next_bit == 0:
            # Si aun faltan bits por enviar resetea el tiempo restante de envio y extrae el primer bit de la lista que fue la que se envio
            self.bits_to_send.pop(0) #  extrae el primer bit de la lista que fue la que se envio
            if len(self.bits_to_send) != 0: # Si solamente queda
                self.actual_bit = self.bits_to_send[0] # actualiza el bit que se esta enviando actualmente
                self.write_msg_in_file(f"{ms} {self.port.name} send {self.actual_bit} {'collision' if collision else 'ok'}")
                self.time_to_send_next_bit = self.signal_time -1
            else:
                self.pending = False
                self.writing = False
                self.transmitting = False
                self.actual_bit = -1
                self.time_to_send_next_bit = self.signal_time -1
        elif self.time_to_send_next_bit > 0:
            self.time_to_send_next_bit -= 1

    def write_in_file_logs(self, ms: int, sending: bool, collision: bool):
        bit = -1
        if sending or collision:
            bit = self.actual_bit
        else:
            bit = self.port.bits_received_in_ms
        state = "send" if sending else "receive"
        name = self.port.name
        ok = "collision" if collision else "ok"
        if sending:
            self.write_msg_in_file(f"{ms} {name} {state} {bit} {ok}")
            print(f"{ms} {name} {state} {bit} {ok}")
            
        elif not sending:
            self.write_msg_in_file(f"{ms} {name} {state} {bit}")
            print(f"{ms} {name} {state} {bit}")
            

    def check_read(self):
        """Escribe el bit que recibio en el archivo de logs"""
        pass
    
    def save_data(self, data_msg):
        self._data = open(self.data_name, "a")
        self._data.write(data_msg+"\n") # Escribiendo mensaje(msg) en el archivo de salida
        self._data.close()
        
    def close_output(self):
        self._output.close() # Cerrando archivo donde se va a escribir
    
    def write_data_in_file(self, frame:Frame, state="OK"):
        data_to_write = frame.get_data_bits()
        sender = frame.get_src_mac()
        data_msg = "sender: " + sender + " " + "".join([str(v) for v in data_to_write]) + " OK" if state == "OK" else " ERROR"
        self.save_data(data_msg)
    
    def remove_last_receiving_frame(self):
            # if self.last_updated_frame_time >= 30:
            
        if self.receiving_frame == None:# or len(self.frames_list) <= 0:
            return False
        self.receiving_frame = None
        # self.frames_list.pop(self.actual_frame)
        # if len(self.frames_list) <= 0:
        #     self.actual_frame = -1
        
        return True
        
    
    def remove_last_sending_frame(self):
        # if self.last_updated_frame_time >= 30:
            
        if self.actual_frame == -1 or len(self.frames_list) <= 0:
            return False
        self.frames_list.pop(self.actual_frame)
        if len(self.frames_list) <= 0:
            self.actual_frame = -1
        return False
        
        # if self.actual_frame == -1:
        #     return False
        # if Check.check_frame_len(self.frames_list[self.actual_frame]):
        #     self.frames_list.pop(self.actual_frame)
        #     if len(self.frames_list) <= 1:
        #         self.
          
    def can_remove_frame(self):
        # if self.last_updated_frame_time >= 30:
            
        if self.actual_frame == -1:
            return False
        if len(self.frames_list) <= 0:
            self.actual_frame = -1
        return True
        # return False
                
    def check_frame(self):
        """ """
        if self.receiving_frame == None:
            return False
        # if not self.can_remove_frame():
        #     return False
        #aqui lo hace con la lista de los frames que yo entiendo que son para enviar
        frame:Frame = self.receiving_frame#self.frames_list.pop(self.actual_frame)
        # if len(self.receiving_frame) <= 0:
        #     self.actual_frame = -1
        dst_mac = frame.get_dst_mac()
        if not (self.mac_address == dst_mac or dst_mac == "FFFF"):
            return False
        check_ok = frame.check_frame()#Check.check(frame.get_data_bits(), frame.get_check_bits())
        if check_ok:
            self.write_data_in_file(frame, "OK")
            return True
        else:
            self.write_data_in_file(frame, "ERROR")
            return True


    def read_bit(self, time, bit:int, port=1):#se lee el bit actual y si es el final de la trama se manda a escribir en la data.txt
        self.port.read_bit(bit)        
        if not self.receiving_frame:
            self.receiving_frame=Frame(state="receiving")
        part_of_frame_completed_name,part_of_frame_completed_bits=self.receiving_frame.add_bit(bit)
        if self.receiving_frame.actual_part  == 'end':
            if self.check_frame():
                self.remove_last_receiving_frame()
                # self.write_data_in_file(self.receiving_frame)

        

       # if self.actual_frame == -1:#esta vacio el frame actual
            


    #se le pasa el ip de destino y los datoa a enviar y crea un paquete ip con esto
    #ademas lo adiciona a la lista de paquetes ip a enviar
    def create_ip_packet():
        pass

    #se le pasa in paquete ip, crea un frame con este y lo manda a enviar
    #adiciona este frame a la lista de frames a enviar y ademas comienza su envio
    def create_frame_from_ip_packet():
        pass

    #por aqui se envia in paquete ip, si el ip de destino no pertenece a la tabla de rutas del host
    #se hace una peticion arp para detectar la mac correspondiente al ip de destino
    def send_ip_packet(self,ip_destino:str):
        pass

    #metodo encargado de enviar la peticion arpq
    def send_arpq(self, ip_destino:str):
        pass

    #metodo encargado de recibir la respuesta arpr
    def receive_arpr(self,frame:Frame):
        pass

    #metodo que envia la respuesta de la peticion arpq
    def send_arpr(self, tiempo:int, mac_destino:str):
        pass

    #metodo que recibe la peticion arpq y verifica si hay que dar la respuesta
    def receive_arpq_petition(self,frame:Frame):
       pass

    