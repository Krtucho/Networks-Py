class Port:
    def __init__(self, name:str):
        self.connected:bool = False
        self.name: str = name
        
        self.state = "reading"
        self.time = 0