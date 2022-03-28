class Device:
    def __init__(self, name = "random"):
        self.name = name
        self._output = open(f'output/{name}.txt', 'w') # Archivo de salida en la que se guardaran los logs
        
    def show_port_name(self) -> None:
        pass
    
    def read_bit(self, bit, port):
        pass
    
    def close_output(self):
        self._output.close() # Cerrando archivo donde se va a escribir
    #@staticmethod()
    #def aaa():
    #    pass
    
    