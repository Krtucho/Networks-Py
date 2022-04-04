from Port import Port
from Device import Device
import random

class Host(Device):
    def __init__(self, name):
        super().__init__(name)
        self.port = Port(f"{self.name}_1")
        
        self.transmitting = False # Si se encuentra transmitiendo en este instante
       # self.time_to_send_next_bit = 10 # Tiempo restante para enviar el siguiente bit de la lista bits_to_send
        self.time_last_bit=0  #Tiempo en que se comenzo a enviar el ultimo bit (el que se esta enviand en este momento)
        self.writing = False    # Esta escribiendo en este instante
        
        self.time_to_retry = 0  # Tiempo necesario para reintentar enviar
        self.pending = False    # Si el host esta intentando reenviar alguna informacion que no puedo enviarla debido a una colision o un a desconexion
        self.bits_to_send = []  # Bits a enviar
        self.actual_bit = 0     # Bit que se esta enviando actualmente


    def read_bit(self, bit, port=1):
        self.port.read_bit(bit)
    
    def send(self, bits:list,time:int):#coloco 
        #transmitting=True  #actualizo a transmitiendo
        self.time_last_bit=time # coloco el tiempo de inicio del bit que envio ahora
        self.writing=True
        for i in bits: 
            self.bits_to_send.append(i) #agrego todos los bits nuevos a la lista de bits a transmitir
        

    # def check_transmision(self):
    #     if self.transmitting:
    #         if !collision:#comprobar que lo que se esta transmitiendo es igual a lo primero que esta en la cola de pendientes
    #             write_in_file_logs()
    #         else:
    #             if self.port.disconnected:
    #                 try_again()
    #             elif collision:
    #                 wait()
            #aqui implementar que si esta em el ultimo ms de su tranmision, entonces su imprimir que su transmision fue ok
        #aqui implementar lo de si esta leyendo y se cambio el ultimo valor que imprimio, mandar a imprimir y agregar a su lista de recibidos
        #y si no se cambio y pasaron 10 ms mandar a escribir y agregar tambien a su lista de recibidos
    
    def check_read(self):
        """Escribe el bit que recibio en el archivo de logs"""
        pass
    # def show_port_name(self):
    #     print(f"{self.name}_{self.port.name}")

