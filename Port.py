class Port:
    def __init__(self, name:str):
        self.connected:bool = False
        self.name: str = name
        
        self.state = "reading"
        self.time = 0
        
        self.bits_received_in_ms = -1# Ultimo bit que se leyo[]
        
    def connect(self):
        self.connected = True
        
    def disconnect(self):
        self.connected = False
        
    def clean_bits_received(self):
        self.bits_received_in_ms = []
        
    def read_bit(self, bit:int):
        self.bits_received_in_ms.append(bit)