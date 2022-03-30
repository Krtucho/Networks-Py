class Device:
    def __init__(self, name = "random")-> None:
        self.name = name # Nombre del dispositivo
        self._output = open(f'output/{name}.txt', 'w') # Archivo de salida en la que se guardaran los logs
    
    def show_port_name(self) -> None: # 
        pass
    
    def read_bit(self, bit, port):
        pass
    
    
    #@staticmethod()
    #def aaa():
    #    pass
    # def write_in_file_logs(self, port: Port, sending: bool):
    #     pass
    
    def write_msg_in_file(self, msg):
        self._output.write(msg) # Escribiendo mensaje(msg) en el archivo de
        
    def close_output(self):
        self._output.close() # Cerrando archivo donde se va a escribir