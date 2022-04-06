class Device:
    def __init__(self, name = "random", n_ports=1)-> None:
        self.name = name # Nombre del dispositivo
        self.output_name = f'output/{name}.txt'
        self._output = open(self.output_name, 'w') # Archivo de salida en la que se guardaran los logs
        self._output.close()
        self.ports:dict = {}
        self.n_ports = n_ports
    
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
        self._output = open(self.output_name, "a")
        self._output.write(msg+"\n") # Escribiendo mensaje(msg) en el archivo de
        self._output.close()
        
    def close_output(self):
        self._output.close() # Cerrando archivo donde se va a escribir