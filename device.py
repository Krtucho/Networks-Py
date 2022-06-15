class Device:
    def __init__(self, name = "random", n_ports=1)-> None:
        self.name = name # Nombre del dispositivo
        self.output_name = f'output/{name}.txt'
        self._output = open(self.output_name, 'w') # Archivo de salida en la que se guardaran los logs
        self._output.close()
        self.ports:dict = {}
        self.n_ports = n_ports
    
    def write_msg_in_file(self, msg):
        self._output = open(self.output_name, "a")
        self._output.write(msg+"\n") # Escribiendo mensaje(msg) en el archivo de salida
        self._output.close()
        
    def close_output(self):
        self._output.close() # Cerrando archivo donde se va a escribir