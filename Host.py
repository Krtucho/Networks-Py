from port import Port
from device import Device
from frame import *
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
        
        # Frames
        self.frames_list:list = [] # Lista con los frames a enviar
        self.actual_frame = -1 # Indice del frame actual de la lista de frames_list
        # Frames times
        self.last_updated_frame_time = 0 # Tiempo transcurrido desde que se envio el ultimo bit
        self.receiving_frame = None#=Frame()#ver despues por que no se construyo la trama vacia
        # Files
        self.data_name = f'output/{name}_data.txt'
        self._data = open(self.data_name, 'w') # Archivo de salida en la que se guardaran los logs

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
        
        data_msg = "".join(data_to_write) + "" if state == "OK" else "ERROR"
        self.save_data(data_msg)
    
    def remove_last_frame(self):
        if self.last_updated_frame_time >= 30:
            
            if self.actual_frame == -1:
                return False
            self.frames_list.pop(self.actual_frame)
            if len(self.frames_list) <= 0:
                self.actual_frame = -1
            return True
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
        if not self.mac_address == dst_mac:
            return False
        if Check.check(frame.get_data_bits(), frame.get_check_bits()):
            self.save_data(frame, "OK")
            return True
        else:
            self.save_data(frame, "ERROR")
            return True


    def read_bit(self, time, bit:int, port=1):#se lee el bit actual y si es el final de la trama se manda a escribir en la data.txt
        self.port.read_bit(bit)        
        if not self.receiving_frame:
            self.receiving_frame=Frame(state="receiving")
        part_of_frame_completed_name,part_of_frame_completed_bits=self.receiving_frame.add_bit(bit)
        if self.receiving_frame.actual_part  == 'end':
            if self.check_frame():
                self.write_data_in_file(self.receiving_frame)

        

       # if self.actual_frame == -1:#esta vacio el frame actual
            
        