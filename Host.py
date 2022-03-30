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
        
   

    # def check_transmision(self):
    #     if self.transmitting:
    #         if !collision:
    #             write_in_file_logs()
    #         else:
    #             if self.port.disconnected:
    #                 try_again()
    #             elif collision:
    #                 wait()
    
    def check_read(self):
        """Escribe el bit que recibio en el archivo de logs"""
        pass
    # def show_port_name(self):
    #     print(f"{self.name}_{self.port.name}")