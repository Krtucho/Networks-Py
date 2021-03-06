from port import Port
from device import Device

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
        

    def read_bit(self, bit, port=1):
        self.port.read_bit(bit)
    
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