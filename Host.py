from Port import Port
from Device import Device

class Host(Device):
    def __init__(self, name):
        super().__init__(name)
        self.port = Port(f"{self.name}_1")
        
        self.transmitting = False # Si se encuentra transmitiendo en este instante
        self.time_to_send_next_bit = 10 # Tiempo restante para enviar el siguiente bit de la lista bits_to_send
        self.writing = False    # Esta escribiendo en este instante
        
        self.time_to_retry = 0  # Tiempo necesario para reintentar enviar
        self.pending = False    # Si el host esta intentando reenviar alguna informacion que no puedo enviarla debido a una colision o un a desconexion
        self.bits_to_send = []  # Bits a enviar
        self.actual_bit = 0     # Bit que se esta enviando actualmente


    def read_bit(self, bit, port=1):
        self.port.read_bit(bit)
    
    def send_many_bits(self, bits:list):
        pass
    
    def send_bit(self):
        pass
        
   def change_detected(self, bit_to_cmp: int):
       return self.port.bits_received_in_ms == bit_to_cmp

    # def check_transmision(self):
    #     if self.transmitting:
    #         if !collision:
    #             write_in_file_logs()
    #         else:
    #             if self.port.disconnected:
    #                 try_again()
    #             elif collision:
    #                 wait()
    
    def update_bit_time(self, ms: int, collision: bool):
        if self.time_to_send_next_bit == 0:
            if len(self.bits_to_send) > 0:
                self.time_to_send_next_bit = 10
                self.log(f"{ms} {self.name} send {self.actual_bit} {'collision' if collision else 'ok'}")
                self.actual_bit = self.bits_to_send.pop(0)
            elif len(self.bits_to_send) == 0:
                self.time_to_send_next_bit=10
        elif self.time_to_send_next_bit > 0:
            self.time_to_send_next_bit -= 1
            self.log(f"{ms} {self.name} send {self.actual_bit} {'collision' if collision else 'ok'}")

     def write_in_file_logs(self, ms: int,port: Port,sending: bool, collision: bool):
        bit = port.bits_received_in_ms[-1]
        state = "send" if sending else "receive"
        name = port.name
        ok = "collision" if collision else "ok"
        if sending:
            self.write_msg_in_file(f"{ms} {name} {state} {bit} {ok}")
        elif not sending:
            self.write_msg_in_file(f"{ms} {name} {state} {bit}")


    def check_read(self):
        """Escribe el bit que recibio en el archivo de logs"""
        pass
    # def show_port_name(self):
    #     print(f"{self.name}_{self.port.name}")