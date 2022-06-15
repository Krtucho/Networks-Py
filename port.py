class Port:
    """Clase que representa un puerto de los dispositivos"""
    def __init__(self, name:str):
        self.connected:bool = False # Dice si el puerto se encuentra conectado o no
        self.name: str = name   # Nombre del puerto
        
        self.bits_received_in_ms = -1   # Ultimo bit que se leyo[]
        
    def connect(self):
        self.connected = True
        
    def disconnect(self):
        self.connected = False
        
    def clean_bits_received(self): # Limpia variable de ultimo bit recibido en ms
        self.bits_received_in_ms = -1
        
    def read_bit(self, bit:int):
        self.bits_received_in_ms = bit